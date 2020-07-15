import os
from tqdm import tqdm

from adjacency_matrix import AdjacencyMatrix

import argparse

import torch

parser = argparse.ArgumentParser(description='To set to the path to the data')
parser.add_argument('-s', '--source_path', help='An input path where the data is located', required=True) # Location of the amino acid tags
parser.add_argument('-d', '--destination_path', help='An output path to save the statistics', required=True)
parser.add_argument('-t', '--mat_type', help='The type of matrix requested, choose from fully_connected, direct neighbour or nearest neighbour', required=True)
parser.add_argument('-r', '--radius', type=int, help='Define the radius of nearest neighbours', required=False)
parser.add_argument('-z', '--tensor_dimension', type=int, help='The padding factor to bring all tensors to the same dimension', required=True)

args = parser.parse_args()

source_path = args.source_path
destination_path = args.destination_path
mat_type = args.mat_type
radius = args.radius
tensor_dimension = args.tensor_dimension

start_tensor = torch.Tensor([0, 1, 0])
end_tensor = torch.Tensor([0, 1, 0])

def main(source_path, destination_path, mat_type, tensor_dimension):
    for root, dirs, files in os.walk(source_path, topdown=False):
        for name in tqdm(files):
            adj = AdjacencyMatrix(source_path, destination_path, name.split('_')[0], mat_type, tensor_dimension)
            if mat_type == 'fully_connected':
                adj.fully_connected()
                adj.pad()
                adj.save_file()
            elif mat_type == 'direct_neighbour':
                adj.direct_neighbour()
                adj.save_file()
            elif mat_type == 'nearest_neighbour':
                adj.nearest_neighbour(radius)
                adj.save_file_nearest(radius)

if __name__ == '__main__':
    main(source_path, destination_path, mat_type, tensor_dimension)