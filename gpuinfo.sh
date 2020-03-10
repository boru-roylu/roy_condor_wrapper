#! /usr/bin/bash

python=/g/ssli/roylu/bin/python3 
gpu_info_py=/g/ssli/roylu/roy_condor_wrapper/gpuinfo.py

while true
do
    $python $gpu_info_py
    sleep 1
done
