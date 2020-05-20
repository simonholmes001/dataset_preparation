import torch
torch.cuda.empty_cache()
# device = torch.device('cuda')

import pickle

class AdjacencyMatrix:
    """
    Create difference types of adjaceny matrix: fully connected, direct neighbour or nearest neighbours
    """

    def __init__(self, source_path, destination_path, name, mat_type):
        self.source_path = source_path
        self.name = name
        self.destination_path = destination_path
        self.mat_type = mat_type # Indicates type of adjacency matrix, fully connected, direct neighbour or nearest neighbours

    def fully_connected(self):
        """
        :return:
        """
        with open(self.source_path + '/' + self.name + '_amino_acid_tag_.csv') as f:
            count = sum(1 for line in f)
            x = torch.eye(count)
            y = torch.ones((count, count))
            self.z = torch.sub(y,x)
            print(self.z)

        return self.z

    # def save_file(self):
    #     torch.save(self.z, self.destination_path + '/' + self.mat_type + '/' + self.name.split('.')[0] + '_' + self.mat_type + '.pt')


    def save_file(self):
        with open(self.destination_path + '/' + self.mat_type + '/' + self.name.split('_')[0] + '_' + self.mat_type + '.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.z, file, protocol=4) # Save as a pickle object
