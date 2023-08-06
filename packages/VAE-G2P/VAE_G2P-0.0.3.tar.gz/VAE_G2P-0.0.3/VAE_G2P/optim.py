import numpy as np
import torch
import pyro
from pyro.infer import SVI
from pyro.infer import Trace_ELBO
from torch.utils import data
from pyro.optim import AdamW
from scipy.stats import linregress
from pyro import poutine
from collections import deque

from .data_wrapper import TorchDataWrapper

def rel_diff(curr,prev):
    return abs((curr - prev) / prev)

def collate_it(x):
    return x[0]


class AnnealingScheduler:
    def _cosine_anneal(self,currentStepFrac):
        cos_vals = np.cos(np.pi * currentStepFrac) + 1.0
        return self.finalTemp + ((self.initTemp - self.finalTemp) / 2.0) * cos_vals

    def _linear_anneal(self,currentStepFrac):
        return (self.finalTemp - self.initTemp) * currentStepFrac + self.initTemp

    def __init__(self,initTemp,finalTemp,totalNumSteps,scheduleType):
        """ Scheduler for KL-Anneling.

        Parameters
        ----------
        initTemp : float
            Initial temperature.
        finalTemp : float
            Final temperature.
        totalNumSteps : int
            Number of total steps for annealing
        scheduleType : str
            Type of scheduler. Must be 'linear' or 'cosine'.

        Returns
        -------
        None

        """

        assert initTemp>=0.0 and finalTemp >=0.0,"Annealing temperatures must be greater than 0.0"
        self.initTemp=initTemp
        self.finalTemp=finalTemp
        self.totalNumSteps=totalNumSteps
        if scheduleType=='linear':
            self._anneal_func=self._linear_anneal
        else:
            self._anneal_func=self._cosine_anneal

    def currentTemp(self,currentStep):
        frac = currentStep/self.totalNumSteps
        if frac>1.0:
            return self.finalTemp
        else:
            return self._anneal_func(frac)


