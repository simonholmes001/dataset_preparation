import os

import torch
import numpy as np
import pickle

class CoordinateMaker:

    def __init__(self):
        pass

    def build_distance_map(self):
        pass
        # return self.distance_map_reconstructed

    def calculate_coordinates(self):

        """
        numpy implementation before trying with pytorch
        """

        structure = np.zeros(self.distance_map_reconstructed.shape)
        for i in range(0,self.distance_map_reconstructed.shape[0]):
            for j in range(0,self.distance_map_reconstructed.shape[1]):
                structure[i,j] = 1/2 * (self.distance_map_reconstructed[i,0]**2 + 
                                        self.distance_map_reconstructed[0,j]**2 - 
                                        self.distance_map_reconstructed[i,j]**2)

        w, v = np.linalg.eigh(structure)
        nb_components = 3 # 3D
        self.coordinate_matrix = np.matmul(v[:,-nb_components:], np.diag(np.sqrt(w[-nb_components:])))

        return self.coordinate_matrix

    def control_distance_heatmap(self):
        
        coordinate_matrix_distances = distance.pdist(self.coordinate_matrix, 'euclidean')
        coordinate_matrix_distance_map = distance.squareform(coordinate_matrix_distances)

        """
        Need to add-in code to display the heatmaps along with the original distance map
        Optional if original distance map exists -> will also need to add in variables for this
        as inputs to the method
        """

    def prepare_for_view(self):
        pass
        """
        Write code to transform the constructed coordinate_matrix into a mmCIF file for viewing
        in Jmol or some other molecular viewing software
        Ouput will be a mmCIF file
        """

def main():
    coordinates = CoordinateMaker()
    if model_type == 'train':
        datapipe.create_train_dataset(lower_limit)
        datapipe.dataset_statistics()
        datapipe.prepare_train_set()
    else:
        datapipe.create_test_dataset(lower_limit, check_path)
        datapipe.dataset_statistics()
        datapipe.prepare_test_set()

if __name__ == '__main__':
    main(input_path, upper_limit, dataset_size, model_type)