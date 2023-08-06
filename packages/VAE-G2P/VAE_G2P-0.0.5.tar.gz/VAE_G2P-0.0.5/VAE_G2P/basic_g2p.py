import numpy as np
import torch
from torch import nn
import pyro
import pyro.distributions as dist
from torch.utils import data
from collections import deque
from scipy.stats import linregress
import copy

from .networks import FCLayers
from .data import GeneToPhenotypeDataset
from .data_wrapper import TorchDataWrapper




def _rel_diff(curr,prev):
    return abs((curr - prev) / prev)

def _collate_it(x):
    return x[0]


def _returnELBOSlopeError(elbo_deque):
    """ Takes that average of the deque containing ELBO values. Helps determine convergence in the face of noisy SVI by taking the slope of the ELBO values as a function of iteration number. Error is computed as abs(slope)/mean(ELBO)
    
    Parameters
    ----------
    elbo_deque : collections.deque
        Deque containing previous N ELBO values (depends on deque size).
    
    Returns
    -------
    float
        ELBO error 
    """
    return abs(linregress(range(len(elbo_deque)),elbo_deque)[0]/np.mean(elbo_deque))



class BasicG2PMapLoss(nn.Module):
    def __init__(self):
        super(BasicG2PMapLoss,self).__init__()

    def forward(self,symptoms_logits,missing_logits, freq_logits, obs_symptoms, obs_freq_classes,cut_points):
        symptom_annot_loss=dist.Bernoulli(logits=symptoms_logits).log_prob(obs_symptoms).sum()

        freq_missing=torch.zeros(obs_freq_classes.shape,dtype=torch.float32,device=freq_logits.device)
        freq_missing[(obs_freq_classes==-1.0)]=1.0
        missing_loss=dist.Bernoulli(logits=missing_logits[obs_symptoms==1.0]).log_prob(freq_missing[obs_symptoms==1.0]).sum()

        
        freq_missing_mask = torch.zeros(obs_freq_classes.shape,dtype=torch.bool,device=freq_logits.device)
        freq_obs_mask = torch.zeros(obs_freq_classes.shape,dtype=torch.bool,device=freq_logits.device)
        freq_missing_mask[obs_symptoms==1.0]=1
        freq_obs_mask[(obs_symptoms==1.0)&(obs_freq_classes!=-1.0)]=1
        if freq_obs_mask.sum()>0:
            freq_loss=dist.OrderedLogistic(freq_logits[freq_obs_mask],cut_points).log_prob(obs_freq_classes[freq_obs_mask]).sum()
        else:
            freq_loss=0.0

        return -1.0*(symptom_annot_loss+missing_loss+freq_loss)


class BasicG2PMapLoss_Categortical(nn.Module):
    def __init__(self):
        super(BasicG2PMapLoss_Categortical,self).__init__()

    def forward(self,symptoms_logits,missing_logits, freq_logits, obs_symptoms, obs_freq_classes):
        symptom_annot_loss=dist.Bernoulli(logits=symptoms_logits).log_prob(obs_symptoms).sum()

        freq_missing=torch.zeros(obs_freq_classes.shape,dtype=torch.float32,device=freq_logits.device)
        freq_missing[(obs_freq_classes==-1.0)]=1.0
        missing_loss=dist.Bernoulli(logits=missing_logits[obs_symptoms==1.0]).log_prob(freq_missing[obs_symptoms==1.0]).sum()

        
        freq_missing_mask = torch.zeros(obs_freq_classes.shape,dtype=torch.bool,device=freq_logits.device)
        freq_obs_mask = torch.zeros(obs_freq_classes.shape,dtype=torch.bool,device=freq_logits.device)
        freq_missing_mask[obs_symptoms==1.0]=1
        freq_obs_mask[(obs_symptoms==1.0)&(obs_freq_classes!=-1.0)]=1
        if freq_obs_mask.sum()>0:
            freq_loss=dist.Categorical(logits=freq_logits[freq_obs_mask,:]).log_prob(obs_freq_classes[freq_obs_mask]).sum()
        else:
            freq_loss=0.0

        return -1.0*(symptom_annot_loss+missing_loss+freq_loss)

