import os
from tqdm import tqdm

from distance_matrix import DistanceMatrix

import argparse

parser = argparse.ArgumentParser(description='To set to the path to the data')
parser.add_argument('-s', '--source_path', help='An input path where the data is located', required=True)
parser.add_argument('-d', '--destination_path', help='An output path to save the statistics', required=True)
parser.add_argument('-z', '--tensor_dimension', help='The tensor dimension to pad all tensors to', required=True)
parser.add_argument('-z', '--tensor_dimension', help='The tensor dimension to pad all tensors to', required=True)

args = parser.parse_args()

source_path = args.source_path
destination_path = args.destination_path
tensor_dimension = args.tensor_dimension

def main(source_path, destination_path, tensor_dimension):
    for root, dirs, files in os.walk(source_path, topdown=False):
        for name in tqdm(files):
            dis = DistanceMatrix(source_path, destination_path, name.split('_')[0], tensor_dimension)
            dis.flatten_distance_matrix()
            dis.save_file()

if __name__ == '__main__':
    main(source_path, destination_path, tensor_dimension)