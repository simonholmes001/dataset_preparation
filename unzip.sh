#!/usr/bin/env bash

# Script to unpack the test_data.gz files


# Add in a path to the data - VERY NECESSARY TO AVOID MAKING A MESS OF YOUR FILE STRUCTURE!!!
cd $*
for dir in */
do
    cd ${dir}
    for file in ./*
    do
        echo $file
        gzip -d ${file}
    done
done