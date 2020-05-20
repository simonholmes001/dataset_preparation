#!/usr/bin/env bash

# Script to unpack the test_data.gz files

SOURCE='/media/kovan_ai_tor_the_beast/hard_drive_2/TEST_DATA/adjacency/dataset_gz'

cd $SOURCE
for dir in */
do
    cd ${dir}
    for file in ./*
    do
        echo $file
        gzip -d ${file}
    done
done