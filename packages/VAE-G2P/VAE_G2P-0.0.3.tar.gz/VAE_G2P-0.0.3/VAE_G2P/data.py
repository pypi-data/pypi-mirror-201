import pandas as pd
import numpy as np
import torch
from scipy import sparse
import itertools
import pickle
from collections.abc import Iterable

class GeneToPhenotypeDataset:

	def _process_gene_table(self):

		#possible dtypes = [float_array,one_hot_cat,sparse_binary,float]
		self.aux_gene_info_table=pd.DataFrame([],index=self.gene_info_table.columns,columns=['dtype','idx_map','inv_idx_map','return_dim'])
		for col in self.gene_info_table.columns:
			has_iterables = self.gene_info_table[col].apply(lambda x:isinstance(x,Iterable))
			has_strings = self.gene_info_table[col].apply(lambda x:isinstance(x,str))
			has_floats = self.gene_info_table[col].apply(lambda x:isinstance(x,float))
			if (has_iterables.sum()>0) and (has_strings.sum()==0):
				assert has_iterables.sum()==self.gene_info_table.shape[0], "Mixed iterables and other data types in gene_info_table columns is not allowed."
				#check length, if all the same, then must be float array. Otherwise, assume sparse-binary array
				iterable_lengths = self.gene_info_table[col].apply(lambda x:len(x))
				if np.unique(iterable_lengths.values).shape[0]==1:
					assert self.gene_info_table[col].apply(lambda lst: all((isinstance(x, float) for x in lst))).sum()==self.gene_info_table.shape[0], "If all entries in data column are the same length, only float entries are allowed. Arrays of ints should be re-coded as categorical variables."
					self.aux_gene_info_table.loc[col,'dtype']='float_array'
					self.aux_gene_info_table.loc[col]['idx_map']='NA'
					self.aux_gene_info_table.loc[col]['inv_idx_map']='NA'
					self.aux_gene_info_table.loc[col,'return_dim']=np.unique(iterable_lengths.values)[0]
				else:
					all_unique=sorted(list(set().union(*self.gene_info_table[col])))
					idx_map=dict(zip(all_unique,list(range(len(all_unique)))))
					self.aux_gene_info_table.loc[col,'dtype']='sparse_binary'
					self.aux_gene_info_table.loc[col]['idx_map']=idx_map
					self.aux_gene_info_table.loc[col]['inv_idx_map']=dict(zip(idx_map.values(),idx_map.keys()))
					self.gene_info_table[col]=self.gene_info_table[col].apply(lambda x: [idx_map[y] for y in x])
					self.aux_gene_info_table.loc[col,'return_dim']=len(idx_map)

			else:
				assert (has_strings.sum()==self.gene_info_table.shape[0]) or (has_floats.sum()==self.gene_info_table.shape[0]),"Single entry columns in gene_info_table must be either all float or all string. Mixed types or integers are not allowed."
				if has_floats.sum()==self.gene_info_table.shape[0]:
					self.aux_gene_info_table.loc[col,'dtype']='float'
					self.aux_gene_info_table.loc[col,'idx_map']='NA'
					self.aux_gene_info_table.loc[col]['inv_idx_map']='NA'
					self.aux_gene_info_table.loc[col,'return_dim']=1
				else:
					self.aux_gene_info_table.loc[col,'dtype']='one_hot_cat'
					all_unique=sorted(list(self.gene_info_table[col].unique()))
					assert len(all_unique)>1, "Must have at least 2 categories for one-hot variable."
					idx_map=dict(zip(all_unique,list(range(len(all_unique)))))
					self.aux_gene_info_table.loc[col]['idx_map']=idx_map
					self.aux_gene_info_table.loc[col]['inv_idx_map']=dict(zip(idx_map.values(),idx_map.keys()))
					self.gene_info_table[col]=self.gene_info_table[col].apply(lambda x: idx_map[x])
					self.aux_gene_info_table.loc[col,'return_dim']=len(idx_map)-1
	

	def __init__(self,disease_labels,symptom_freq_pairs,disease_associated_genes,gene_info_table,ordinal_freq_map,training_data_fraction,validation_data_fraction,missing_label='NA'):
		"""Dataset that stores disease-symptom annotations as a sparse array that can be used for disease embedding.
		
		Args:
		    disease_labels (Array of Strings): Strings that make up the index of the disease dataset
		    symptom_freq_pairs (Array of iterables): Each list contains the symptoms-frequency pairs annotated to each disease. Symptoms-frequencies are stored as a tuple.
		    ordinal_freq_map (Dictionary): Dictionary providing ordinal rank of each frequency used to describe the symptoms. 
		    missing_label (str, optional): String used to denote missing frequency information.
		"""
		self.disease_table=pd.DataFrame(columns=['SympFreqs','MappedGenes'],index=disease_labels)
		orig_symp_values = pd.Series(symptom_freq_pairs,index=disease_labels)
		all_unique_symptoms=sorted(list(set().union(*orig_symp_values.apply(lambda x:[y[0] for y in x]).values)))
		self.symptom_map=dict(zip(all_unique_symptoms,range(len(all_unique_symptoms))))
		self.inverse_symptom_map=dict(zip(self.symptom_map.values(),self.symptom_map.keys()))
		self.num_symptoms=len(self.symptom_map)
		
		self.ordinal_freq_map=ordinal_freq_map
		assert -1 not in ordinal_freq_map.values(),"-1 is not allowed as ordinal value for symptom frequency. This represents missing data and is reserved for this purpose."
		self.ordinal_freq_map[missing_label]=-1
		self.num_ordinal_freqs = len(self.ordinal_freq_map)-1
		self.missing_label=missing_label

		self.gene_info_table=gene_info_table

		new_symptoms = orig_symp_values.apply(lambda x: [(self.symptom_map[y[0]],self.ordinal_freq_map[y[1]]) for y in x])
		self.disease_table['SympFreqs']=new_symptoms
		orig_gene_values=pd.Series(disease_associated_genes,index=disease_labels)
		self.gene_map=dict(zip(self.gene_info_table.index,range(self.gene_info_table.index.shape[0])))
		self.inverse_gene_map=dict(zip(self.gene_map.values(),self.gene_map.keys()))
		self.num_total_genes = len(self.gene_map)
		self.disease_table['MappedGenes']=orig_gene_values.apply(lambda x: self.gene_map[x])


		self._process_gene_table()
		self.SetNewTrainingState(training_data_fraction,validation_data_fraction)



	def SetNewTrainingState(self, training_fraction, validation_fraction):

		assert (training_fraction+validation_fraction)<=1.0,"Training and validation fraction added together cannot exceed 1.0"
		if (training_fraction+validation_fraction)==1.0:
		    print("Warning: Setting a model training state without allowing for a test fraction. There will be test fraction available for independent replication.")

		num_training_diseases=int(np.floor(training_fraction*self.disease_table.shape[0]))
		num_validation_diseases=int(np.ceil(validation_fraction*self.disease_table.shape[0]))
		num_testing_diseases=int(self.disease_table.shape[0]-num_training_diseases-num_validation_diseases)

		self.training_index=pd.Index(np.random.choice(self.disease_table.index,size=num_training_diseases,replace=False))
		if (num_training_diseases+num_validation_diseases)==self.disease_table.index.shape[0]:
		    self.validation_index=self.disease_table.index.difference(self.training_index)
		else:
		    self.validation_index=pd.Index(np.random.choice(self.disease_table.index.difference(self.training_index),size=num_validation_diseases,replace=False))

		self.testing_index=self.disease_table.index.difference(np.union1d(self.training_index,self.validation_index))

		self.training_index=self.training_index.values
		self.validation_index=self.validation_index.values
		self.testing_index=self.testing_index.values

	def ShuffleTrainingValidation(self):
		combined_index=np.concatenate([self.training_index,self.validation_index])
		np.random.shuffle(combined_index)
		self.training_index=combined_index[0:self.training_index.shape[0]]
		self.validation_index=combined_index[self.training_index.shape[0]:]

	def SaveTrainingState(self,fName):
		if fName[-4:]!='.pth':
			fName+='.pth'
		currentState = dict()
		currentState['training_index']=self.training_index
		currentState['validation_index']=self.validation_index
		currentState['testing_index']=self.testing_index

		with open(fName, 'wb') as f:
			pickle.dump(currentState,f)

	def LoadTrainingState(self,fName):
		if fName[-4:]!='.pth':
			fName+='.pth'

		with open(fName, 'rb') as f:
			currentState = pickle.load(f)

		self.training_index=currentState['training_index']
		self.validation_index=currentState['validation_index']
		self.testing_index=currentState['testing_index']

		assert np.setdiff1d(np.union1d(np.union1d(self.training_index,self.validation_index),self.testing_index),self.disease_table.index.values).shape[0]==0,"Index of stored and loaded state do not match."




	def _torchWrapper(self,x):
		"""
		Note, all torch floating point tensors are converted to 32-bits to
		ensure GPU compatibility.
		"""

		if x.dtype==np.float32:
		    if sparse.issparse(x):
		        return torch.tensor(x.toarray(),dtype = torch.float32)
		    else:
		        return torch.tensor(x,dtype = torch.float32)

		elif x.dtype==np.float64:
		    if sparse.issparse(x):
		        return torch.tensor(x.toarray(),dtype = torch.float32)
		    else:
		        return torch.tensor(x,dtype = torch.float32)
		else:
		    if sparse.issparse(x):
		        return torch.tensor(x.toarray(),dtype = torch.long)
		    else:
		        return torch.tensor(x,dtype = torch.long)


	def _build_disease_coo_matrices(self,index):

		symp_x_inds=list(itertools.chain.from_iterable([[i]*len(x) for i,x in enumerate(self.disease_table.loc[index]['SympFreqs'])]))
		symp_y_inds=list(itertools.chain.from_iterable(self.disease_table.loc[index]['SympFreqs'].apply(lambda x: [y[0] for y in x])))
		values_freqs= list(itertools.chain.from_iterable(self.disease_table.loc[index]['SympFreqs'].apply(lambda x: [y[1] for y in x])))
		values_symps= np.ones((len(symp_x_inds)))

		return sparse.coo_matrix((values_symps,(symp_x_inds,symp_y_inds)),shape=(len(index),len(self.symptom_map)),dtype=np.float32),sparse.coo_matrix((values_freqs,(symp_x_inds,symp_y_inds)),shape=(len(index),len(self.symptom_map)),dtype=np.float32)

	def _build_gene_table_matrices(self, gene_list):
		return_data=[]
		for dcol in self.aux_gene_info_table.index:
			if self.aux_gene_info_table.loc[dcol]['dtype']=='float':
				return_data+=[self.gene_info_table.loc[gene_list][dcol].values.reshape(-1,1)]
			elif self.aux_gene_info_table.loc[dcol]['dtype']=='one_hot_cat':
				x_inds=list(itertools.chain.from_iterable([[i] for i,x in enumerate(self.gene_info_table.loc[gene_list][dcol]) if x!=0]))
				y_inds=self.gene_info_table.loc[gene_list][dcol].values
				y_inds=list(y_inds[y_inds!=0]-1)
				values=np.ones((len(x_inds)))
				return_data+=[sparse.coo_matrix((values,(x_inds,y_inds)),shape=(len(gene_list),self.aux_gene_info_table.loc[dcol]['return_dim']),dtype=np.float32)]
			elif self.aux_gene_info_table.loc[dcol]['dtype']=='float_array':
				return_data+=[np.vstack(self.gene_info_table.loc[gene_list][dcol].values)]
			else:
				x_inds=list(itertools.chain.from_iterable([[i]*len(x) for i,x in enumerate(self.gene_info_table.loc[gene_list][dcol])]))
				y_inds=list(itertools.chain.from_iterable(self.gene_info_table.loc[gene_list][dcol]))
				values= np.ones((len(x_inds)))
				return_data+=[sparse.coo_matrix((values,(x_inds,y_inds)),shape=(len(gene_list),self.aux_gene_info_table.loc[dcol]['return_dim']),dtype=np.float32)]
		return tuple(return_data)

	def ReturnDataArrays(self,index):
		symp_arrays=self._build_disease_coo_matrices(index)
		symp_arrays=tuple(self._torchWrapper(x) for x in symp_arrays)
		gene_arrays=self.ReturnGeneDataArrays([self.inverse_gene_map[x] for x in self.disease_table.loc[index]['MappedGenes'].values])
		return symp_arrays+(gene_arrays,)

	def ReturnGeneDataArrays(self,gene_list):
		gene_arrays=self._build_gene_table_matrices(gene_list)
		gene_arrays=tuple(self._torchWrapper(x) for x in gene_arrays)
		return torch.cat(gene_arrays,axis=1)


	def DropSymptoms(self,symptom_list):

		oldSymptomToIntMap=self.symptom_map

		allSymptoms=set(oldSymptomToIntMap.keys())

		removedSymptoms=set(symptom_list)

		assert len(removedSymptoms.difference(allSymptoms))==0, "Symptoms: {0:s} not in set of possible symptoms.".format(','.join(list(removedSymptoms.difference(allSymptoms))))

		keptInts = set([oldSymptomToIntMap[x] for x in allSymptoms.difference(symptom_list)])


		for old_symp in removedSymptoms:
		    del oldSymptomToIntMap[old_symp]

		newSymptomToIntMap = {}
		oldToNewIntMap={}
		for i,key in enumerate(oldSymptomToIntMap):
			oldToNewIntMap[oldSymptomToIntMap[key]]=i
			newSymptomToIntMap[key] = i


		self.symptom_map=newSymptomToIntMap
		self.inverse_symptom_map=dict(zip(self.symptom_map.values(),self.symptom_map.keys()))
		self.disease_table['SympFreqs']=self.disease_table['SympFreqs'].apply(lambda x: [(oldToNewIntMap[y[0]],y[1]) for y in x if y[0] in keptInts])

	def DropDiseases(self, disease_list):
		disease_list=pd.Index(disease_list)
		assert len(disease_list.difference(self.disease_table.index))==0,"Subjects: {0:s} not in data table.".format(','.join(list(disease_list.difference(self.dataset.index))))
		self.disease_table.drop(index=disease_list,inplace=True)


	def FindAllDiseases_wSymptom(self,symptom):
		if symptom not in self.symptom_map.keys():
			raise KeyError("Symptom {0:s} not in possible set.".format(symptom))
		else:
			intVal = self.symptom_map[symptom]
			return self.disease_table.index[self.disease_table['SympFreqs'].apply(lambda x: intVal in set([y[0] for y in x]))]

	def FindAllDiseases_wGene(self,gene):
		if gene not in self.gene_map.keys():
			raise KeyError("Gene {0:s} not in possible set.".format(gene))
		else:
			intVal = self.gene_map[gene]
			return self.disease_table.index[self.disease_table['MappedGenes'].apply(lambda x: intVal==x)]

	def InferNullModel(self,pseudo_count=1.0):
		training_data_symps,training_data_freqs = self._build_disease_coo_matrices(self.training_index)
		base_symp_freqs=((pseudo_count/2.0)+ np.array(training_data_symps.sum(axis=0)).ravel())/(pseudo_count+training_data_symps.shape[0])
		missing_rates=((pseudo_count/2.0)+ np.array((training_data_symps==1).multiply(training_data_freqs==-1).sum(axis=0)).ravel())/(pseudo_count+np.array(training_data_symps.sum(axis=0)).ravel())

		full_freq_array=training_data_freqs.toarray()
		full_freq_array[training_data_symps.toarray()==0.0]=-1.0
		full_freq_array[full_freq_array==-1]=full_freq_array.max()+1
		unrolled_freq_array=np.zeros((full_freq_array.shape[0],full_freq_array.shape[1],int(full_freq_array.max()+1)))
		for i in range(unrolled_freq_array.shape[0]):
			unrolled_freq_array[i,np.arange(unrolled_freq_array.shape[1]),np.array(full_freq_array[i],dtype=np.int32)]=1
		unrolled_freq_array=unrolled_freq_array[:,:,:-1]
		freq_counts=unrolled_freq_array.sum(axis=0)+(pseudo_count/unrolled_freq_array.shape[2])
		freq_stats=freq_counts/freq_counts.sum(axis=1).reshape(freq_counts.shape[0],-1)
		return {'BaselineSymptomRates':base_symp_freqs,"MissingRates":missing_rates,'FrequencyRates':freq_stats}
			
if __name__=='__main__':
	omim_table=pd.read_pickle('../../../Data/OMIM_HPO_Table/OMIMSingleGeneInNetworkHPOUnrolled.pth')
	pp_embed=pd.read_csv('../../../Data/PrimeKG/NetworkEmbeddings/PrimeKG_protein_protein_Dim8.txt',sep=' ',header=None,skiprows=[0])
	pp_embed.set_index(0,inplace=True)
	gene_table=pd.read_pickle('../../../Data/PrimeKG/PrimeKG_ProteinFeatures.pth')
	gene_table.loc[gene_table.index,'net_embed']=pd.Series([x for x in pp_embed.loc[gene_table.index].values],index=gene_table.index)


	self=GeneToPhenotypeDataset(omim_table.index,omim_table.HPO_wFreq,omim_table['GENE/INHERIT'].apply(lambda x:x[0]),gene_table,{'VR':0,'OC':1,'F':2,'VF':3,'O':4},0.6,0.15,missing_label='NA')
