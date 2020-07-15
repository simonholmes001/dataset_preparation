import os
import pandas as pd
from tqdm import tqdm
import shutil

import argparse

"""
DON'T FORGET TO CHANGE THE PATHS!!!!!!!
"""

parser = argparse.ArgumentParser(description='Dataset Pipeline')
parser.add_argument('-i', '--input_path', help='The input path containing the amino acid tags of the proteins downloaded from the PDB', required=True) # Source for the amino acid tags
parser.add_argument('-p', '--check_path', help='The path containing the train dataset, required only for creating the test dataset', required=False)
parser.add_argument('-l', '--target_length', type=int, help='The upper limit of protein size', required=True)
parser.add_argument('-s', '--dataset_size', type=int, help='Size of dataset to prepare', required=True)
parser.add_argument('-m', '--model_type', help='Type of dataset to prepare, train or test', required=True)

# INPUT_PATH IS ALWAYS /media/the_beast/disk/protein_folding/amino_acid_tags/

args = parser.parse_args()

input_path = args.input_path
check_path = args.check_path
target_length = args.target_length
dataset_size = args.dataset_size
model_type = args.model_type


class DataPipeline:

    def __init__(self, input_path,target_length, dataset_size, model_type):
        self.input_path = input_path
        self.target_length = target_length
        self.dataset_size = dataset_size
        self.model_type = model_type

    def create_train_dataset(self):

        self.counter = []
        self.tag = []
        self.tag.clear()
        self.counter.clear()

        for root, dirs, files in os.walk(self.input_path, topdown=False):
            for name in tqdm(files):
                with open(self.input_path + name) as f:
                    count = sum(1 for line in f)
                    if count != 0:
                        if len(self.counter) > self.dataset_size - 1:
                            break
                        else:
                            if count <= self.target_length:
                                self.counter.append(count)
                                self.tag.append(name.split('_')[0])
                                print("{} {}".format(name.split('_')[0], count))
                                print(f"Length of the dataset is currently: {len(self.tag)}")
        print(self.tag)
        print(f"Dataset size is: {len(self.tag)}\n")

        return self.tag, self.counter

    def create_test_dataset(self, check_path):

        self.counter = []
        self.tag = []
        self.tag.clear()
        self.counter.clear()
        duplicate_list = []
        duplicate_list.clear()

        print("Preparing duplicate list...")
        for root, dirs, files in os.walk(check_path, topdown=False):
            for name in tqdm(files):
                duplicate_list.append(name.split('_')[0])

        print("Preparing test dataset...")
        for root, dirs, files in os.walk(self.input_path, topdown=False):
            for name in tqdm(files):
                if name.split('_')[0] in duplicate_list:
                    pass
                else:
                    with open(self.input_path + name) as f:
                        count = sum(1 for line in f)
                        if count != 0:
                            if len(self.counter) > self.dataset_size - 1:
                                break
                            else:
                                if count <= self.target_length:
                                    self.counter.append(count)
                                    self.tag.append(name.split('_')[0])
                                    print("{} {}".format(name.split('_')[0], count))
                                    print(f"Length of the dataset is currently: {len(self.tag)}")
        print(self.tag)
        print(f"Dataset size is: {len(self.tag)}\n")

        return self.tag, self.counter

    def dataset_statistics(self):

        df2 = pd.DataFrame(data=self.counter, columns=['length'])
        df3 = pd.DataFrame(data=self.tag, columns=['name'])
        df4 = pd.concat([df3, df2], axis=1)

        print(f"Dataset statistics:\n {df4['length'].describe()}")

    def prepare_train_set(self):

        tag_destination = '/media/the_beast/A/mathisi_tests/data/tags/'
        label_input_path = '/media/the_beast/disk/protein_folding/pickle_files/pickle_label_gz/'
        distance_destination = '/media/the_beast/A/mathisi_tests/data/distance_matrix/'
        features_input_path = '/media/the_beast/disk/protein_folding/pickle_files/pickle_features_gz/'
        features_destination = '/media/the_beast/A/mathisi_tests/data/features/'

        for t in self.tag:
            shutil.copy(self.input_path + t + '_amino_acid_tag_.csv', tag_destination)

        for t in self.tag:
            try:
                shutil.copy(label_input_path + t + '_label.pickle.gz', distance_destination)
            except:
                print(f"Distance file NOK: {t}")
                pass

        for t in self.tag:
            try:
                shutil.copy(features_input_path + t + '_feature.pickle.gz', features_destination)
            except:
                print(f"Feature file NOK: {t}")
                pass

    def prepare_test_set(self):

        tag_destination = '/media/the_beast/A/mathisi_tests/data/testset/tags/'
        label_input_path = '/media/the_beast/disk/protein_folding/pickle_files/pickle_label_gz/'
        distance_destination = '/media/the_beast/A/mathisi_tests/data/testset/distance_matrix/'
        features_input_path = '/media/the_beast/disk/protein_folding/pickle_files/pickle_features_gz/'
        features_destination = '/media/the_beast/A/mathisi_tests/data/testset/features/'

        for t in self.tag:
            shutil.copy(self.input_path + t + '_amino_acid_tag_.csv', tag_destination)

        for t in self.tag:
            try:
                shutil.copy(label_input_path + t + '_label.pickle.gz', distance_destination)
            except:
                print(f"Distance file NOK: {t}")
                pass

        for t in self.tag:
            try:
                shutil.copy(features_input_path + t + '_feature.pickle.gz', features_destination)
            except:
                print(f"Feature file NOK: {t}")
                pass

def main(input_path, target_length, dataset_size, model_type):
    datapipe = DataPipeline(input_path, target_length, dataset_size, model_type)
    if model_type == 'train':
        datapipe.create_train_dataset()
        datapipe.dataset_statistics()
        datapipe.prepare_train_set()
    else:
        datapipe.create_test_dataset(check_path)
        datapipe.dataset_statistics()
        datapipe.prepare_test_set()

if __name__ == '__main__':
    main(input_path, target_length, dataset_size, model_type)