class BasicG2PMap(nn.Module):
    def __init__(self,
        n_predictors,
        n_symptoms,
        n_freq_classes,
        network_hyperparameters={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True},
        update_embedding=False,
        cut_points = [0.04,0.3,0.8,0.99]
        ):
        super(BasicG2PMap,self).__init__()
        self.n_predictors=n_predictors
        self.n_outcomes=n_symptoms
        self.n_freq_classes=n_freq_classes
        self.network_hyperparameters=network_hyperparameters
        self.cut_points=torch.logit(torch.tensor(cut_points,dtype=torch.float32))

        self.mlp=FCLayers(n_in=self.n_predictors, n_out=network_hyperparameters['n_hidden'], n_layers=network_hyperparameters['n_layers'],
                                n_hidden=network_hyperparameters['n_hidden'], dropout_rate=network_hyperparameters['dropout_rate'],use_batch_norm=network_hyperparameters['use_batch_norm'],use_activation=True,activation_fn=nn.ReLU)
        self.symptom_layer=nn.Linear(network_hyperparameters['n_hidden'],self.n_outcomes,bias=True)
        self.missing_layer=nn.Linear(network_hyperparameters['n_hidden'],self.n_outcomes,bias=True)
        self.freq_layer=nn.Linear(network_hyperparameters['n_hidden'],self.n_outcomes,bias=True)

    def forward(self, data_arrays):
        hidden_state = self.mlp(data_arrays)
        symptom_logits = self.symptom_layer(hidden_state)
        missing_logits = self.missing_layer(hidden_state)
        freq_logits =  self.freq_layer(hidden_state)
        return symptom_logits,missing_logits,freq_logits

    def package_state(self):
        """
        Packages the model state dict as a dictionary.

        Returns
        -------
        dict
            Model state dict.

        """
        packaged_model_state={}
        packaged_model_state['model_state'] = copy.deepcopy(self.state_dict(keep_vars=True))
        return packaged_model_state

    def load_state(self,prior_model_state):
        """
        Loads model state from dictionary

        Parameters
        ----------
        prior_model_state : dict
            Dictionary of model state produced by PackageCurrentState

        Returns
        -------
        None

        """
        self.load_state_dict(prior_model_state['model_state'],strict=True)

