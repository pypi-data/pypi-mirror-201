import pandas as pd
import numpy as np
import torch
import pickle
import pyro
import copy

from cvae_model import DiseaseCondVAE
from basic_g2p import BasicG2PModel
from data import GeneToPhenotypeDataset
from optim import AutoEncoderOptimizer

__version__ = "0.0.1"


class VAE_G2P:

	def _readModelFromFile(self,fName):
		with open(fName,'rb') as f:
			model_dict = torch.load(f,map_location='cpu')
		return model_dict


	def __init__(self,diseaseGeneDataset,nLatentDim,isLinear=True,**kwargs):
		self.diseaseGeneDataset = diseaseGeneDataset
		self.nLatentDim=nLatentDim
		self.isLinear=isLinear
		self.numSymptoms=self.diseaseGeneDataset.num_symptoms
		self.numFreqCats=self.diseaseGeneDataset.num_ordinal_freqs

		self.all_model_kwargs = kwargs

		if 'encoder_hyperparameters' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['encoder_hyperparameters']={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True}
		if 'decoder_hyperparameters' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['decoder_hyperparameters']={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True}

		if 'missing_freq_priors' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['missing_freq_priors']=[0.0,3.0]

		if 'frequency_cut_points' not in self.all_model_kwargs.keys():
			self.all_model_kwargs['frequency_cut_points']=[0.04,0.3,0.8,0.99]

		assert (len(self.all_model_kwargs['frequency_cut_points'])+1)==self.diseaseGeneDataset.num_ordinal_freqs, "Number of model cutpoints must equal number frequency classes in dataset, excluding the Unknown class"

	
		self.basic_g2p=BasicG2PModel(self.diseaseGeneDataset,network_hyperparameters=self.all_model_kwargs['decoder_hyperparameters'],cut_points=self.all_model_kwargs['frequency_cut_points'])

		self.vae_g2p_model=DiseaseCondVAE(self.numSymptoms,self.numFreqCats,self.nLatentDim,self.basic_g2p,isLinear=self.isLinear,encoder_hyperparameters=self.all_model_kwargs['encoder_hyperparameters'],decoder_hyperparameters=self.all_model_kwargs['decoder_hyperparameters'],missing_freq_prior_mean=self.all_model_kwargs['missing_freq_priors'][0],missing_freq_prior_scale=self.all_model_kwargs['missing_freq_priors'][1],cut_points=self.all_model_kwargs['frequency_cut_points'])


	def Fit(self,batch_size,logFile=None,verbose=True,monitor_validation=True,prior_model_state=None,**kwargs):
		"""


		Parameters
		----------


		batch_size : int,
		    Size of dataset batches for inference. 

		verbose : bool, optional
		    Indicates whether or not to print (to std out) the loss function values and error after every epoch. The default is True.

		logFile: str, optional

		    File to log model fitting process.

		Keyword Parameters
		----------
		learningRate: float, optional
		    Specifies the maximum learning rate used during inference. Default is 0.05

		errorTol: float, optional
		    Error tolerance in ELBO (computed on held out validation data) to determine convergence. Default is 1e-4.

		numParticles: int, optional
		    Number of particles (ie random samples) used to approximate gradient. Default is 1. Computational cost increases linearly with value.

		maxEpochs: int, optional
		    Maximum number of epochs (passes through training data) for inference. Note, because annealing and learning rate updates depend on maxEpochs, this offers a simple way to adjust the speed at which these values change. Default is 200.

		computeDevice: str or None, optional
		    Specifies compute device for inference. Default is None, which instructs algorithm to use cpu. Two other options are supported: 'cuda' and 'mps'. Note, if device number is not included (ex: 'cuda:0'), then it is automatically assumed to be '0'

		numDataLoaders: int
		    Specifies the number of threads used to process data and prepare for upload into the gpu. Note, due to the speed of gpu, inference can become limited by data transfer speed, hence the use of multiple DataLoaders to improve this bottleneck. Default is 0, meaning just the dedicated cpu performs data transfer.

		KLAnnealingParams: dict with keys 'initialTemp','maxTemp','fractionalDuration','schedule'
		    Parameters that define KL-Annealing strategy used during inference, important for avoiding local optima. Note, annealing is only used for computation of ELBO and gradients on training data. Validation data ELBO evaluation, used to monitor convergence, is performed at the maximum desired temperature (typically 1.0, equivalent to standard variational inference). Therefore, it is possible for the model to converge even when the temperature hasn't reached it's final value. It's also possible that further cooling would find a better optimum, but this is highly unlikely in practice.
		    initialTemp--initial temperature during inference. Default: 1.0 (no annealing)
		    maxTemp--final temperature obtained during inference. Default: 1.0 (standard variational inference)
		    fractionalDuration--fraction of inference epochs used for annealing. Default is 0.25
		    schedule--function used to change temperature during inference. Defualt is 'cosine'. Options: 'cosine','linear'



		Returns
		-------
		output : list
		    List containing the following information: [loss function value of best model (computed on validation data),sequence of training loss values, sequence of validation loss values, error estimates across iterations (computed on validation data)].



		"""


		######### Parse Keyword Arguments #########
		allKeywordArgs = list(kwargs.keys())


		if 'learningRate' in allKeywordArgs:
		    learningRate=kwargs['learningRate']
		else:
		    learningRate=0.01


		if 'errorTol' in allKeywordArgs:
		    errorTol=kwargs['errorTol']
		else:
		    errorTol=1e-4

		if 'numParticles' in allKeywordArgs:
		    numParticles=kwargs['numParticles']
		else:
		    numParticles=1


		if 'maxEpochs' in allKeywordArgs:
		    maxEpochs=kwargs['maxEpochs']
		else:
		    maxEpochs=500


		if 'computeDevice' in allKeywordArgs:
		    computeDevice=kwargs['computeDevice']
		else:
		    computeDevice=None

		if 'numDataLoaders' in allKeywordArgs:
		    numDataLoaders=kwargs['numDataLoaders']
		    if computeDevice in [None,'cpu']:
		        assert numDataLoaders==0,"Specifying number of dataloaders other than 0 only relevant when using GPU computing"
		else:
		    numDataLoaders=0

		if 'KLAnnealingParams' in allKeywordArgs:
		    KLAnnealingParams=kwargs['KLAnnealingParams']
		    assert set(KLAnnealingParams.keys())==set(['initialTemp','maxTemp','fractionalDuration','schedule']),"KL Annealing Parameters must be dictionary with the following keys: 'initialTemp','maxTemp','fractionalDuration','schedule'"
		else:
		    KLAnnealingParams={'initialTemp':1.0,'maxTemp':1.0,'fractionalDuration':1.0,'schedule': 'cosine'}


		if 'EarlyStopPatience' in allKeywordArgs:
			EarlyStopPatience=kwargs['EarlyStopPatience']
		else:
			EarlyStopPatience=10


		pyro.clear_param_store()
		if prior_model_state is None:
			self.basic_g2p.Fit(batch_size,learningRate,maxEpochs,errorTol,compute_device=computeDevice,numDataLoaders=numDataLoaders,early_stop_patience=EarlyStopPatience,monitor_validation=False)
		else:
			self.basic_g2p.LoadModel(prior_model_state)


		optimizer=AutoEncoderOptimizer(self.vae_g2p_model,self.diseaseGeneDataset,optimizationParameters={'learningRate': learningRate,'maxEpochs': maxEpochs,'numParticles':numParticles},computeConfiguration={'device':computeDevice,'numDataLoaders':numDataLoaders},KLAnnealingParams=KLAnnealingParams)
		output=optimizer.BatchTrain(batch_size,errorTol=errorTol,verbose=verbose,logFile=logFile,monitor_validation=monitor_validation,early_stop_patience=EarlyStopPatience)
		return output

	def PredictEmbedFromGeneOnly(self,gene_list,returnStdErrors=False):
		assert len(set(gene_list).difference(self.diseaseGeneDataset.gene_map.keys()))==0,"The following genes are not in the embedding table: {0:s}".format(','.join(list(set(gene_vec).difference(self.diseaseGeneDataset.gene_map.keys()))))

		gene_data=self.diseaseGeneDataset.ReturnGeneDataArrays(gene_list)
		modes_for_prior = torch.cat(self.vae_g2p_model.baseline_g2p_model.basic_net(gene_data),axis=1)
		z_loc,z_scale = self.vae_g2p_model.prior_model(torch.cat((modes_for_prior,gene_data),axis=1))
		if returnStdErrors:
			return z_loc.detach().numpy(),z_scale.detach().numpy()
		else:
			return z_loc.detach().numpy()

	def PredictSymptomsFromGeneOnly(self,gene_list,numSamples=0):
		z_loc,z_scale=self.PredictEmbedFromGeneOnly(gene_list,returnStdErrors=True)

		if numSamples==0:
			symptom_probs=torch.sigmoid(self.vae_g2p_model.symptom_annotation_decoder.forward(torch.tensor(z_loc))).detach().numpy()

			symptom_freqs=torch.exp(pyro.distributions.OrderedLogistic(self.vae_g2p_model.symptom_frequency_decoder(torch.tensor(z_loc)),self.vae_g2p_model.cut_points).logits).detach().numpy()
		else:
			samples_from_priors = torch.normal(torch.tensor(z_loc)*torch.ones((numSamples,z_loc.shape[0],z_loc.shape[1])),torch.tensor(z_scale)*torch.ones((numSamples,z_loc.shape[0],z_loc.shape[1])))

			symptom_probs=np.zeros((len(gene_list),self.numSymptoms))
			symptom_freqs=np.zeros((len(gene_list),self.numSymptoms,self.numFreqCats))

			for i in range(numSamples):
				symptom_probs+=torch.sigmoid(self.vae_g2p_model.symptom_annotation_decoder.forward(samples_from_priors[i])).detach().numpy()/numSamples
				symptom_freqs+=torch.exp(pyro.distributions.OrderedLogistic(self.vae_g2p_model.symptom_frequency_decoder(samples_from_priors[i]),self.vae_g2p_model.cut_points).logits).detach().numpy()/numSamples

		output_table=pd.DataFrame([],index=self.diseaseGeneDataset.symptom_map.keys(),columns=gene_list)
		for i,gene in enumerate(gene_list):
			output_table[gene]=list(zip(symptom_probs[i],symptom_freqs[i]))
		return output_table

	

	def PerDatumELBO(self,hpo_freq_pairs,gene_list,num_particles=10):
		assert isinstance(hpo_freq_pairs,list),"The provided HPO-frequncy pairs must be an interable of ('HPO Symptom','Frequency') nested within a list."

		assert isinstance(gene_list,list),"Conditional VAE model expects a list of genes in order to compute ELBO"
		assert len(hpo_freq_pairs)==len(gene_list) or (len(hpo_freq_pairs)==1 or len(gene_list)==1),"Number of provided symptom-frequency pair datasets must equal number of genes, unless number of genes or the number of symptom-frequency pair datasets is equal to 1, at which point the data type with length 1 is broadcasted to the same size as the other dataset."

		#generate data tensors, allows broadcasting 
		annot_array=torch.zeros((max(len(hpo_freq_pairs),len(gene_list)),self.numSymptoms),dtype=torch.float32)
		freq_array=torch.zeros((max(len(hpo_freq_pairs),len(gene_list)),self.numSymptoms),dtype=torch.float32)

		if len(gene_list)<len(hpo_freq_pairs):
			gene_list=gene_list*len(hpo_freq_pairs)
		elif len(gene_list)>len(hpo_freq_pairs):
			hpo_freq_pairs=hpo_freq_pairs*len(gene_list)

		for t,hpo_freq_vec in enumerate(hpo_freq_pairs):
			idx_vec=[self.diseaseGeneDataset.symptom_map[x[0]] for x in hpo_freq_vec]
			freq_vec=[self.diseaseGeneDataset.ordinal_freq_map[x[1]] for x in hpo_freq_vec]
			annot_array[t,idx_vec]=1.0
			freq_array[t,idx_vec]=torch.tensor(freq_vec,dtype=torch.float32)

		data=(annot_array,freq_array,self.diseaseGeneDataset.ReturnGeneDataArrays(gene_list))

		elbo=self.vae_g2p_model.per_datum_ELBO(*data,num_particles=num_particles)
		return elbo.detach().numpy().ravel()

	def PerplexCompare(self,hpo_freq_pairs,gene_list,num_particles=10,index=None):
		perplex_vec = -1.0*self.PerDatumELBO(hpo_freq_pairs,gene_list)
		model_compare_results=self.basic_g2p.PerplexCompareNull(hpo_freq_pairs,gene_list)
		model_compare_results['VAE_G2P Perplex.']=perplex_vec
		model_compare_results['VAE_G2P-BasicG2PModel']=model_compare_results['VAE_G2P Perplex.']-model_compare_results['BasicG2PModel Perplex.']
		model_compare_results['VAE_G2P-Null']=model_compare_results['VAE_G2P Perplex.']-model_compare_results['Null Perplex.']
		model_compare_results['Genes']=gene_list
		model_compare_results=pd.DataFrame(model_compare_results)
		if index is not None:
			model_compare_results['Index']=index
			model_compare_results.set_index('Index',inplace=True)
		else:
			model_compare_results.set_index('Genes',inplace=True)
		return model_compare_results


	def EmbedDisease(self,hpo_freq_pairs,gene_list=None,returnStdErrors=False):
		assert isinstance(hpo_freq_pairs,list),"The provided HPO-frequncy pairs must be an interable of ('HPO Symptom','Frequenc') nested within a list."
		assert isinstance(gene_list,list),"Conditional VAE model expects a list of genes in order to compute ELBO"
		assert len(hpo_freq_pairs)==len(gene_list) or (len(hpo_freq_pairs)==1 or len(gene_list)==1),"Number of provided symptom-frequency pair datasets must equal number of genes, unless number of genes or the number of symptom-frequency pair datasets is equal to 1, at which point the data type with length 1 is broadcasted to the same size as the other dataset."

		#generate data tensors, allows broadcasting 
		annot_array=torch.zeros((max(len(hpo_freq_pairs),len(gene_list)),self.numSymptoms),dtype=torch.float32)
		freq_array=torch.zeros((max(len(hpo_freq_pairs),len(gene_list)),self.numSymptoms),dtype=torch.float32)

		if len(gene_list)<len(hpo_freq_pairs):
			gene_list=gene_list*len(hpo_freq_pairs)
		elif len(gene_list)>len(hpo_freq_pairs):
			hpo_freq_pairs=hpo_freq_pairs*len(gene_list)

		for t,hpo_freq_vec in enumerate(hpo_freq_pairs):
			idx_vec=[self.diseaseGeneDataset.symptom_map[x[0]] for x in hpo_freq_vec]
			freq_vec=[self.diseaseGeneDataset.ordinal_freq_map[x[1]] for x in hpo_freq_vec]
			annot_array[t,idx_vec]=1.0
			freq_array[t,idx_vec]=torch.tensor(freq_vec,dtype=torch.float32)

		data=(annot_array,freq_array,self.diseaseGeneDataset.ReturnGeneDataArrays(gene_list))
		p_m,p_std=self.vae_g2p_model.posterior_latent_state(*data)
		if returnStdErrors:
			return p_m.detach().numpy(),p_std.detach().numpy()
		else:
			return p_m.detach().numpy()


	def EstimateMissingAnnotationRates(self,hpo_freq_pairs,gene_list):
		assert len(hpo_freq_pairs)==len(gene_list),"Expect length of HPO-Freqency Pair sets and gene lists to be the same."
		mapping_dict={}
		for i,hpo_freq_vec in enumerate(hpo_freq_pairs):
			mapping_dict[gene_list[i]]=torch.tensor([self.diseaseGeneDataset.symptom_map[x[0]] for x in hpo_freq_vec],dtype=torch.long)

		post_mean=self.EmbedDisease(hpo_freq_pairs,gene_list=gene_list,returnStdErrors=False)

		output_dictionary={}
		for i,post_vec in enumerate(post_mean):
			embed_tensor=torch.tensor(post_vec,dtype=torch.float32)
			pred_missing_full=self.vae_g2p_model.missing_freq_disease_decoder(embed_tensor)+self.vae_g2p_model.missing_freq_intercepts_post_mean
			pred_missing=torch.sigmoid(pred_missing_full[mapping_dict[gene_list[i]]]).detach().numpy()
			output_dictionary[gene_list[i]]=list(zip([self.diseaseGeneDataset.inverse_symptom_map[x] for x in mapping_dict[gene_list[i]].detach().numpy()],pred_missing))
		return output_dictionary


	def ImputeMissingSymptomFrequencies(self,hpo_freq_pairs,gene_list):
		assert len(hpo_freq_pairs)==len(gene_list),"Expect length of HPO-Freqency Pair sets and gene lists to be the same."
		mapping_dict={}
		for i,hpo_freq_vec in enumerate(hpo_freq_pairs):
			mapping_dict[gene_list[i]]=torch.tensor([self.diseaseGeneDataset.symptom_map[x[0]] for x in hpo_freq_vec if x[1]==self.diseaseGeneDataset.missing_label],dtype=torch.long)

		post_mean=self.EmbedDisease(hpo_freq_pairs,gene_list,returnStdErrors=False)


		output_dictionary={}
		for i,post_vec in enumerate(post_mean):
			embed_tensor=torch.tensor(post_vec,dtype=torch.float32)
			pred_class_full=pyro.distributions.OrderedLogistic(self.vae_g2p_model.symptom_frequency_decoder(embed_tensor.unsqueeze(dim=0)),self.vae_g2p_model.cut_points).logits.squeeze(dim=0)
			pred_annots=torch.exp(pred_class_full[mapping_dict[gene_list[i]],:]).detach().numpy()
			output_dictionary[gene_list[i]]=list(zip([self.diseaseGeneDataset.inverse_symptom_map[x] for x in mapping_dict[gene_list[i]].detach().numpy()],pred_annots))

		return output_dictionary

	def SuggestNewSymptoms(self,hpo_freq_pairs,gene_list,annot_rate_threshold=0.0):
		assert len(hpo_freq_pairs)==len(gene_list),"Expect length of HPO-Freqency Pair sets and gene lists to be the same."

		mapping_dict={}
		for i,hpo_freq_vec in enumerate(hpo_freq_pairs):
			mapping_dict[gene_list[i]]=set([x[0] for x in hpo_freq_vec])

		post_mean=self.EmbedDisease(hpo_freq_pairs,gene_list,returnStdErrors=False)

		output_dictionary={}
		for i,post_vec in enumerate(post_mean):
			embed_tensor=torch.tensor(post_vec,dtype=torch.float32)
			pred_symptoms=torch.sigmoid(self.vae_g2p_model.symptom_annotation_decoder(embed_tensor.unsqueeze(dim=0)).squeeze(dim=0)).detach().numpy()
			pred_class_full=pyro.distributions.OrderedLogistic(self.vae_g2p_model.symptom_frequency_decoder(embed_tensor.unsqueeze(dim=0)),self.vae_g2p_model.cut_points).logits.squeeze(dim=0)
			pred_class_full=torch.exp(pred_class_full).detach().numpy()

			allowed_symptoms=np.arange(self.numSymptoms)
			allowed_symptoms=allowed_symptoms[pred_symptoms>=annot_rate_threshold]
			pred_class_full=pred_class_full[pred_symptoms>=annot_rate_threshold]
			pred_symptoms=pred_symptoms[pred_symptoms>=annot_rate_threshold]

			
			allowed_symptoms=allowed_symptoms[np.argsort(pred_symptoms)[::-1]]
			pred_class_full=pred_class_full[np.argsort(pred_symptoms)[::-1]]
			pred_symptoms=np.sort(pred_symptoms)[::-1]
			output_vec=[]
			for j in range(allowed_symptoms.shape[0]):
				symptom=self.diseaseGeneDataset.inverse_symptom_map[allowed_symptoms[j]]
				if symptom not in mapping_dict[gene_list[i]]:
					output_vec+=[(symptom,pred_symptoms[j],pred_class_full[j])]
			output_dictionary[gene_list[i]]=output_vec
		return output_dictionary




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
			stored_model = self._readModelFromFile(stored_model)

		assert set(stored_model.keys())==set(['model_state','meta_data','variational_post_params','baseline_g2p_model']),"Model dictionary must contain the following elements: 'model_state','meta_data','baseline_g2p_model'"
		self.basic_g2p=BasicG2PModel(self.diseaseGeneDataset,network_hyperparameters=stored_model['meta_data']['all_model_kwargs']['decoder_hyperparameters'],cut_points=stored_model['meta_data']['all_model_kwargs']['frequency_cut_points'])
		self.vae_g2p_model=DiseaseCondVAE(
			stored_model['meta_data']['numSymptoms'],
			stored_model['meta_data']['numFreqCats'],
			stored_model['meta_data']['nLatentDim'],
			self.basic_g2p,
			isLinear=stored_model['meta_data']['isLinear'],
			encoder_hyperparameters=stored_model['meta_data']['all_model_kwargs']['encoder_hyperparameters'],
			decoder_hyperparameters=stored_model['meta_data']['all_model_kwargs']['decoder_hyperparameters'],
			missing_freq_prior_mean=stored_model['meta_data']['all_model_kwargs']['missing_freq_priors'][0],
			missing_freq_prior_scale=stored_model['meta_data']['all_model_kwargs']['missing_freq_priors'][1],
			cut_points=stored_model['meta_data']['all_model_kwargs']['frequency_cut_points']
			)
		self.vae_g2p_model.load_state(stored_model)
	


	def SaveModel(self,fName=None):
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
		model_dict = self.vae_g2p_model.package_state()
		model_dict['meta_data']={}
		model_dict['meta_data']['numSymptoms']=self.numSymptoms
		model_dict['meta_data']['numFreqCats']=self.numFreqCats
		model_dict['meta_data']['nLatentDim']=self.nLatentDim
		model_dict['meta_data']['isLinear']=self.isLinear
		model_dict['meta_data']['all_model_kwargs']=self.all_model_kwargs
		if fName is not None:
		    with open(fName,'wb') as f:
		        torch.save(model_dict,f)
		return model_dict

