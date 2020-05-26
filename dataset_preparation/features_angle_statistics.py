import numpy as np
import pandas as pd

import argparse

parser = argparse.ArgumentParser(description='To set to the path to the data')
parser.add_argument('-p', '--path', help='An input path where the data is located & will be saved', required=True)
parser.add_argument('-c', '--code', help='The one-hot encoded amino acid code, must be given as a flaot, for example, 1.0, 5.0', required=True)
parser.add_argument('-n', '--name', help='The maino acid three-letter namde', required=True)
parser.add_argument('-t', '--tag', help='The pubchem code for the amino acid', required=True)

args = parser.parse_args()

path = args.path
code = args.code
name = args.name
tag = args.tag

phi_statistics = 'phi_all_proteins.csv'
psi_statistics = 'psi_all_proteins.csv'

print("Loading files...")
print("Loading phi...")
df_phi = pd.read_csv(path + phi_statistics, header=None, names=['amino acids', 'phi'])
print("Loading psi...")
df_psi = pd.read_csv(path + psi_statistics, header=None, names=['amino acids', 'psi'])

array = [code]
print("Loading phi for amino acid {}...".format(name))
df_phi_angle_statistics = df_phi.loc[df_phi['amino acids'].isin(array)]
print("Loading psi for amino acid {}...".format(name))
df_psi_angle_statistics = df_psi.loc[df_psi['amino acids'].isin(array)]

print("Loading phi_describe for amino acid {}...".format(name))
phi = df_phi_angle_statistics['phi'].describe()
print("Loading psi_describe for amino acid {}...".format(name))
psi = df_psi_angle_statistics['psi'].describe()

print("Joining phi & psi for amino acid {}...".format(name))
df = pd.concat([phi, psi], axis=1)
df = df.drop(df.index[[0, 3, 7]])
df = df.transpose()
df = pd.concat([df, df], axis=1)
df = df.drop(df.index[1])
df = df.rename(index={'phi':tag})
print(df)
print("Saving dataframe for amino acid {}...".format(name))
df.to_csv(path + '/' + name + '_features.csv', encoding='utf-8')



