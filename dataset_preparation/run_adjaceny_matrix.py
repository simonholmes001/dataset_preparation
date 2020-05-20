from tqdm import tqdm

from .adjacency_matrix import AdjacencyMatrix















def main(source_path, destination_path, mat_type):
    for root, dirs, files in os.walk(source_path, topdown=False):
        for name in tqdm(files):
            adj = AdjacencyMatrix(source_path, destination_path, name.split('_')[0], mat_type)
            if mat_type == fully_connected
                stats.open_files()
            stats.collect_statistics()
            stats.save_statistics()

if __name__ == '__main__':
    main(source_path, destination_path, mat_type)