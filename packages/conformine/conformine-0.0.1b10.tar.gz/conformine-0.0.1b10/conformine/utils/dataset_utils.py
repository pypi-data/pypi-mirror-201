import sys

import torch
from torch.utils.data import Dataset
from ..utils.data_utils import read_fasta, fasta_to_index


class StandaloneInputData(Dataset):
	def __init__(self, fasta_file, dev='cpu'):
		self.names = []
		self.input = []
		self.input_file = fasta_file
		self.__fasta_to_onehot()
		self.__extract_input_data()
		self.X = [seq.to(dev) for seq in self.input]
		self.protein_lengh = [seq.shape[0] for seq in self.X]

	def __fasta_to_onehot(self):
		fasta_dictionary = read_fasta(fasta_path=self.input_file)
		numpy_index_dictionary = fasta_to_index(fasta_dict=fasta_dictionary)
		self.index_dictionary = {key: torch.tensor(numpy_index_dictionary[key]) for key in
		                         numpy_index_dictionary.keys()}

	def __extract_input_data(self):
		for key in self.index_dictionary.keys():
			self.names.append(key)
			self.input.append(self.index_dictionary[key])

	def __len__(self):
		return len(self.X)

	def __getitem__(self, item):
		sample = [self.X[item], None, self.names[item], None, self.protein_lengh[item]]
		# The None's above are for the ground truth and the protein type, used for training
		return sample