class BasicG2PModel:

    def __init__(self,
        g2p_dataset,
        network_hyperparameters={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True},
        cut_points=[0.04,0.3,0.8,0.99]
        ):
        self.g2p_dataset=g2p_dataset
        self.cut_points=torch.logit(torch.tensor(cut_points,dtype=torch.float32))

        self.n_pred=len(self.g2p_dataset.symptom_map)
        self.n_freq_class=len(self.g2p_dataset.ordinal_freq_map)-1
        self.basic_net = BasicG2PMap(self.g2p_dataset.aux_gene_info_table['return_dim'].sum(), self.n_pred,self.n_freq_class,network_hyperparameters=network_hyperparameters)
        self.basic_net.eval()

    def Fit(self,batch_size,learning_rate,max_epochs,errorTol,compute_device=None,numDataLoaders=0,verbose=True,logFile=None,early_stop_patience=5,monitor_validation=False,weight_decay=0.0001):

        if compute_device is None:
            compute_device='cpu'
        else:
            try:
                device_type,device_num=compute_device.split(':')
            except ValueError:
                device_type=compute_device
                device_num='0'
                compute_device=device_type+':'+device_num
            assert device_type in ['cuda','mps','cpu']," Only 'cuda','mps', and 'cpu' supported"
            if device_type=='mps':
                assert torch.backends.mps.is_available()==True,"mps device not available"
            if device_type=='cuda':
                assert torch.cuda.is_available()==True,"cuda device is not available"


        errorComputationWindow = max(int(0.01*max_epochs),2)

        error_window = deque(maxlen=errorComputationWindow)
        elbo_window = deque(maxlen=errorComputationWindow)
        errorVec = []
        trainLoss = []
        validationLoss = []


        if self.g2p_dataset.training_index is not None:
            numTotalTrainingSamples=self.g2p_dataset.training_index.shape[0]
            numTotalValidationSamples=self.g2p_dataset.validation_index.shape[0]
        else:
            raise ValueError("Training state for OMIMDataset.DatasetTrainingState not set prior to calling optimizer. Please set training set using data.DatasetTrainingState.SetNewTrainingState") 

        assert batch_size < numTotalTrainingSamples, "Batch size is greater than or equal to training data size."

        self.basic_net.to(compute_device)
        self.cut_points=self.cut_points.detach().to(compute_device)

        torchTrainingData=TorchDataWrapper(self.g2p_dataset,batch_size,index='Training')
        torchValidationData=TorchDataWrapper(self.g2p_dataset,batch_size,index='Validation')


        optimizer = torch.optim.AdamW(self.basic_net.parameters(), lr=learning_rate,weight_decay=weight_decay)
        criterion = BasicG2PMapLoss()
        criterion.to(compute_device)
        

        bestModelState=self.basic_net.package_state()

        trainingDataLoader = data.DataLoader(torchTrainingData,num_workers=numDataLoaders,collate_fn=_collate_it)
        validationDataLoader = data.DataLoader(torchValidationData,num_workers=numDataLoaders,collate_fn=_collate_it)

        avg_epoch_train_loss = 0.0
        self.basic_net.eval()
        for i,data_batch in enumerate(trainingDataLoader):
            if compute_device.split(':')[0]!='cpu':
                data_batch=tuple([x.to(compute_device) for x in data_batch])
            preds=self.basic_net(data_batch[2])
            loss = criterion(*preds, data_batch[0],data_batch[1],self.cut_points) / (data_batch[0].shape[0]/numTotalTrainingSamples)
            avg_epoch_train_loss+=loss.item()
        avg_epoch_train_loss=avg_epoch_train_loss/(i+1)
        prev_train_loss=avg_epoch_train_loss
        elbo_window.append(prev_train_loss)


        

        avg_epoch_val_loss = 0.0
        for i,data_batch in enumerate(validationDataLoader):
            if compute_device.split(':')[0]!='cpu':
                data_batch=tuple([x.to(compute_device) for x in data_batch])
            preds=self.basic_net(data_batch[2])
            loss = criterion(*preds, data_batch[0],data_batch[1],self.cut_points) / (data_batch[0].shape[0]/numTotalValidationSamples)

            avg_epoch_val_loss+=loss.item()
        avg_epoch_val_loss=avg_epoch_val_loss/(i+1.0)
        bestModelScore=np.inf

        early_stop_count=0

        for epoch in range(max_epochs):
            torchTrainingData.shuffle_index()
            avg_epoch_train_loss = 0.0
            self.basic_net.train()
            for i,data_batch in enumerate(trainingDataLoader):
                if compute_device.split(':')[0]!='cpu':
                    data_batch=tuple([x.to(compute_device) for x in data_batch])
                optimizer.zero_grad()
                with torch.set_grad_enabled(True):
                    preds=self.basic_net(data_batch[2])
                    loss = criterion(*preds, data_batch[0],data_batch[1],self.cut_points) / (data_batch[0].shape[0]/numTotalTrainingSamples)
                    loss.backward()
                    optimizer.step()
                avg_epoch_train_loss+=loss.item()
            avg_epoch_train_loss=avg_epoch_train_loss/(i+1)

            self.basic_net.eval()
            avg_epoch_val_loss = 0.0
            for i,data_batch in enumerate(validationDataLoader):
                if compute_device.split(':')[0]!='cpu':
                    data_batch=tuple([x.to(compute_device) for x in data_batch])
                preds=self.basic_net(data_batch[2])
                loss = criterion(*preds, data_batch[0],data_batch[1],self.cut_points) / (data_batch[0].shape[0]/numTotalValidationSamples)
                avg_epoch_val_loss+=loss.item()
            avg_epoch_val_loss=avg_epoch_val_loss/(i+1.0)


            if np.isnan(avg_epoch_val_loss) or np.isnan(avg_epoch_train_loss):
                print("Warning: NaN detected during inference. Model unlikely to be fully optimized!")
                break

            if monitor_validation:
                if avg_epoch_val_loss<bestModelScore:
                    bestModelState = self.basic_net.package_state()
                    bestModelScore = avg_epoch_val_loss
                    early_stop_count=0
                else:
                    early_stop_count+=1 
            else:
                if avg_epoch_train_loss<bestModelScore:
                    bestModelState = self.basic_net.package_state()
                    bestModelScore = avg_epoch_train_loss
                    early_stop_count=0
                else:
                    early_stop_count+=1 




            #track overall convergence
            trainLoss+=[avg_epoch_train_loss]
            validationLoss+=[avg_epoch_val_loss]

            error_window.append(_rel_diff(avg_epoch_train_loss,prev_train_loss))
            elbo_window.append(avg_epoch_train_loss)

            avg_error = sum(error_window)/len(error_window)
            med_error = sorted(error_window)[int(0.5*len(error_window))]
            slope_error = _returnELBOSlopeError(elbo_window)

            prev_train_loss=avg_epoch_train_loss
            errorVec+=[min([avg_error,med_error,slope_error])]





            if early_stop_count>early_stop_patience:
                if verbose:
                    print("BasicG2PModel model diverging after %03d epochs; stopping optimization. Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                if logFile!=None:
                    with open(logFile, "a") as f:
                        f.write("BasicG2PModel model diverging after %03d epochs; stopping optimization. Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                break

            if (avg_error < errorTol) or (med_error < errorTol) or (slope_error<errorTol):


                if verbose:
                    print("BasicG2PModel model optimization converged in %03d epochs; Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                if logFile!=None:
                    with open(logFile, "a") as f:
                        f.write("BasicG2PModel model optimization converged in %03d epochs; Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                break

            else:
                if verbose:
                    print("Completed %03d epochs of BasicG2PModel model training; Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                if logFile!=None:
                    with open(logFile, "a") as f:
                        f.write("Completed %03d epochs of BasicG2PModel model training; Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))


        if epoch == (max_epochs-1):
            print('Warning: Optimization did not converge in allotted epochs')

        self.basic_net.load_state(bestModelState)
        #set eval mode
        if compute_device.split(':')[0]!='cpu':
            self.basic_net.to('cpu')
            self.cut_points=self.cut_points.detach().to('cpu')
        self.basic_net.eval()

        return bestModelScore,trainLoss,validationLoss,errorVec
            

    def PredictOutcomes(self,index=None,gene_list=None):
        assert (index is not None) ^ (gene_list is not None) or (embed_values is not None),"Must provide either: disease index, HGNC id, or a vector of embedding values to generate data."
        if self.basic_net.training:
            self.basic_net.eval()
            in_training=True
        else:
            in_training=False

        if index is not None:
            gene_list=[self.g2p_dataset.inverse_gene_map[x] for x in self.g2p_dataset.disease_table.loc[index]['MappedGenes'].values]
        assert len(set(gene_list).difference(self.g2p_dataset.gene_map.keys()))==0, "Genes: {0:s} not in GeneToPhenotypeDataset".format(','.join(list(gene_list)))
        gene_input=self.g2p_dataset.ReturnGeneDataArrays(gene_list)
        output=self.basic_net.forward(gene_input)

      
        if in_training:
            self.basic_net.train()
        symptoms=torch.sigmoid(output[0]).detach().clone().numpy()
        missing=torch.sigmoid(output[1]).detach().clone().numpy()
        frequency=torch.exp(dist.OrderedLogistic(output[2],self.cut_points).logits).detach().clone().numpy()  
        return {'BaselineSymptomRates':symptoms,"MissingRates":missing,'FrequencyRates':frequency}  

    def PerplexCompareNull(self,hpo_freq_pairs,gene_list):

        if self.basic_net.training:
            self.basic_net.eval()
            in_training=True
        else:
            in_training=False

        annot_array=torch.zeros((max(len(hpo_freq_pairs),len(gene_list)),self.n_pred),dtype=torch.float32)
        freq_array=torch.zeros((max(len(hpo_freq_pairs),len(gene_list)),self.n_pred),dtype=torch.float32)
        for t,hpo_freq_vec in enumerate(hpo_freq_pairs):
            idx_vec=[self.g2p_dataset.symptom_map[x[0]] for x in hpo_freq_vec]
            freq_vec=[self.g2p_dataset.ordinal_freq_map[x[1]] for x in hpo_freq_vec]
            annot_array[t,idx_vec]=1
            freq_array[t,idx_vec]=torch.tensor(freq_vec,dtype=torch.float32)
        data_arrays=(annot_array,freq_array,self.g2p_dataset.ReturnGeneDataArrays(gene_list))


        pred_log_odds=self.basic_net.forward(data_arrays[2])
        if in_training:
            self.basic_net.train()

        null_model_log_odds=tuple(torch.logit(self.g2p_dataset._torchWrapper(x)).unsqueeze(dim=0) for x in self.g2p_dataset.InferNullModel().values())
        output=np.zeros((pred_log_odds[0].shape[0],3))
        perplex_function_null=BasicG2PMapLoss_Categortical()
        perplex_function_basic=BasicG2PMapLoss()
        for i in range(output.shape[0]):
            output[i,0]=perplex_function_basic(pred_log_odds[0][i:i+1],pred_log_odds[1][i:i+1],pred_log_odds[2][i:i+1], data_arrays[0][i:i+1],data_arrays[1][i:i+1],self.cut_points).detach().item()
            output[i,1]=perplex_function_null(null_model_log_odds[0],null_model_log_odds[1],null_model_log_odds[2], data_arrays[0][i:i+1],data_arrays[1][i:i+1]).detach().item()
            output[i,2]=output[i,0]-output[i,1]

        return {'BasicG2PModel Perplex.':output[:,0],'Null Perplex.':output[:,1],'BasicG2PModel-Null':output[:,2]}


    def LoadModel(self,stored_model):
        """
        Loads previously fit model either from a dictionary (generated using PackageModel) or from a file path (with file constructed using PackageModel)

        Parameters
        ----------
        stored_model : either dict or str (file path)

        Returns
        -------
        None.

        """
        if not isinstance(stored_model,dict):
            assert isinstance(stored_model,str),"Expects file name if not provided with dictionary."
            with open(stored_model,'rb') as f:
                model_dict = torch.load(f,map_location='cpu')

        self.basic_net.load_state(model_dict)



    def PackageModel(self,fName=None):
        """
        Packages the current model and returns it as a python dictionary. Will optionally write this dictionary to disk using PyTorch.

        Parameters
        ----------
        fName : str, default None
            File path to save model to disk. The default is None, which means that only a model dictionary will be returned.

        Returns
        -------
        model_dict : dict
            Dictionary containing fitted model parameters in addition to general meta data.

        """
        model_dict = self.basic_net.package_state()
        if fName is not None:
            with open(fName,'wb') as f:
                torch.save(model_dict,f)
        return model_dict



