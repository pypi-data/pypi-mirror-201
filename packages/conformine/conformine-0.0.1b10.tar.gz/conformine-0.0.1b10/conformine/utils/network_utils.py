import os
from torch.utils.data import DataLoader
# from sklearnex import patch_sklearn

# patch_sklearn()


class NNwrapper:
    def __init__(self, model, dev='cuda:0', learning_rate=1e-5, with_scheduler=False, name='unnamed', with_shift=False,
                 shift_normalization=None, only_scalars=True, global_loss_only=True):

        self.train_average_pearson_list = []
        self.train_average_pearson_pval_list = []
        self.train_average_r2_list = []

        self.test_average_pearson_list = []
        self.test_average_pearson_pval_list = []
        self.test_average_r2_list = []

        self.dev = dev
        self.model = model
        self.learning_rate = learning_rate
        self.with_scheduler = with_scheduler
        self.name = name
        self.model_path = os.path.join('../models', self.name)
        self.dataloaders_path = os.path.join(self.model_path, 'dataloaders')

        self.model.to(self.dev)
        self.with_shift = with_shift
        self.shift_normalization = shift_normalization

        self.only_scalars = only_scalars
        self.global_loss_only = global_loss_only

    def predict(self, dataset, batch_size=5):
        print('Predicting values...')
        data_loader = DataLoader(dataset,
                                 batch_size=batch_size,
                                 collate_fn=collate_fn,
                                 shuffle=True)

        self.model.set_batch_size(batch_size=batch_size)
        self.model.eval()

        results_dict = {}

        # conf_names_dict = {
        #     0: 'core_alpha',
        #     1: 'core_beta',
        #     # 2: 'coil',
        #     2: 'other_conformation',
        #     3: 'surr_alpha',
        #     4: 'surr_beta',
        # }
        conf_names_dict = {
            0: 'core_helix',
            1: 'core_sheet',
            2: 'other_conformation',
            3: 'surr_helix',
            4: 'surr_sheet',
        }
        for sample in data_loader:
            X, y, name, prot_type, prot_len = sample

            yp = self.model.forward(sample)
            num_conf = yp.shape[-1] - 2

            for idx, sequence in enumerate(yp):
                trimmed_sequence = sequence[:prot_len[idx]]
                results_dict[name[idx]] = {'id': name[idx],
                                           'ConVa': trimmed_sequence[:,0].cpu().detach().tolist(),
                                           'Predicted_ShiftCrypt':trimmed_sequence[:,-1].cpu().detach().tolist()}
                if num_conf > 0:
                    for conformation_idx in range(num_conf):
                        results_dict[name[idx]][conf_names_dict[conformation_idx]] = trimmed_sequence[:,conformation_idx+1].cpu().detach().tolist()
        return results_dict


def collate_fn(batch):
    return tuple(zip(*batch))

