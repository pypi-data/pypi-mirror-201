import sys
import time
import numpy as np
import torch
import os
from ..utils.dataset_utils import StandaloneInputData
from ..utils.network_utils import NNwrapper
from ..utils.pytorch_models import ActivationsRemovedMyRNN
from Bio import SeqIO
import pickle
import json

import warnings
from sklearn.exceptions import ConvergenceWarning

from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def from_fasta_to_dataset(fasta_file, the_device='cpu'):
    fasta_name = fasta_file.split('/')[-1].split('.')[0]

    seq_dictionary = {}
    with open(fasta_file, 'r') as handle:
        for record in SeqIO.parse(handle, "fasta"):
            seq_dictionary[record.id] = [aa for aa in str(record.seq)]

    dataset = StandaloneInputData(fasta_file=fasta_file, dev=the_device)
    return dataset, fasta_name, seq_dictionary


def make_prediction(dataset, seq_dictionary, the_device='cpu', fasta_name=str):
    rootdir = get_project_root()

    torch_model = ActivationsRemovedMyRNN()
    state_dictionary_path = os.path.join(os.path.abspath(rootdir), 'utils/models',
                                         'state_dictionary_torch_model_bw_0.13.pt')

    torch_model.load_state_dict(torch.load(state_dictionary_path))

    model_wrapper = NNwrapper(
        model=torch_model,
        name='{0}_predictions'.format(fasta_name),
        dev=the_device,
    )
    tic = time.time()
    predictions_dict = model_wrapper.predict(dataset, batch_size=100)

    # corrected_parameters_path = os.path.join(rootdir, 'utils/models/normalization_parameters.json')
    corrected_parameters_path = os.path.join(rootdir, 'utils/models/113_correct_normalization_parameters.json')
    with open(corrected_parameters_path, 'r') as f:
        corrected_parameters_dict = json.load(f)

    # positional_to_name = {
    #     'ConVa': '0',
    #     'core_alpha': '1',
    #     'core_beta': '2',
    #     'other_conformation': '3',
    #     'surr_alpha': '4',
    #     'surr_beta': '5',
    #     'Predicted_ShiftCrypt': '6',
    # }
    positional_to_name = {
        'ConVa': '0',
        'core_helix': '1',
        'core_sheet': '2',
        'other_conformation': '3',
        'surr_helix': '4',
        'surr_sheet': '5',
        'Predicted_ShiftCrypt': '6',
    }

    corrected_predictions = {}
    for idx in predictions_dict.keys():
        corrected_predictions[idx] = {}
        for pre_conf in predictions_dict[idx].keys():
            if pre_conf != 'id':
                conf = positional_to_name[pre_conf]
                norm_std = corrected_parameters_dict[conf]['std']
                norm_average = corrected_parameters_dict[conf]['average']

                corrected_array = np.array(predictions_dict[idx][pre_conf]) * norm_std + norm_average
                corrected_list = corrected_array.tolist()
                corrected_predictions[idx][pre_conf] = corrected_list
            else:
                corrected_predictions[idx]['id'] = predictions_dict[idx]['id']

    predictions_dict = corrected_predictions

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        scaler = pickle.load(open(os.path.join(rootdir, 'utils/models', 'minmax_scaler_bw_0.13_ground_sklearn_1.2.1.pkl'), 'rb'))
        scaled_predictions = scale_conva(the_scaler=scaler, predictions_dict=predictions_dict)
    predictions_dict = scaled_predictions

    for id in predictions_dict.keys():
        predictions_dict[id]['seq'] = seq_dictionary[id]

    toc = time.time()
    print("ConforMine predictions ran in {0} seconds".format(str(toc-tic)))


    return predictions_dict


def scale_conva(the_scaler, predictions_dict):
    scaled_dictionary = {}

    for bmrb_id in predictions_dict.keys():
        conva = np.array(predictions_dict[bmrb_id]['ConVa'])
        corrected_conva = list(the_scaler.transform(conva.reshape(-1,1)).flatten())

        updated_predictions = predictions_dict[bmrb_id]
        updated_predictions['ConVa'] = corrected_conva

        scaled_dictionary[bmrb_id] = updated_predictions

    return scaled_dictionary


def to_json(predictions_dict, json_savepath:str):
    if json_savepath[-5:] == '.json':
        with open(json_savepath, 'w') as f:
            json.dump(predictions_dict, f, indent=4)
    else:
        raise NameError('The output file should have the .json extension')
