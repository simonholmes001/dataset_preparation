import torch
torch.cuda.empty_cache()
# device = torch.device('cuda')
import pandas as pd
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

    def flatten_distance_matrix(self):
        """
        :return:
        """
        with open(self.source_path + '/' + self.name + '_label.pickle', 'rb') as labels_file:
            holder = pd.read_pickle(labels_file)
            upper_triangle = torch.triu(holder, diagonal=1)
            q = upper_triangle.shape
            print("The shape of q is {} by {}".format(q[0], q[1]))
            try:
                down_pad = self.tensor_dimension - q[0]
            except:
                print(self.name.split('_')[0])
                pass
            try:
                right_pad = self.tensor_dimension - q[1]
            except:
                pass
            try:
                print("The down pad is: {}".format(down_pad))
                print("The right pad is: {}".format(right_pad))
            except:
                pass
            try:
                m = torch.nn.ZeroPad2d((0,right_pad,0,down_pad))
                x = m(upper_triangle)
                print("Final shape of {} is: {}".format(self.name.split('_')[0], x.shape))
            except:
                pass
            self.flatten = torch.flatten(upper_triangle)

        return self.flatten

    def save_file(self):
        with open(self.destination_path + '/' + self.name.split('_')[0] + '_labels.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.flatten, file, protocol=4) # Save as a pickle object
