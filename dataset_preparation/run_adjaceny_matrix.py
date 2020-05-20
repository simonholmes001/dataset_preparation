import os
from tqdm import tqdm

from adjacency_matrix import AdjacencyMatrix

import argparse

parser = argparse.ArgumentParser(description='To set to the path to the data')
parser.add_argument('-s', '--source_path', help='An input path where the data is located', required=True)
parser.add_argument('-d', '--destination_path', help='An output path to save the statistics', required=True)
parser.add_argument('-t', '--mat_type', help='The type of matrix requested, choose from fully_connected, direct neighbour or nearest neighbour', required=True)
parser.add_argument('-r', '--radius', help='Define the radius of nearest neighbours', required=False)

args = parser.parse_args()

source_path = args.source_path
destination_path = args.destination_path
mat_type = args.mat_type
radius = args.radius

def main(source_path, destination_path, mat_type):
    for root, dirs, files in os.walk(source_path, topdown=False):
        for name in tqdm(files):
            adj = AdjacencyMatrix(source_path, destination_path, name.split('_')[0], mat_type)
            if mat_type == 'fully_connected':
                adj.fully_connected()
                adj.save_file()

if __name__ == '__main__':
    main(source_path, destination_path, mat_type)