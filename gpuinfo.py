#! /g/ssli/sw/roylu/bin/python3

import os
import json

from utils import *
from config import *

gpus = get_gpu_info()
if not gpus:
    gpus = {}
hostname = os.environ['HOSTNAME'].split('.')[0]

os.makedirs(gpu_info_dir, exist_ok=True)
gpu_info_path = os.path.join(gpu_info_dir, hostname) 
gpu_lock_path = os.path.join(gpu_info_dir, f'{hostname}.lock')

try:
    while os.path.exists(gpu_lock_path):
        pass
    gpu_info_lock(hostname)
    with open(gpu_info_path, 'w') as f:
        json.dump(gpus, f)
except Exception as e:
    print('[Error]', e)
finally:
    gpu_info_unlock(hostname)
