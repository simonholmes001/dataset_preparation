import torch
torch.cuda.empty_cache()
# device = torch.device('cuda')

import pandas as pd
import pickle

class FeaturesMatrix:
    """

    """

    def __init__(self, source_path, destination_path, name, tensor_dimension):
        self.source_path = source_path
        self.name = name
        self.destination_path = destination_path
        self.tensor_dimension = tensor_dimension # Indicates the padding factor to bring all tensors to the same dimension

    def features_same_size(self):
        """
        Takes the features matrix & adjusts all to the same dimension
        """
        with open(self.source_path + self.name + '_features.pickle', 'rb') as labels_file:
            holder = pd.read_pickle(labels_file)
            q = holder.shape
            print("The shape of {} is {} by {}".format(self.name.split('_')[0], q[0], q[1]))
            down_pad = self.tensor_dimension - q[0]
            print("The down padding is: {}".format(down_pad))
            m = torch.nn.ZeroPad2d((0,0,0,down_pad))
            self.padded_tensor = m(holder)
            print("Final shape of {} is: {}".format(self.name.split('_')[0], self.padded_tensor.shape))

            return self.padded_tensor # Comment out if flatten tensor required

            # self.padded_flat = torch.flatten(self.padded_tensor) # Comment out if flatten tensor not required
            # return self.padded_flat # Comment out if flatten tensor not required



    def save_file(self):
        with open(self.destination_path + self.name.split('_')[0] + '_' + 'features.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.padded_tensor, file, protocol=4) # Save as a pickle object  # COMMENT OUT IF FLATTEN REQUIRED
            # pickle.dump(self.padded_flat, file, protocol=4) # Save as a pickle object # COMMENT OUT IF FLATTEN NOT REQUIRED
