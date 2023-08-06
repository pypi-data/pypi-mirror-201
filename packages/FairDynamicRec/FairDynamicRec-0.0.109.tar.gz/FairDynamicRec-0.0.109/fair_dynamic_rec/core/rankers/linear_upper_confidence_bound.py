import numpy as np
from .linear_submodular_bandit import LSB
from fair_dynamic_rec.core.util.utils import get_param_config_name
from fair_dynamic_rec.core.util.outputs import make_output_dir

class LinUCB(LSB):
    def __init__(self, config, dataObj, parameters=None):
        super(LinUCB, self).__init__(config, dataObj, parameters)
        self.dim = self.dataObj.feature_data['train_item_latent_features'].shape[1]

        if config.load_model and self.__class__.__name__ == 'LinUCB':
            self.load_parameters(config, parameters)
        else:
            # parameters
            self.ill_matrix_counter = 0
            self.theta = np.ones((self.dataObj.n_users, self.dim))  # d-dimensional
            self.b = np.zeros((self.dataObj.n_users, self.dim))  # d
            self.M = np.zeros((self.dataObj.n_users, self.dim, self.dim))  # d by d
            self.MInv = np.zeros((self.dataObj.n_users, self.dim, self.dim))  # for fast matrix inverse computation, d by d
            for i in range(self.dataObj.n_users):
                self.M[i] = np.eye(self.dim)
                self.MInv[i] = np.eye(self.dim)
            # for ill inverse
            self.b_tmp = np.zeros((self.dataObj.n_users, self.dim))
            self.MInv_tmp = np.zeros((self.dataObj.n_users, self.dim, self.dim))

            # self.gamma = float(parameters.get("gamma",{}).get("value",0))
            # self.window = int(parameters.get('window',{}).get('value',0))
            self.click_history = np.zeros((self.dataObj.n_users, self.dim))
            #
            # self.shuffle_K = int(parameters.get('shuffle_K',{}).get('value',0))
            # self.epsilon = float(parameters.get('epsilon', {}).get('value', 0))
            # self.ears_gamma = float(parameters.get('ears_gamma', {}).get('value', 0))

    def save_parameters(self, config, ranker_config):
        pre_path = make_output_dir(config, get_param_config_name(ranker_config))
        np.savetxt(pre_path/'n_samples', self.n_samples, fmt='%i')
        np.savetxt(pre_path / 'n_clicks', self.n_clicks, fmt='%i')
        text_file = open(pre_path / 'ill_matrix_counter', "w")
        text_file.write(str(self.ill_matrix_counter))
        text_file.close()
        np.savetxt(pre_path / 'theta', self.theta, fmt='%f')
        np.savetxt(pre_path / 'b', self.b, fmt='%f')
        self.save_3d_array(pre_path / 'M', self.M, '%f')
        self.save_3d_array(pre_path / 'MInv', self.MInv, '%f')
        np.savetxt(pre_path / 'b_tmp', self.b_tmp, fmt='%f')
        self.save_3d_array(pre_path / 'MInv_tmp', self.MInv_tmp, '%f')
        np.savetxt(pre_path / 'click_history', self.click_history, fmt='%f')
        # np.savetxt(pre_path / 'item_coef', self.item_coef, fmt='%f')
        # np.savetxt(pre_path / 'exp_recommended', self.exp_recommended, fmt='%f')
        # np.savetxt(pre_path / 'exp_examined', self.exp_examined, fmt='%f')
    def load_parameters(self, config, ranker_config):
        pre_path = make_output_dir(config, get_param_config_name(ranker_config))
        self.n_samples = np.loadtxt(pre_path/'n_samples', dtype='int')
        self.n_clicks = np.loadtxt(pre_path / 'n_clicks', dtype='int')
        with open(pre_path / 'ill_matrix_counter') as file:
            line = file.readline().rstrip()
            self.ill_matrix_counter = int(line)
        self.theta = np.loadtxt(pre_path / 'theta')
        self.b = np.loadtxt(pre_path / 'b')
        self.M = self.load_3d_array(pre_path / 'M', (self.dataObj.n_users, self.dim, self.dim))
        self.MInv = self.load_3d_array(pre_path / 'MInv', (self.dataObj.n_users, self.dim, self.dim))
        self.b_tmp = np.loadtxt(pre_path / 'b_tmp')
        self.MInv_tmp = self.load_3d_array(pre_path / 'MInv_tmp', (self.dataObj.n_users, self.dim, self.dim))
        self.click_history = np.loadtxt(pre_path / 'click_history')
        # self.item_coef = np.loadtxt(pre_path / 'item_coef')
        # self.exp_recommended = np.loadtxt(pre_path / 'exp_recommended')
        # self.exp_examined = np.loadtxt(pre_path / 'exp_examined')
    def save_3d_array(self, fn_out, arr, frmt):
        # Write the array to disk
        with open(fn_out, 'w') as outfile:
            # I'm writing a header here just for the sake of readability
            # Any line starting with "#" will be ignored by numpy.loadtxt
            outfile.write('# Array shape: {0}\n'.format(arr.shape))

            # Iterating through a ndimensional array produces slices along
            # the last axis. This is equivalent to data[i,:,:] in this case
            for data_slice in arr:
                # The formatting string indicates that I'm writing out
                # the values in left-justified columns 7 characters in width
                # with 2 decimal places.
                np.savetxt(outfile, data_slice, fmt=frmt)

                # Writing out a break to indicate different slices...
                outfile.write('# New slice\n')
    def load_3d_array(self, fn_in, shp):
        # Read the array from disk
        arr = np.loadtxt(fn_in)

        # However, going back to 3D is easy if we know the
        # original shape of the array
        return arr.reshape(shp)

    def get_ranking(self, batch_users, sampled_item=None, round=None):
        """
        :param x: features
        :param k: number of positions
        :return: ranking: the ranked item id.
        """
        # assert x.shape[0] >= k
        rankings = np.zeros((len(batch_users), self.config.list_size), dtype=int)
        self.batch_features = np.zeros((len(batch_users), self.config.list_size, self.dim))
        tie_breaker = self.prng.rand(len(self.dataObj.feature_data['train_item_latent_features']))
        for i in range(len(batch_users)):
            user = batch_users[i]
            x = self.dataObj.feature_data['train_item_latent_features']
            if self.processing_type == 'item_weight':
                x = self.item_coef[user].reshape(self.dataObj.n_items, 1) * x

            if self.processing_type == 'recommended_discountfactor':
                cb = self.alpha * (1 - (self.exp_recommended[user] / (round + 1))) * np.sqrt(np.multiply(np.dot(x, self.MInv[user]), x).sum(axis=1))
            elif self.processing_type == 'examined_discountfactor':
                cb = self.alpha * (1 - (self.exp_examined[user] / (round + 1))) * np.sqrt(np.multiply(np.dot(x, self.MInv[user]), x).sum(axis=1))
            else:
                cb = self.alpha * np.sqrt(np.multiply(np.dot(x, self.MInv[user]), x).sum(axis=1))
            score = np.dot(x, self.theta[user])
            ucb = score + cb
            rankings[i] = np.lexsort((tie_breaker, -ucb))[:self.config.list_size]
            if self.processing_type == 'EARS':
                rankings[i] = np.asarray(self.shuffling_topK(rankings[i], np.sort(-ucb)[:self.config.list_size], self.config.list_size))
            self.batch_features[i] = self.dataObj.feature_data['train_item_latent_features'][rankings[i]]
        return rankings