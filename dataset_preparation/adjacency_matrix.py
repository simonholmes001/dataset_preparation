import torch
torch.cuda.empty_cache()
device = torch.device('cuda')

class AdjacencyMatrix

    def __init__(self, source_path, destination_path, name, mat_type):
        self.source_path = source_path
        self.name = name
        self.destination_path = destination_path
        self.mat_type = mat_type # Indicates type of adjacency matrix, fully connected, direct neighbour or nearest neighbours

    def fully_connected(self):
        """
        :return:
        """
        with open(source_path + name) as f:
            count = sum(1 for line in f)
            x = torch.zeros((count, count), device=device)
            y = torch.ones((count, count), device=device)
            self.z = torch.add(x,y)
            self.z = torch.triu(self.z, diagonal=1)

        return self.z

    def save_file(self):
        try:
            with open(self.destination_path + '/' + self.name.split('.')[0] + '- ' + self.mat_type + '_.pickle', 'wb', buffering=500000000) as file:
                pickle.dump(self.z, file, protocol=4) # Save as a pickle object
        except:
            pass

