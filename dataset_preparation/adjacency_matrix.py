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
        Takes the amino acid tag files (files containend the primary sequence of the amino acids & counts the length of the amino acids. Creates an
        adjacency matrix based on the length of the protein. If n amino acids then the adjacency matrix is n x n. Adjacency matrix can be either:
        fully connected -> considers that every amino acid is connected to every other amino acid
        direct neighbour -> the adjacency matrix reflects that physiccal connection between amino acids so only between amino acid n, n-1 & n+1
        nearest neighbours -> a radius is given that will connect each amino acid to all of its neighbours within a given radius
        :return: fully connected adjacency matrix as a pytorch tensor
        """
        with open(self.source_path + self.name + '_amino_acid_tag_.csv') as f:
            count = sum(1 for line in f)
            x = torch.eye(count)
            y = torch.ones((count, count))
            self.z = torch.sub(y,x)
            print(self.z)

        return self.z

    def direct_neighbour(self):
        """
        Takes the amino acid tag files (files containend the primary sequence of the amino acids & counts the length of the amino acids. Creates an
        adjacency matrix based on the length of the protein. If n amino acids then the adjacency matrix is n x n. Adjacency matrix can be either:
        fully connected -> considers that every amino acid is connected to every other amino acid
        direct neighbour -> the adjacency matrix reflects that physiccal connection between amino acids so only between amino acid n, n-1 & n+1
        nearest neighbours -> a radius is given that will connect each amino acid to all of its neighbours within a given radius
        :return: fully connected adjacency matrix as a pytorch tensor
        """
        start = torch.Tensor([0, 1, 0])
        end = torch.Tensor([0, 1, 0])
        padding_range = self.tensor_dimension - 3
        padding = torch.zeros((padding_range))
        sos = torch.cat((start, padding),0)
        eos = torch.cat((padding, end),0)
        identity = torch.eye(self.tensor_dimension)
        tensor_list = []
        tensor_list.append(sos)
        shaper = identity.shape[0]

        with open(self.source_path + self.name + '_amino_acid_tag_.csv') as f:
            for shape in range(shaper-2):
                print(self.name)
                row = identity[shape] + identity[shape+2]
                tensor_list.append(row)
            tensor_list.append(eos)
            self.adj = torch.stack(tensor_list)

        return self.adj

    def nearest_neighbour(self, radius):
        """
        Takes the amino acid tag files (files containend the primary sequence of the amino acids & counts the length of the amino acids. Creates an
        adjacency matrix based on the length of the protein. If n amino acids then the adjacency matrix is n x n. Adjacency matrix can be either:
        fully connected -> considers that every amino acid is connected to every other amino acid
        direct neighbour -> the adjacency matrix reflects that physiccal connection between amino acids so only between amino acid n, n-1 & n+1
        nearest neighbours -> a radius is given that will connect each amino acid to all of its neighbours within a given radius
        :return: fully connected adjacency matrix as a pytorch tensor
        """

        radius_set = [4, 6, 8]

        padding_range = self.tensor_dimension - radius
        padding = torch.zeros((padding_range))

        identity = torch.eye(self.tensor_dimension)

        if radius not in radius_set:
            print(f"Radius choice of {radius}, please choose again. Radius must be either 4, 6 or 8. Please choose a number from that list")
        else:
            if radius == 4:
                start = torch.ones(radius)
                start[0] = start[0] - 1
                start[3] = start[3] - 1

                start_1 = torch.ones(radius)
                start_1[1] = start_1[1] - 1

                end = torch.ones(radius)
                end[0] = end[0] - 1
                end[3] = end[3] - 1

                end_1 = torch.ones(radius)
                end_1[2] = end_1[2] - 1


                sos = torch.cat((start, padding),0)
                sos_1 = torch.cat((start_1, padding),0)
                eos = torch.cat((padding, end),0)
                eos_1 = torch.cat((padding, end_1),0)

            if radius == 6:
                start = torch.ones(radius)
                start[0] = start[0] - 1
                start[4] = start[4] - 1
                start[5] = start[5] - 1

                start_1 = torch.ones(radius)
                start_1[1] = start_1[1] - 1
                start_1[5] = start_1[5] - 1

                start_2 = torch.ones(radius)
                start_2[2] = start_2[2] - 1

                end = torch.ones(radius)
                end[0] = end[0] - 1
                end[1] = end[1] - 1
                end[5] = end[5] - 1

                end_1 = torch.ones(radius)
                end_1[0] = end_1[0] - 1
                end_1[4] = end_1[4] - 1

                end_2 = torch.ones(radius)
                end_2[3] = end_2[3] - 1

                sos = torch.cat((start, padding),0)
                sos_1 = torch.cat((start_1, padding),0)
                sos_2 = torch.cat((start_2, padding),0)
                eos = torch.cat((padding, end),0)
                eos_1 = torch.cat((padding, end_1),0)
                eos_2 = torch.cat((padding, end_2),0)

            if radius == 8:
                start = torch.ones(radius)
                start[0] = start[0] - 1
                start[5] = start[5] - 1
                start[6] = start[6] - 1
                start[7] = start[7] - 1

                start_1 = torch.ones(radius)
                start_1[1] = start_1[1] - 1
                start_1[6] = start_1[6] - 1
                start_1[7] = start_1[7] - 1

                start_2 = torch.ones(radius)
                start_2[2] = start_2[2] - 1
                start_2[7] = start_2[7] - 1

                start_3 = torch.ones(radius)
                start_3[3] = start_3[3] - 1

                end = torch.ones(radius)
                end[0] = end[0] - 1
                end[1] = end[1] - 1
                end[2] = end[2] - 1
                end[7] = end[7] - 1

                end_1 = torch.ones(radius)
                end_1[0] = end_1[0] - 1
                end_1[1] = end_1[1] - 1
                end_1[6] = end_1[6] - 1

                end_2 = torch.ones(radius)
                end_2[0] = end_2[0] - 1
                end_2[5] = end_2[5] - 1

                end_3 = torch.ones(radius)
                end_3[4] = end_3[4] - 1

                sos = torch.cat((start, padding),0)
                sos_1 = torch.cat((start_1, padding),0)
                sos_2 = torch.cat((start_2, padding),0)
                sos_3 = torch.cat((start_3, padding),0)
                eos = torch.cat((padding, end),0)
                eos_1 = torch.cat((padding, end_1),0)
                eos_2 = torch.cat((padding, end_2),0)
                eos_3 = torch.cat((padding, end_3),0)

        tensor_list = []
        tensor_list.clear()
        tensor_list.append(sos)

        if radius == 4:
            tensor_list.append(sos_1)
        if radius == 6:
            tensor_list.append(sos_1)
            tensor_list.append(sos_2)
        if radius == 8:
            tensor_list.append(sos_1)
            tensor_list.append(sos_2)
            tensor_list.append(sos_3)

        shaper = identity.shape[0]


        with open(self.source_path + self.name + '_amino_acid_tag_.csv') as f:
            for shape in range(shaper-radius):
                if radius == 4:
                    row = identity[shape] + identity[shape+1] + identity[shape+3] + identity[shape+4]
                elif radius == 6:
                    row = identity[shape] + identity[shape+1] + identity[shape+2] + identity[shape+4] + identity[shape+5] + identity[shape+6]
                elif radius == 8:
                    row = identity[shape] + identity[shape+1] + identity[shape+2] + identity[shape+3] + identity[shape+5] + identity[shape+6] + identity[shape+7] + identity[shape+8]
                tensor_list.append(row)

            if radius == 4:
                tensor_list.append(eos_1)
                tensor_list.append(eos)

            if radius == 6:
                tensor_list.append(eos_2)
                tensor_list.append(eos_1)
                tensor_list.append(eos)

            if radius == 8:
                tensor_list.append(eos_3)
                tensor_list.append(eos_2)
                tensor_list.append(eos_1)
                tensor_list.append(eos)

            self.adj = torch.stack(tensor_list)

        return self.adj


    def pad(self):
        q = self.z.shape
        print("The shape of {} is {} by {}".format(self.name.split('_')[0], q[0], q[1]))
        down_pad = self.tensor_dimension - q[0]
        right_pad = self.tensor_dimension - q[1]
        print("The down padding is: {}".format(down_pad))
        print("The right padding is: {}".format(right_pad))
        m = torch.nn.ZeroPad2d((0,right_pad,0,down_pad))
        self.adj = m(self.z)
        print("Final shape of {} is: {}".format(self.name.split('_')[0], self.adj.shape))

        return self.adj

    def save_file(self):
        with open(self.destination_path + self.name.split('_')[0] + '_' + 'adjacency-matrix.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.adj, file, protocol=4) # Save as a pickle object

    def save_file_nearest(self, radius):
        with open(self.destination_path + self.name.split('_')[0] + '_' + 'adjacency-matrix.pickle', 'wb', buffering=500000000) as file:
            pickle.dump(self.adj, file, protocol=4) # Save as a pickle object


    # def save_file(self):
    #     with open(self.destination_path + self.mat_type + self.name.split('_')[0] + '_' + 'adjacency-matrix.pickle', 'wb', buffering=500000000) as file:
    #         pickle.dump(self.adj, file, protocol=4) # Save as a pickle object
    #
    # def save_file_nearest(self, radius):
    #     with open(self.destination_path + self.mat_type + '_' + str(radius) + self.name.split('_')[0] + '_' + 'adjacency-matrix.pickle', 'wb', buffering=500000000) as file:
    #         pickle.dump(self.adj, file, protocol=4) # Save as a pickle object