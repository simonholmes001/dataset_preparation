import torch
torch.cuda.empty_cache()
# device = torch.device('cuda')
import pandas as pd
import pickle

class DistanceMatrix:
    """
    Create upper diagonal & flattened distance matrix from the amino acid distance matrices
    """

    def __init__(self, source_path, destination_path, name):
        self.source_path = source_path
        self.name = name
        self.destination_path = destination_path

    def flatten_distance_matrix(self):
        """
        :return:
        """
        with open(self.source_path + '/' + self.name + '_label.pickle', 'rb') as labels_file:
            holder = pd.read_pickle(labels_file)
            upper_triangle = torch.triu(holder, diagonal=1)
            self.flatten = torch.flatten(upper_triangle)

        return self.flatten

    def save_file(self):
        with open(self.destination_path + '/' + self.name.split('_')[0] + '_distance_label.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.flatten, file, protocol=4) # Save as a pickle object
