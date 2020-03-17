#! /usr/bin/bash

#gpu_info_py=/g/ssli/sw/roylu/roy_condor_wrapper/gpuinfo.py


hostnames=(james julia fred)
hostname=`echo $HOSTNAME | cut -d'.' -f1`

trap "rm -f $gpu_lock_path" EXIT

while true
do
    for hostname in ${hostname[@]}
    output_dir=/g/ssli/sw/roylu/roy_condor_wrapper/.gpu_info
    output_path=$output_dir/$hostname
    gpu_lock_path=$output_dir/${hostname}.lock
    if [ -f gpu_lock_path ]
    then
        sleep 1
        continue
    else
        touch $gpu_lock_path
    fi
    #/g/ssli/sw/roylu/bin/python3 $gpu_info_py
    #timeout 1s /g/ssli/sw/roylu/bin/gpustat --json > $output_path || echo '{}' > $output_path
    /g/ssli/sw/roylu/bin/gpustat --json > $output_path
    [ -f $gpu_lock_path ] && rm -f $gpu_lock_path
    sleep 2
done
