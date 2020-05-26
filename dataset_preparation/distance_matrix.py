import numpy as np
import torch
torch.cuda.empty_cache()
# device = torch.device('cuda')
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

class DistanceMatrix:
    """
    Create upper diagonal & flattened distance matrix from the amino acid distance matrices
    """

    def __init__(self, source_path, destination_path, name, tensor_dimension):
        self.source_path = source_path
        self.name = name
        self.destination_path = destination_path
        self.tensor_dimension = tensor_dimension

    def standardise_flatten_distance_matrix(self):
        """
        :return:
        """
        with open(self.source_path + '/' + self.name + '_label.pickle', 'rb') as labels_file:
            print("Converting to numpy array and standardising...")
            holder = pd.read_pickle(labels_file)
            array = holder.numpy() # Convert pytorch tensor to numpy array to perform standardisation
            scaler = StandardScaler()
            scaled_values = scaler.fit_transform(array)
            new_tensor = torch.from_numpy(scaled_values)
            upper_triangle = torch.triu(new_tensor, diagonal=1)
            q = upper_triangle.shape
            print("The shape of q is {} by {}".format(q[0], q[1]))
            down_pad = self.tensor_dimension - q[0]
            print(self.name.split('_')[0])
            right_pad = self.tensor_dimension - q[1]
            print("The down pad is: {}".format(down_pad))
            print("The right pad is: {}".format(right_pad))
            m = torch.nn.ZeroPad2d((0,right_pad,0,down_pad))
            padded = m(upper_triangle)
            print("Final shape of {} is: {}".format(self.name.split('_')[0], padded.shape))

            self.flatten = torch.flatten(padded)

        return self.flatten

    def save_file(self):
        with open(self.destination_path + '/' + self.name.split('_')[0] + '_labels.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.flatten, file, protocol=4) # Save as a pickle object
