import torch
torch.cuda.empty_cache()
# device = torch.device('cuda')

import pickle

class AdjacencyMatrix:
    """
    Create difference types of adjaceny matrix: fully connected, direct neighbour or nearest neighbours
    """

    def __init__(self, source_path, destination_path, name, mat_type, tensor_dimension):
        self.source_path = source_path
        self.name = name
        self.destination_path = destination_path
        self.mat_type = mat_type # Indicates type of adjacency matrix, fully connected, direct neighbour or nearest neighbours
        self.tensor_dimension = tensor_dimension # Indicates the padding factor to bring all tensors to the same dimension

    def fully_connected(self):
        """
        Takes the amino acid tag files (files containind the primary sequence of the amino acids & counts the length of the amino acids. Creates an
        adjacency matrix based on the length of the protein. If n amino acids then the adjacency matrix is n x n. Adjacency matrix can be either:
        fully connected -> considers that every amino acid is connected to every other amino acid
        direct neighbour -> the adjacency matrix reflects that physiccal connection between amino acids so only between amino acid n, n-1 & n+1
        nearest neighbours -> a radius is given that will connect each amino acid to all of its neighbours within a given radius
        :return: fully connected adjacency matrix as a pytorch tensor
        """
        with open(self.source_path + '/' + self.name + '_amino_acid_tag_.csv') as f:
            count = sum(1 for line in f)
            x = torch.eye(count)
            y = torch.ones((count, count))
            self.z = torch.sub(y,x)
            print(self.z)

        return self.z

    def pad(self):
        q = self.z.shape
        print("The shape of {} is {} by {}".format(self.name.split('_')[0], q[0], q[1]))
        down_pad = self.tensor_dimension - q[0]
        right_pad = self.tensor_dimension - q[1]
        print("The down padding is: {}".format(down_pad))
        print("The right padding is: {}".format(right_pad))
        m = torch.nn.ZeroPad2d((0,right_pad,0,down_pad))
        self.padded_tensor = m(self.z)
        print("Final shape of {} is: {}".format(self.name.split('_')[0], self.padded_tensor.shape))

        return self.padded_tensor

    def save_file(self):
        with open(self.destination_path + '/' + self.mat_type + '/' + self.name.split('_')[0] + '_' + 'adjacency-matrix.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.padded_tensor, file, protocol=4) # Save as a pickle object
