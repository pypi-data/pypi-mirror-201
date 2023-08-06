import pandas as pd
import torch
import numpy as np

class TorchDataWrapper(torch.utils.data.Dataset):

    def _collateFunction(self,x):
        return x[0]

    def _indexSplit(self,dataSetSize,totalNumBatches):
        if totalNumBatches>0:
            nEachBatch, extras = divmod(dataSetSize, totalNumBatches)
            section_sizes = ([0] +extras * [nEachBatch+1] +(totalNumBatches-extras) * [nEachBatch])
            return np.array(section_sizes, dtype=np.int32).cumsum()
        else:
            return np.array([0]+[dataSetSize], dtype=np.int32)

    def __init__(self,primary_dataset,batch_size,index='Training'):
        """

        Wrapper for DatasetTrainingState to allow for rapid subset sampling using PyTorch DataLoader, which allows for multi-threaded loading/queueing of data.

        Parameters
        ----------
        training_state : DatasetTrainingState
            DatasetTrainingState to be wrapped
        batch_size : int
            Batch size for the sampler.

        Returns
        -------
        None

        """


        self.primary_dataset = primary_dataset
        assert index in ['Training','Validation','Test'],"Only Training, Validation or Test dataset indices allowed."
        if index=='Training':
            self.sampling_index=self.primary_dataset.training_index
        elif index=='Validation':
            self.sampling_index=self.primary_dataset.validation_index
        else:
            self.sampling_index=self.primary_dataset.testing_index

        np.random.shuffle(self.sampling_index)
        self.totalNumBatches,leftover = divmod(len(self.sampling_index),batch_size)
        self.splits = self._indexSplit(self.sampling_index.shape[0],self.totalNumBatches)
        if self.totalNumBatches == 0:
            self.totalNumBatches+=1

    def __len__(self):
        return self.totalNumBatches

    def shuffle_index(self):
        np.random.shuffle(self.sampling_index)

    def __getitem__(self,index):
        batchIndex=self.sampling_index[self.splits[index]:self.splits[index+1]]
        return self.primary_dataset.ReturnDataArrays(batchIndex)

