#! /g/ssli/sw/roylu/bin/python3

import os
import time
import json

from utils import *
from config import *
import portalocker

hostname = os.environ['HOSTNAME'].split('.')[0]

os.makedirs(gpu_info_dir, exist_ok=True)
gpu_info_path = os.path.join(gpu_info_dir, hostname) 

while True:
    try:
        stdout = run_cmd(['gpustat', '--json'])
        gpus = json.loads(stdout)
        with portalocker.Lock(gpu_info_path, 'w', timeout=5) as f:
            json.dump(gpus, f)
        time.sleep(50)
    except Exception as e:
        print('[Error]', e)
