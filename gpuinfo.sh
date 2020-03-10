#! /usr/bin/bash

gpu_info_py=/g/ssli/sw/roylu/roy_condor_wrapper/gpuinfo.py

while true
do
    /g/ssli/sw/roylu/bin/python3 $gpu_info_py
    sleep 1
done
