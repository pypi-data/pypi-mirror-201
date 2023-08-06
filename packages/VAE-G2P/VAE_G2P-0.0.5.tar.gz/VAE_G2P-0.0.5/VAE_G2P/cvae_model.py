import torch
from torch import nn
import pyro
import pyro.distributions as dist
import copy
from pyro.infer import Trace_ELBO

from .networks import FC_MeanScaleEncoder,FC_Decoder,Linear_Decoder

class DiseaseCondVAE(nn.Module):

	def __init__(self,
		num_symptoms,
		n_freq_classes,
		n_latent_dim,
		baseline_g2p_model,
		isLinear=True,
		encoder_hyperparameters={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True},
		decoder_hyperparameters={'n_layers' : 2, 'n_hidden' : 64, 'dropout_rate': 0.1, 'use_batch_norm':True},
		missing_freq_prior_mean=0.0,
		missing_freq_prior_scale=3.0,
		cut_points = [0.04,0.3,0.8,0.99]
		):    

		super(DiseaseCondVAE,self).__init__()
		self.num_symptoms=num_symptoms
		self.n_latent_dim=n_latent_dim
		self.n_freq_classes=n_freq_classes
		self.baseline_g2p_model=baseline_g2p_model


		#encoder receives the following information: annotated symptoms, whether frequency is present or missing, and the assigned frequency. This information can be encoded using self.num_dx (annotation present)+self.num_dx (frequency present vs missing)+ self.num_dx*(self.n_freq_classes) (using one-hot endoding)
		self.encoder=FC_MeanScaleEncoder((self.n_freq_classes+2)*self.num_symptoms+self.baseline_g2p_model.g2p_dataset.aux_gene_info_table['return_dim'].sum(),n_latent_dim,**encoder_hyperparameters)
		self.prior_model=FC_MeanScaleEncoder(3*self.num_symptoms+self.baseline_g2p_model.g2p_dataset.aux_gene_info_table['return_dim'].sum(),n_latent_dim,**encoder_hyperparameters)

		self.isLinear=isLinear

		if self.isLinear:
			self.symptom_annotation_decoder=Linear_Decoder(n_latent_dim,self.num_symptoms)
			self.symptom_frequency_decoder=Linear_Decoder(n_latent_dim,self.num_symptoms)
		else:
			self.symptom_annotation_decoder=FC_Decoder(self.n_latent_dim,self.num_symptoms,**decoder_hyperparameters)
			self.symptom_frequency_decoder=FC_Decoder(self.n_latent_dim,self.num_symptoms,**decoder_hyperparameters)

		self.missing_freq_disease_decoder=nn.Linear(self.n_latent_dim,1,bias=True)

		self.missing_freq_prior_scale=torch.tensor(missing_freq_prior_scale,dtype=torch.float32)
		self.missing_freq_prior_mean=torch.tensor(missing_freq_prior_mean,dtype=torch.float32)

		self.cut_points=torch.logit(torch.tensor(cut_points,dtype=torch.float32))

		assert (len(self.cut_points)+1)==self.n_freq_classes, "Number of cut points+1 must equal number of frequency classes"

		self.missing_freq_intercepts=torch.zeros(self.num_symptoms,dtype=torch.float32)

		self.missing_freq_intercepts_post_mean=torch.zeros(self.num_symptoms,dtype=torch.float32)
		self.missing_freq_intercepts_post_log_scale=torch.zeros(self.num_symptoms,dtype=torch.float32)

		
		self.compute_device='cpu'
		self.eval()

	def model(self,annot_data=None,freq_data=None,gene_data=None,num_samples=None,minibatch_scale=1.0, annealing_factor=1.0):
		if annot_data is not None:
			num_samples=annot_data.shape[0]
		else:
			if num_samples is None:
				num_samples=1000
				print('Warning: no arguments were given to DiseaseVAE.model. This should only be done during debugging.')
		if freq_data is not None:
			assert (freq_data.shape[0]==num_samples)&(freq_data.shape[1]==self.num_symptoms), "Frequency annotation data dimensions do not match number of samples/symptoms"

			freq_missing=torch.zeros(freq_data.shape,dtype=torch.float32,device=self.compute_device)
			freq_missing[(freq_data==-1.0)]=1.0

			freq_missing_mask = torch.zeros(freq_data.shape,dtype=torch.bool,device=self.compute_device)
			freq_obs_mask = torch.zeros(freq_data.shape,dtype=torch.bool,device=self.compute_device)
			freq_missing_mask[annot_data==1]=1.0
			freq_obs_mask[(annot_data==1)&(freq_data!=-1)]=1.0

			transformed_freq_data=freq_data.detach().clone().long()
			transformed_freq_data[(annot_data==1.0)&(freq_data==-1.0)]=0.0
		else:
			freq_missing=None
			freq_missing_mask=None
			freq_obs_mask=None
			transformed_freq_data=None



		pyro.module("symptom_annotation_decoder", self.symptom_annotation_decoder)
		pyro.module("symptom_frequency_decoder", self.symptom_frequency_decoder)
		pyro.module("missing_freq_disease_decoder", self.missing_freq_disease_decoder)
		pyro.module("prior_model",self.prior_model)

		with torch.no_grad():
			self.missing_freq_prior_scale=self.missing_freq_prior_scale.detach().to(self.compute_device)
			self.missing_freq_prior_mean=self.missing_freq_prior_mean.detach().to(self.compute_device)
			self.cut_points=self.cut_points.detach().to(self.compute_device)

		self.missing_freq_intercepts=pyro.sample("missing_freq_intercepts", dist.Normal(torch.zeros(self.num_symptoms,dtype=torch.float32,device=self.compute_device)+self.missing_freq_prior_mean, torch.ones(self.num_symptoms,dtype=torch.float32,device=self.compute_device)*self.missing_freq_prior_scale).to_event(1))


		with pyro.poutine.scale(None,minibatch_scale):

			with pyro.plate("data",size=num_samples,dim=-2):
				with torch.no_grad():
					gene_pred= self.baseline_g2p_model.basic_net.forward(gene_data)
					gene_pred=torch.cat(gene_pred,axis=1)
				z_loc,z_scale = self.prior_model(torch.cat((gene_pred,gene_data),axis=1))
				with pyro.poutine.scale(None, annealing_factor):
					latent_variables=pyro.sample("latent_variables",dist.Normal(z_loc,z_scale))


				annotation_pred = self.symptom_annotation_decoder.forward(latent_variables)
				annotation_outcomes = pyro.sample("annotation_outcomes",dist.Bernoulli(logits=annotation_pred),obs=annot_data)


				if freq_missing_mask is None:
					freq_missing_mask = torch.zeros(annotation_outcomes.shape,dtype=torch.bool,device=self.compute_device)
					freq_missing_mask[annotation_outcomes==1]=1

				with pyro.plate("freq_annots",size=self.num_symptoms,dim=-1):

					with pyro.poutine.mask(mask=freq_missing_mask):
						missing_pred = self.missing_freq_disease_decoder.forward(latent_variables)+self.missing_freq_intercepts
						missing_outcomes = pyro.sample("missing_outcomes",dist.Bernoulli(logits=missing_pred),obs=freq_missing)

					if freq_obs_mask is None:
						freq_obs_mask = torch.zeros(annotation_outcomes.shape,dtype=torch.bool,device=self.compute_device)
						freq_obs_mask[(annotation_outcomes==1)&(missing_outcomes!=-1)]=1

					with pyro.poutine.mask(mask=freq_obs_mask):
						frequency_predictions=self.symptom_frequency_decoder.forward(latent_variables)
						frequency_outcomes=pyro.sample("frequency_outcomes",dist.OrderedLogistic(frequency_predictions,self.cut_points),obs=transformed_freq_data)


		freq_data_output=torch.zeros(annotation_outcomes.shape,dtype=torch.long,device=self.compute_device)
		freq_data_output[(annotation_outcomes==1)]=frequency_outcomes[(annotation_outcomes==1)]
		freq_data_output[(annotation_outcomes==1)&(missing_outcomes==1)]=-1.0

		return annotation_outcomes,freq_data_output

	def guide(self,annot_data=None,freq_data=None,gene_data=None,num_samples=None,minibatch_scale=1.0, annealing_factor=1.0):
		if annot_data is not None:
			num_samples=annot_data.shape[0]
		else:
			if num_samples is None:
				num_samples=1000
				print('Warning: no arguments were given to ClinicalDxVAE.model. This should only be done during debugging.')


		if freq_data is not None:

			assert (freq_data.shape[0]==num_samples)& (freq_data.shape[1]==self.num_symptoms), "Frequency annotation data dimensions do not match number of samples/symptoms"
			freq_missing=torch.zeros(freq_data.shape,dtype=torch.float32,device=self.compute_device)
			freq_missing[(freq_data==-1.0)]=1.0

			freq_missing_mask = torch.zeros(freq_data.shape,dtype=torch.bool,device=self.compute_device)
			freq_obs_mask = torch.zeros(freq_data.shape,dtype=torch.bool,device=self.compute_device)
			freq_missing_mask[annot_data==1]=1.0
			freq_obs_mask[(annot_data==1)&(freq_data!=-1)]=1.0
		else:
			freq_missing_mask=torch.ones(annot_data.shape,dtype=torch.bool,device=self.compute_device)
			freq_obs_mask=torch.ones(annot_data.shape,dtype=torch.bool,device=self.compute_device)


		pyro.module("encoder", self.encoder)

		self.missing_freq_intercepts_post_mean = pyro.param('missing_freq_intercepts_post_mean', torch.zeros(self.num_symptoms,dtype=torch.float32,device=self.compute_device))
		self.missing_freq_intercepts_post_log_scale = pyro.param('missing_freq_intercepts_post_log_scale', torch.zeros(self.num_symptoms,dtype=torch.float32,device=self.compute_device))

		self.missing_freq_intercepts=pyro.sample("missing_freq_intercepts",dist.Normal(self.missing_freq_intercepts_post_mean,torch.exp(self.missing_freq_intercepts_post_log_scale)).to_event(1))

		with pyro.poutine.scale(None,minibatch_scale):
			#unroll the data
			missing_freqs=torch.zeros(annot_data.shape,dtype=torch.float32,device=self.compute_device)
			missing_freqs[freq_data==-1]=1.0

			#assign unnannotated and missing data to an unobserved class
			transformed_freq_data=freq_data.detach().clone().long()

			transformed_freq_data[freq_data==-1]=len(self.cut_points)+1
			transformed_freq_data[(annot_data==0)]=len(self.cut_points)+1

			unrolled_freq_classes = torch.nn.functional.one_hot(transformed_freq_data)

			input_data=torch.cat([annot_data,missing_freqs,unrolled_freq_classes[:,:,:-1].flatten(start_dim=1),gene_data],axis=1)
			z_mean,z_std = self.encoder.forward(input_data)
			with pyro.poutine.scale(None, annealing_factor):
				with pyro.plate("data",size=num_samples,dim=-2):
					pyro.sample("latent_variables", dist.Normal(z_mean, z_std))

	def posterior_latent_state(self,annot_data,freq_data,gene_data):
		if self.training:
			self.eval()
			in_training=True
		else:
			in_training=False

		missing_freqs=torch.zeros(annot_data.shape,dtype=torch.float32,device=self.compute_device)
		missing_freqs[freq_data==-1]=1.0

		#assign unnannotated and missing data to an unobserved class
		transformed_freq_data=freq_data.detach().clone().long()

		transformed_freq_data[freq_data==-1]=len(self.cut_points)+1
		transformed_freq_data[(annot_data==0)]=len(self.cut_points)+1

		unrolled_freq_classes = torch.nn.functional.one_hot(transformed_freq_data)

		input_data=torch.cat([annot_data,missing_freqs,unrolled_freq_classes[:,:,:-1].flatten(start_dim=1),gene_data],axis=1)


		p_mean,p_std=self.encoder.forward(input_data)
		if in_training:
			self.train()

		return p_mean.detach(),p_std.detach()

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
		packaged_model_state['baseline_g2p_model'] = copy.deepcopy(self.baseline_g2p_model.basic_net.state_dict(keep_vars=True))
		packaged_model_state['variational_post_params']={}
		packaged_model_state['variational_post_params']['missing_freq_intercepts_post_mean']=self.missing_freq_intercepts_post_mean.detach()
		packaged_model_state['variational_post_params']['missing_freq_intercepts_post_log_scale']=self.missing_freq_intercepts_post_log_scale.detach()
		
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
		self.baseline_g2p_model.basic_net.load_state_dict(prior_model_state['baseline_g2p_model'],strict=True)
		self.missing_freq_intercepts_post_mean=prior_model_state['variational_post_params']['missing_freq_intercepts_post_mean']
		self.missing_freq_intercepts_post_log_scale=prior_model_state['variational_post_params']['missing_freq_intercepts_post_log_scale']

	def switch_device(self, new_compute_device):
		"""Sw

		Parameters
		----------
		compute_device : str
		    String name for compute device. Ideally expressed as 'type:number'
		"""
		self.compute_device=new_compute_device
		self.to(self.compute_device)
		self.missing_freq_intercepts_post_mean.to(self.compute_device)
		self.missing_freq_intercepts_post_log_scale.to(self.compute_device)
		self.baseline_g2p_model.basic_net.to(self.compute_device)

	def per_datum_ELBO(self,annot_data,freq_data,gene_data,num_particles=10,prior_only=False):
		""" Computes the evidence lower bound (ELBO) for each observation in the dataset.

		Parameters
		----------
		obs_data : torch.tensor
		    Binary array of observed data.
		num_particles : int
		    Number of particles (samples) used to approximate the ELBOs

		Returns
		-------
		torch.tensor
		    Per-datum ELBOs

		"""
		if self.training:
		    self.eval()
		    in_training=True
		else:
		    in_training=False

		elboFunc = Trace_ELBO(num_particles=num_particles)
		elboVec = torch.zeros(annot_data.shape[0],dtype=torch.float32,device=self.compute_device)

		for model_trace, guide_trace in elboFunc._get_traces(self.model, self.guide,(annot_data,freq_data,gene_data,),{}):
		    elboVec+=model_trace.nodes['annotation_outcomes']['log_prob'].detach().sum(axis=1)/num_particles
		    elboVec+=model_trace.nodes['missing_outcomes']['log_prob'].detach().sum(axis=1)/num_particles
		    elboVec+=model_trace.nodes['frequency_outcomes']['log_prob'].detach().sum(axis=1)/num_particles
		    elboVec+=model_trace.nodes['latent_variables']['log_prob'].detach().sum(axis=1)/num_particles
		    elboVec-=guide_trace.nodes['latent_variables']['log_prob'].detach().sum(axis=1)/num_particles

		if in_training:
		    self.train()
		return elboVec.reshape(elboVec.shape[0],1)
