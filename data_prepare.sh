#!/usr/bin/env bash

# Script to prepare the data for the message passing neural network

# REMEMBER TO UPDATE ALL OF THE DIRECTORY NAMES ### VERY IMPORTANT

echo Unpacking distance files...

bash unzip.sh /media/the_beast/A/mathisi_tests/data/transformed/testset/distance_matrix/

# echo Unpacking features files...

# bash unzip.sh /media/the_beast/A/mathisi_tests/data/features/

echo Preparing adjacency matrix data...

echo -n "Please enter an option for t, the adjacency matrix type: "
read t
if [ $t == "nearest_neighbour"  ]; then
    echo -n "Please enter an option for r, the radius: "
    read r
else
  echo "No need to enter a radius"
fi
echo -n "Please enter an option for z, the tensor dimension: "
read z

if [ $t == "nearest_neighbour"  ]; then
  python3 ./dataset_preparation/run_adjacency_matrix.py -s /media/the_beast/A/mathisi_tests/data/transformed/testset/tags/ -d /media/the_beast/A/mathisi_tests/data/transformed/testset/$t/ -t $t -r $r -z $z
else
  python3 ./dataset_preparation/run_adjacency_matrix.py -s /media/the_beast/A/mathisi_tests/data/transformed/testset/tags/ -d /media/the_beast/A/mathisi_tests/data/transformed/testset/$t/ -t $t -z $z
fi

echo Preparing distance matrix labels...

python3 ./dataset_preparation/run_distance_matrix.py -s /media/the_beast/A/mathisi_tests/data/transformed/testset/distance_matrix/ -d /media/the_beast/A/mathisi_tests/data/transformed/testset/$t/ -z $z

echo Preparing amino acid features

python3 ./dataset_preparation/merge_aa_features.py -o /media/the_beast/A/mathisi_tests/data/transformed/testset/tags/

echo Preparing amino acid features to the same dimensions...

mv /media/the_beast/A/mathisi_tests/data/transformed/testset/tags/*features* /media/the_beast/A/mathisi_tests/data/transformed/testset/temp/

python3 ./dataset_preparation/run_features_same_size.py -s /media/the_beast/A/mathisi_tests/data/transformed/testset/temp/ -d /media/the_beast/A/mathisi_tests/data/transformed/testset/$t/ -z $z

echo Script complete. Now run the control scipts