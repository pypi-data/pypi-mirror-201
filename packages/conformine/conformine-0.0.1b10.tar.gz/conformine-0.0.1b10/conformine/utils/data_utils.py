from Bio import SeqIO
import numpy as np


def read_fasta(fasta_path):
    fasta_dict = {}
    for record in SeqIO.parse(fasta_path, 'fasta'):
        fasta_dict[record.id] = record.seq

    return fasta_dict


def fasta_to_index(fasta_dict):
    index_dict = {}

    aa_dict = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11,
               'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19, 'X': 20}

    for key in fasta_dict.keys():
        index_dict[key] = np.array([aa_dict[aa] for aa in fasta_dict[key]])

    return index_dict
