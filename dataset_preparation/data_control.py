import os
import pandas as pd
from tqdm import tqdm

import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

import argparse

parser = argparse.ArgumentParser(description='Dataset Pipeline')
parser.add_argument('-i', '--input_path', help='The input path containing files to be controlled', required=True) # Source for the amino acid tags
parser.add_argument('-z', '--tensor_dimension', type=int, help='The tensor size', required=True)

args = parser.parse_args()

input_path = args.input_path
tensor_dimension = args.tensor_dimension

class DataControl:

    def __init__(self, input_path, tensor_dimension):
        self.input_path = input_path
        self.tensor_dimension = tensor_dimension

    def control_dimension(self):

        print("Controlling tensor dimensions...")
        tensors_to_delete = []
        tensors_to_delete.clear()
        for root, dirs, files in os.walk(self.input_path, topdown=False):
            for name in tqdm(files):
                if 'adjacency' in name:
                    try:
                        with open(self.input_path + name, 'rb') as labels_file:
                            df1 = pd.read_pickle(labels_file)
                            if df1.shape[0] != self.tensor_dimension or df1.shape[1] != self.tensor_dimension:
                                print(f"{name.splt('_')[0]} is not of the correct dimension for an adjacency matrix")
                                tensors_to_delete.append(name)
                    except:
                        print(f"{name} has an issue")
                        tensors_to_delete.append(name)
                        pass
                elif 'features' in name:
                    try:
                        with open(self.input_path + name, 'rb') as labels_file:
                            df2 = pd.read_pickle(labels_file)
                            if df2.shape[0] != self.tensor_dimension or df2.shape[1] != 58: # Hard code second dimension of the features tensor
                                print(f"{name.splt('_')[0]} is not of the correct dimension for a features matrix")
                                tensors_to_delete.append(name)
                    except:
                        print(f"{name} has an issue")
                        tensors_to_delete.append(name)
                        pass
                elif 'labels' in name:
                    try:
                        with open(self.input_path + name, 'rb') as labels_file:
                            df3 = pd.read_pickle(labels_file)
                            if df3.shape[0] != self.tensor_dimension * (self.tensor_dimension - 1) / 2:
                                print(f"{name.splt('_')[0]} is not of the correct dimension for a labels matrix")
                                tensors_to_delete.append(name)
                    except:
                        print(f"{name} has an issue")
                        tensors_to_delete.append(name)
                        pass

        if len(tensors_to_delete) == 0:
            print("There are no tensors to delete")
        else:
            print(f"{len(tensors_to_delete)} tensors must be deleted")

        if len(tensors_to_delete) != 0:
            print("Deleting tensors")
            for name in tensors_to_delete:
                try:
                    os.remove(self.input_path + name)
                except:
                    pass
        print("All non valid tensor dimensions now deleted")


    def control_nan(self):

        print("Controlling features with nan, this could take some time...")
        files_to_delete = []
        files_to_delete.clear()
        for root, dirs, files in os.walk(self.input_path, topdown=False):
            for name in tqdm(files):
                if 'feature' in name:
                    with open(self.input_path + name, 'rb') as labels_file:
                        df = pd.read_pickle(labels_file).to(device)
                        df_flat = torch.flatten(df)
                        for i in df_flat.to(device):
                            if torch.isnan(i) == True:
                                files_to_delete.append(name)

        file_counter = {}
        for file in files_to_delete:
            file_count = files_to_delete.count(file)
            file_counter.update({file:file_count})

        print("Deleting feature files containing nan...")
        for key, value in file_counter.items():
            try:
                os.remove(self.input_path + key)
            except:
                pass
        print("All feature files containing nan are now deleted")

    def control_presence(self):

        print("Controlling that three files per protein are present (adjacency, features, labels)...")

        tag_list = []
        tag_list.clear()
        for root, dirs, files in os.walk(self.input_path, topdown=False):
            for name in tqdm(files):
                tag_list.append(name.split('_')[0])

        tag_counter = {}
        for tag in tag_list:
            tag_count = tag_list.count(tag)
            tag_counter.update({tag:tag_count})

        key_list = []
        key_list.clear()
        for key, value in tag_counter.items():
            if value != 3:
                key_list.append(key)

        for root, dirs, files in os.walk(self.input_path, topdown=False):
            for name in tqdm(files):
                if name.split('_')[0] in key_list:
                    try:
                        os.remove(self.input_path + name.split('_')[0] + '_adjacency-matrix.pickle')
                    except:
                        pass
                    try:
                        os.remove(self.input_path + name.split('_')[0] + '_features.pickle')
                    except:
                        pass
                    try:
                        os.remove(self.input_path + name.split('_')[0] + '_labels.pickle')
                    except:
                        pass

        print("Script complete")

def main(input_path, tensor_dimension):
    control = DataControl(input_path, tensor_dimension)
    control.control_dimension()
    control.control_nan()
    control.control_presence()

if __name__ == '__main__':
    main(input_path, tensor_dimension)