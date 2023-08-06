import sys

import torch.nn as nn
import torch
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pad_sequence


class MyLinearLayer(nn.Module):
	def __init__(self, in_dim=None, out_dim=None, residuals=False, dropout=0.0,
	             remove_activation_and_norm=False,
	             ):
		super(MyLinearLayer, self).__init__()
		self.in_dim = in_dim
		self.out_dim = out_dim
		self.residuals = residuals
		self.remove_activation_and_norm = remove_activation_and_norm

		self.layer_norm = nn.LayerNorm(in_dim)
		self.tanh = nn.Tanh()
		self.linear = nn.Linear(
			in_features=self.in_dim,
			out_features=out_dim
		)
		self.dropout = nn.Dropout(p=dropout)

	def forward(self, x0):

		if self.remove_activation_and_norm:
			x = x0
		else:
			x = self.layer_norm(x0)
			x = self.tanh(x)
		x = self.linear(x)
		x = self.dropout(x)
		if self.residuals:
			x += 0
		return x


class ActivationsRemovedMyRNN(nn.Module):

	def __init__(self, bert=False, positional_embedding_for_linear=False, positional_embedding_for_rnn=False):
		super(ActivationsRemovedMyRNN, self).__init__()
		self.batch_size = None
		self.bert = bert
		self.positional_embedding_for_linear = positional_embedding_for_linear
		self.positional_embedding_for_rnn = positional_embedding_for_rnn

		if self.positional_embedding_for_linear and self.positional_embedding_for_rnn:
			print("Only one positional embedding is possible")
			sys.exit()

		# self.recurrent_layers = 2
		self.recurrent_layers = 5
		self.recurrent_hidden_size = 36
		self.output_dimensions = 7
		self.rnn_dropout = 0.15
		self.linear_dropout = 0.1

		if self.bert:
			self.embedding_dimensions = 30
		else:
			self.embedding_dimensions = 50
			self.embeddings = nn.Embedding(num_embeddings=22, embedding_dim=self.embedding_dimensions, padding_idx=21)

		if self.positional_embedding_for_rnn:
			self.embedding_dimensions = self.embedding_dimensions + 1

		self.rnn = nn.GRU(
			input_size=self.embedding_dimensions,
			hidden_size=self.recurrent_hidden_size,
			num_layers=self.recurrent_layers,
			batch_first=True,
			dropout=self.rnn_dropout,
			bidirectional=True
		)

		if not self.positional_embedding_for_linear:
			self.linear_0 = MyLinearLayer(
				in_dim=self.recurrent_hidden_size * 2,
				out_dim=32,
				dropout=self.linear_dropout,
				remove_activation_and_norm=True
			)

		elif self.positional_embedding_for_linear == 'proportional':
			self.linear_0 = MyLinearLayer(
				in_dim=self.recurrent_hidden_size * 2 + 1,
				out_dim=32,
				dropout=self.linear_dropout,
				remove_activation_and_norm=True
			)
		else:
			print("Please select a valid positional embedding")
			sys.exit()

		self.linear_1 = MyLinearLayer(
			in_dim=32,
			out_dim=16,
			dropout=self.linear_dropout
		)

		self.linear_2 = MyLinearLayer(
			in_dim=16,
			out_dim=self.output_dimensions,
			dropout=0.,
		)

		self.linear_sequential = nn.Sequential(
			self.linear_0,
			self.linear_1,
			self.linear_2,
		)

		self.double()

	def set_batch_size(self, batch_size):
		self.batch_size = batch_size

	def __percentage_of_sequence_PE(self, sample):
		list_of_positions = []

		for sequence in sample:
			length = sequence.shape[0]
			percentages = torch.tensor([i / (length - 1) for i in range(length)])
			list_of_positions.append(percentages)

		return list_of_positions

	def forward(self, the_sample):
		x = the_sample[0]
		sequence_lenghs = the_sample[4]
		h = self.init_hidden(batch_size=self.batch_size)

		padded = pad_sequence(x, batch_first=True)

		if self.positional_embedding_for_linear or self.positional_embedding_for_rnn:
			pos_embeding = self.__percentage_of_sequence_PE(x)
			padded_pos_embedding = pad_sequence(pos_embeding, batch_first=True)
			num_of_sequences = padded_pos_embedding.shape[0]

		if not self.bert:
			embeds = self.embeddings(padded.data)
			embed_device = embeds.device

			if self.positional_embedding_for_rnn:
				embeds = \
					torch.cat([embeds, padded_pos_embedding.reshape(num_of_sequences, -1, 1).to(embed_device)], dim=2)

			out = pack_padded_sequence(
				embeds,
				sequence_lenghs,
				batch_first=True,
				enforce_sorted=False)

		else:
			out = pack_padded_sequence(padded.data,
			                           sequence_lenghs,
			                           batch_first=True,
			                           enforce_sorted=False).double()

		out, hi = self.rnn(out, h)

		out = pad_packed_sequence(out, batch_first=True)

		if not self.positional_embedding_for_linear:
			lin_input = out[0]
		elif self.positional_embedding_for_linear == 'proportional':
			lin_input = torch.cat([out[0], padded_pos_embedding.reshape(num_of_sequences, -1, 1).to(embed_device)],
			                      dim=2)

		lin_out = self.linear_sequential(lin_input)
		return lin_out

	def init_hidden(self, batch_size=1):
		weight = next(self.parameters()).data

		hidden = weight.new(self.recurrent_layers * 2,
		                    self.batch_size,
		                    self.recurrent_hidden_size).zero_()

		### Added for non-zero initialization ###
		nn.init.constant_(hidden, 0.5)
		return hidden


def weight_reset_rnn(m):
	if isinstance(m, nn.Embedding) or isinstance(m, MyLinearLayer) or isinstance(m, nn.GRU):
		m.reset_parameters()


def weights_init(m):
	if isinstance(m, nn.Embedding) or isinstance(m, MyLinearLayer):
		torch.nn.init.xavier_uniform(m.weight.data)
	elif isinstance(m, nn.GRU):
		for element in m.all_weights:
			torch.nn.init.xavier_uniform(element)
