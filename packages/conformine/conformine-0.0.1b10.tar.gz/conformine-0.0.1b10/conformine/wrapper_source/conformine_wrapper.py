from ..utils.from_fasta_standalone_predictor import *


class Conformine:
	def __init__(self, fasta_file_path, device='cpu'):
		self.fasta_file_path = fasta_file_path
		self.device = device

		self.dataset, self.fasta_name, self.seq_dictionary = from_fasta_to_dataset(fasta_file=self.fasta_file_path,
		                                                                           the_device=device)
		self.predictions_dictionary = None

	def predict(self):
		self.predictions_dictionary = make_prediction(self.dataset, self.seq_dictionary, the_device=self.device,
		                                              fasta_name=self.fasta_name)

	def get_all_predictions(self):
		return self.predictions_dictionary

	def pred_to_json(self, json_path):
		to_json(self.predictions_dictionary, json_path)