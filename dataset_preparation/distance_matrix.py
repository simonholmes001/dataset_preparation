import torch
from torch import nn
torch.cuda.empty_cache()
from sklearn import preprocessing
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
        with open(self.source_path + self.name.split('_')[0] + '_label.pickle', 'rb') as labels_file:
            holder = pickle.load(labels_file)
            # array = holder.numpy() # Convert pytorch tensor to numpy array to perform standardisation

            # scaler = StandardScaler() # Comment out if no standardisation is required
            # scaled_values = scaler.fit_transform(array) # Comment out if no standardisation is required
            # new_tensor = torch.from_numpy(scaled_values) # Comment out if no standardisation is required

            # normalised = preprocessing.normalize(array, norm='l2') # Comment out if no normalisation is required
            # new_tensor = torch.from_numpy(normalised) # Comment out if no normalisation is required

            # new_tensor = torch.from_numpy(array) # Comment out if running standardisation or normalisation

            # ------------------------------------------------------------------------------------------------ #

            """New method of standardisation - divide through by the biggest distance in the sample set, which is 313"""

            new_tensor = holder / 313

            # Take the upper triangle by running through each value of the flattened tensor and selecting only the non zero values
            # and appending the non zero values into a new list. Will then convert the list to a torch tensor

            upper_triangle = torch.triu(new_tensor, diagonal=1)
            flat = torch.flatten(upper_triangle)

            non_zero = []
            non_zero.clear()
            for i in flat:
                if i == 0:
                    pass
                else:
                    non_zero.append(i)

            up = torch.tensor(non_zero, dtype=torch.float64)

            # Pad the tensor

            target_tensor_dimension = int(self.tensor_dimension * (self.tensor_dimension - 1)/2)
            pad = target_tensor_dimension - up.shape[0]

            self.padded = nn.ConstantPad1d((0, pad), 0)(up)

        return self.padded

    def save_file(self):
        with open(self.destination_path + self.name.split('_')[0] + '_labels.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.padded, file, protocol=4) # Save as a pickle object
