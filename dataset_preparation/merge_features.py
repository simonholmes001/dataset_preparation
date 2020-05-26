import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import argparse
import torch
import pickle

standardised_features_df = pd.read_csv('./standardised_features_2.csv')

# class Merge:
#
#     def __init__(self):
#         self.angle_df = angle.df

def get_features():

    for root, dirs, files in os.walk('/media/kovan_ai_tor_the_beast/hard_drive_1/DATA/output', topdown=False):
        for name in tqdm(files):
            if 'features' in name:
                angle_df = pd.read_csv('/media/kovan_ai_tor_the_beast/hard_drive_1/DATA/output/' + name, header=None)
                angle_df_2 = angle_df.rename(columns={0 :'CID'})
                angle_df_2.to_csv('/media/kovan_ai_tor_the_beast/hard_drive_2/TEST_DATA/' + name.split('_')[0] +  'features.csv', encoding='utf-8')

def main():
    get_features()

if __name__ == '__main__':
    main()

