#! /usr/bin/bash

#gpu_info_py=/g/ssli/sw/roylu/roy_condor_wrapper/gpuinfo.py


output_dir=/g/ssli/sw/roylu/roy_condor_wrapper/.gpu_info
hostname=`echo $HOSTNAME | cut -d'.' -f1`
output_path=$output_dir/$hostname
gpu_lock_path=$output_dir/${hostname}.lock

trap "rm -rf $gpu_lock_path" EXIT

while true
do
    if [ -f gpu_lock_path ]
    then
        sleep 1
        continue
    else
        touch $gpu_lock_path
    fi
    #/g/ssli/sw/roylu/bin/python3 $gpu_info_py
    timeout 1s /g/ssli/sw/roylu/bin/gpustat --json > $output_path || echo '{}' > $output_path
    rm $gpu_lock_path
    sleep 1
done