class AutoEncoderOptimizer:

    def _returnELBOSlopeError(self,elbo_deque):
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




    def __init__(self,vae_model,dataset_training_state,optimizationParameters={'learningRate': 0.05,'maxEpochs': 500,'numParticles':10},computeConfiguration={'device':None,'numDataLoaders':0}, **kwargs):
        """

        This class implements a SGD optimizer, which uses mini-batches randomly sampled from a training dataset. To improve convergence rate and escape local minima, learning rate can be autommatically altered during inference. Note, given stochastic inference strategy coupled with possible re-starts, class tracks model perfomance and stores the best possible instance of the model obtained throughout the inference process.

                vae_model-->The vae model to optimize
                dataset_training_state-->DatasetTrainingState that holds clinical data and indices of the training and validation datasets.

                Other parameters are described in detail below and in the source code.
        Parameters
        ----------
        vae_model: nn.Module
            The vae model to optimize. 
        dataset_training_state: data.DatasetTrainingState
            DatasetTrainingState for some ClinicalDataset 
        optimizationParameters : dict
            Dictionary containing optimzation parameters. Default: {'learningRate': 0.05,'maxEpochs': 5000,'numParticles':10}
        computeConfiguration : dict
            Dictionary containing the compute configuration (device and number of dataloaders. Defaults to using cpu: {'device':None,'numDataLoaders':0}
        **kwargs : See source code.
            These arguments adjust the Adam weight decay parameter ('AdamW_Weight_Decay') and the KL-Annealing scheduler ('KLAnnealingParams'). See source code for details.

        Returns
        -------
        None

        """



        allKeywordArgs = list(kwargs.keys())

        self.vae_model=vae_model
        self.dataset_training_state=dataset_training_state

        #general optimization parameters
        self.maxEpochs=optimizationParameters['maxEpochs']
        self.learningRate = optimizationParameters['learningRate']
        self.numParticles = optimizationParameters['numParticles']

        #compute resources parameters
        self.device=computeConfiguration['device']
        if self.device is None:
            self.device='cpu'

        else:
            try:
                device_type,device_num=self.device.split(':')
            except ValueError:
                device_type=self.device
                device_num='0'
                self.device=device_type+':'+device_num
            assert device_type in ['cuda','mps','cpu']," Only 'cuda','mps', and 'cpu' supported"
            if device_type=='mps':
                assert torch.backends.mps.is_available()==True,"mps device not available"
            if device_type=='cuda':
                assert torch.cuda.is_available()==True,"cuda device is not available"

        self.num_dataloaders=computeConfiguration['numDataLoaders']


        if 'AdamW_Weight_Decay' in allKeywordArgs:
            self.AdamW_Weight_Decay=kwargs['AdamW_Weight_Decay']
        else:
            self.AdamW_Weight_Decay=1e-4

        if 'KLAnnealingParams' not in allKeywordArgs:
            self.KLAnnealingParams = {'initialTemp':1.0,'maxTemp':1.0,'fractionalDuration':1.0,'schedule': 'cosine'}
        else:
            self.KLAnnealingParams=kwargs['KLAnnealingParams']
            assert set(self.KLAnnealingParams.keys())==set(['initialTemp','maxTemp','fractionalDuration','schedule']),"KL Annealing Parameters must be dictionary with the following keys: 'initialTemp','maxTemp','fractionalDuration','schedule'"




    def BatchTrain(self,batch_size:int,errorTol:float = 1e-3,verbose=True,logFile=None,errorComputationWindow=None,early_stop_patience=5,monitor_validation=True):
        """

        Trains the VAE model using the mini-batches. This is the recommended method.

        Parameters
        ----------
        batch_size : int
            Number of samples in each mini-batch
        errorTol : float
            Error tolerance in validation data ELBO for convergence.
        verbose : bool
            Whether to print updates regarding fitting.
        logFile : str
            Path to logfile which can store progress
        errorComputationWindow : int
            Sliding window for computing error tolerance. Default appears to work well.

        Returns
        -------
        tuple
            (bestModelScore, vector of ELBO evaluations on training data, vector of ELBO evaluations on validation data, vector of all errors computed during fitting)

        """
        if errorComputationWindow is None:
            errorComputationWindow = max(int(0.01*self.maxEpochs),2)
        else:
            assert errorComputationWindow>0, "Expects errorComputationWindow to be integer > 0"

        error_window = deque(maxlen=errorComputationWindow)
        elbo_window = deque(maxlen=errorComputationWindow)
        errorVec = []
        trainLoss = []
        validationLoss = []

        if self.dataset_training_state.training_index is not None:
            numTotalTrainingSamples=self.dataset_training_state.training_index.shape[0]
            numTotalValidationSamples=self.dataset_training_state.validation_index.shape[0]
        else:
            raise ValueError("Training state for data.DatasetTrainingState not set prior to calling optimizer. Please set training set using data.DatasetTrainingState.SetNewTrainingState") 

        assert batch_size < numTotalTrainingSamples, "Batch size is greater than or equal to training data size."

        if self.device.split(':')[0]!='cpu':
            self.vae_model.switch_device(self.device)

            

        torchTrainingData=TorchDataWrapper(self.dataset_training_state,batch_size,index='Training')
        torchValidationData=TorchDataWrapper(self.dataset_training_state,batch_size,index='Validation')


        sviFunction = SVI(self.vae_model.model,self.vae_model.guide,AdamW({'weight_decay':self.AdamW_Weight_Decay,'lr':self.learningRate}),loss=Trace_ELBO(num_particles=self.numParticles))

        annealer=AnnealingScheduler(self.KLAnnealingParams['initialTemp'],self.KLAnnealingParams['maxTemp'],int(len(torchTrainingData)*(self.maxEpochs*self.KLAnnealingParams['fractionalDuration'])),self.KLAnnealingParams['schedule'])

        paramUpdateNum=0

        #initialize model states and scores
        bestModelState=self.vae_model.package_state()

        #note, batch_size handled at the level of _TorchDatasetWrapper, not loader itself.
        trainingDataLoader = data.DataLoader(torchTrainingData,num_workers=self.num_dataloaders,collate_fn=collate_it)
        validationDataLoader = data.DataLoader(torchValidationData,num_workers=self.num_dataloaders,collate_fn=collate_it)

        avg_epoch_train_loss = 0.0
        self.vae_model.eval()
        for i,data_batch in enumerate(trainingDataLoader):
            if self.device.split(':')[0]!='cpu':
                data_batch=tuple([x.to(self.device) for x in data_batch])

            avg_epoch_train_loss+=sviFunction.evaluate_loss(*data_batch,minibatch_scale = (numTotalTrainingSamples/data_batch[0].shape[0]),annealing_factor=annealer.currentTemp(paramUpdateNum+1))
        avg_epoch_train_loss=avg_epoch_train_loss/(i+1)
        prev_train_loss=avg_epoch_train_loss


        avg_epoch_val_loss = 0.0
        for i,data_batch in enumerate(validationDataLoader):
            if self.device.split(':')[0]!='cpu':
                data_batch=tuple([x.to(self.device) for x in data_batch])

            avg_epoch_val_loss+=sviFunction.evaluate_loss(*data_batch,minibatch_scale = (numTotalValidationSamples/data_batch[0].shape[0]),annealing_factor=self.KLAnnealingParams['maxTemp'])
        avg_epoch_val_loss = avg_epoch_val_loss/(i+1)
        bestModelScore = np.inf

        elbo_window.append(prev_train_loss)

        early_stop_count=0
        for epoch in range(self.maxEpochs):
            torchTrainingData.shuffle_index()
            avg_epoch_train_loss = 0.0
            self.vae_model.train()
            for i,data_batch in enumerate(trainingDataLoader):
                paramUpdateNum+=1
                if self.device.split(':')[0]!='cpu':
                    data_batch=tuple([x.to(self.device) for x in data_batch])
                avg_epoch_train_loss+=sviFunction.step(*data_batch,minibatch_scale = (numTotalTrainingSamples/data_batch[0].shape[0]),annealing_factor=annealer.currentTemp(paramUpdateNum))
            avg_epoch_train_loss=avg_epoch_train_loss/(i+1.0)

            avg_epoch_val_loss = 0.0
            self.vae_model.eval()
            for i,data_batch in enumerate(validationDataLoader):
                if self.device.split(':')[0]!='cpu':
                    data_batch=tuple([x.to(self.device) for x in data_batch])
                avg_epoch_val_loss+=sviFunction.evaluate_loss(*data_batch,minibatch_scale = (numTotalValidationSamples/data_batch[0].shape[0]),annealing_factor=self.KLAnnealingParams['maxTemp'])
            avg_epoch_val_loss=avg_epoch_val_loss/(i+1.0)

            if np.isnan(avg_epoch_val_loss) or np.isnan(avg_epoch_train_loss):
                print("Warning: NaN detected during inference. Model unlikely to be fully optimized!")
                break

            if monitor_validation:
                if avg_epoch_val_loss<bestModelScore:
                    bestModelState = self.vae_model.package_state()
                    bestModelScore = avg_epoch_val_loss
                    early_stop_count=0
                else:
                    early_stop_count+=1 
            else:
                if avg_epoch_train_loss<bestModelScore:
                    bestModelState = self.vae_model.package_state()
                    bestModelScore = avg_epoch_train_loss
                    early_stop_count=0
                else:
                    early_stop_count+=1 


            #track overall convergence
            trainLoss+=[avg_epoch_train_loss]
            validationLoss+=[avg_epoch_val_loss]



            error_window.append(rel_diff(avg_epoch_train_loss,prev_train_loss))
            elbo_window.append(avg_epoch_train_loss)

            avg_error = sum(error_window)/len(error_window)
            med_error = sorted(error_window)[int(0.5*len(error_window))]
            slope_error = self._returnELBOSlopeError(elbo_window)

            prev_train_loss=avg_epoch_train_loss
            errorVec+=[min([avg_error,med_error,slope_error])]

            if early_stop_count>early_stop_patience:
                if verbose:
                    print("Model diverging after %03d epochs; stopping optimization. Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                if logFile!=None:
                    with open(logFile, "a") as f:
                        f.write("Model diverging after %03d epochs; stopping optimization. Current Loss (Train, Validation): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                break


            if (avg_error < errorTol) or (med_error < errorTol) or (slope_error<errorTol):


                if verbose:
                    print("Optimization converged in %03d epochs; Current Loss (Train, Test): %.4f, %.4f; Error: %.4e"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                if logFile!=None:
                    with open(logFile, "a") as f:
                        f.write("Optimization converged in %03d epochs; Current Loss (Train, Test): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                break

            else:
                if verbose:
                    print("Completed %03d epochs; Current Loss (Train, Test): %.4f, %.4f; Error: %.4e"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))
                if logFile!=None:
                    with open(logFile, "a") as f:
                        f.write("Completed %03d epochs; Current Loss (Train, Test): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))


        if epoch == (self.maxEpochs-1):
            f.write("Completed the maximum of %03d epochs; Final Loss (Train, Test): %.4f, %.4f; Error: %.4e\n"%(epoch+1,trainLoss[-1],validationLoss[-1],errorVec[-1]))


        self.vae_model.load_state(bestModelState)
        #set eval mode
        if self.device.split(':')[0]!='cpu':
            self.vae_model.switch_device('cpu')
        self.vae_model.eval()
        return bestModelScore,trainLoss,validationLoss,errorVec


