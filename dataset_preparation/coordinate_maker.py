import os

import torch
from torch import nn
import numpy as np
import pickle

import seaborn as sns
import matplotlib.pyplot as plt

import distance_heatmap
from distance_heatmap.distance_heatmap import Heatmap

from golden_triangle.GoldenTriangle import golden_triangle

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import argparse

parser = argparse.ArgumentParser(description='Construct 3 dimensional coordinates from model output')
parser.add_argument('-i', '--input_path', help='The input path containing files to be analysed - model output', required=True) 
parser.add_argument('-z', '--tensor_dimension', type=int, help='The tensor size', required=True)
parser.add_argument('-d', '--distance_matrix', help='The input path of the original distance matrix, before preprocessing, if known, type n if not available', required=True)

args = parser.parse_args()

input_path = args.input_path
tensor_dimension = args.tensor_dimension
"""
The distance_matrix variable must be given as a pickle object containing a pytorch tensor and in the format: '/media/the_beast/B/mathisi_tests/data/closed_dataset/distance_matrix/7abp_label.pickle'
If not available, type n
"""
distance_matrix = args.distance_matrix 

class CoordinateMaker:

    def __init__(self, input_path, tensor_dimension, distance_matrix):

        self.input_path = input_path
        self.tensor_dimension = tensor_dimension
        self.distance_matrix = distance_matrix

    def import_data(self):

        print("Loading data...")

        with open(self.input_path, 'rb') as labels_file:
            tensor = pickle.load(labels_file)

        # Remove the padding that was given during data processing

        print("Removing padding...")

        non_zero = []
        non_zero.clear()
        for i in tensor:
            if i == 0:
                pass
            else:
                non_zero.append(i)

        self.non_zero_tensor = torch.tensor(non_zero, dtype=torch.float64)

        for n in range(0,self.z):
            while golden_triangle(n) != self.non_zero_tensor.shape[0]:
                print("Waiting...")
                if golden_triangle(n) == self.non_zero_tensor.shape[0]:
                    self.span = n
            
        return self.non_zero_tensor, self.span


    def build_distance_map(self):

        """
        Returns a reconstructured distance map from the model's output
        """
       
        # Once you have the value of n, set the variable span to this value
        # This code will tag the flattened matrix at what should be the non zero entries. In the next step, the non zero
        # entries will be populated by the values from the model output (or test flattened dstance matrix in this example)
        
        print("Constructing distance map...")

        holder = torch.flatten(torch.zeros(self.span, self.span)) # Create an empty matrix & flatten, of the correct dimension of n
        counter = 0 
        while counter <= self.span:
            for s in range(int(self.span**2 / self.span)): # Was divded by 4, changed to span
                s = s + self.span * counter
                if s == holder.shape[0]:
                    break
                if s % self.span == 0:
                    holder[s] = 0
                elif s % self.span <= counter:
                    holder[s] = 0
                else:
                    try:
                        holder[s] = 5
                    except:
                        pass
            s += 1
            counter += 1

        # Replaces the non zero entries of the flattened matrix that will reconsitute the distance matrix using the
        # values from the model output

        counter_2 = 0
        for num in range(holder.shape[0]):
            if holder[num] == 5:
                holder[num] = non_zeroed[counter_2]
                counter_2 += 1

        # Reconstitute the distance matrix

        print("Building distance map...")

        unflattened = torch.reshape(holder, (self.span, self.span))
        triangle = unflattened.T
        self.distance_map_reconstructed = unflattened + triangle
        
        return self.distance_map_reconstructed

    def calculate_coordinates(self):

        """
        numpy implementation before trying with pytorch
        """

        print("Building 3 dimensional coordinates...")

        distance_map_resonstructed_array = self.distance_map_reconstructed.numpy()

        structure = np.zeros(distance_map_resonstructed_array.shape)
        for i in range(0,distance_map_resonstructed_array.shape[0]):
            for j in range(0,distance_map_resonstructed_array.shape[1]):
                structure[i,j] = 1/2 * (distance_map_resonstructed_array[i,0]**2 + 
                                        distance_map_resonstructed_array[0,j]**2 - 
                                        distance_map_resonstructed_array[i,j]**2)

        w, v = np.linalg.eigh(structure)
        nb_components = 3 # 3D
        self.coordinate_matrix = np.matmul(v[:,-nb_components:], np.diag(np.sqrt(w[-nb_components:])))

        return self.coordinate_matrix

    def control_distance_heatmap(self, distance_matrix):
        
        coordinate_matrix_distances = distance.pdist(self.coordinate_matrix, 'euclidean')
        coordinate_matrix_distance_map = distance.squareform(coordinate_matrix_distances)

        # Plot the heatmaps

        print("Heatmap of original protein...")

        if self.distance_matrix == 'n':
            pass
        else:
            heat = Heatmap(self.distance_matrix)
            heat.loader()
            heat.make_distance_map()


        print("Heatmap of model output...")

        plt.figure(figsize = (15,7.5))
        ax = sns.heatmap(distance_map_reconstructed)
        plt.show()


        print("Heatmap derived from the distance map of the reconstructed 3 dimensional coordinates...")

        plt.figure(figsize = (15,7.5))
        ax = sns.heatmap(coordinate_matrix_distance_map)
        plt.show()

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

def main(input_path, tensor_dimension, distance_matrix):
    coordinates = CoordinateMaker(input_path, tensor_dimension, distance_matrix)
    coordinates.input_data()
    coordinates.build_distance_map()
    coordinates.calculate_coordinates()
    coordinates.control_distance_heatmap()
    coordinates.prepare_for_view()
    


if __name__ == '__main__':
    main(input_path, tensor_dimension, distance_matrix)