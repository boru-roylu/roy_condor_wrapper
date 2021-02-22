#! /g/ssli/sw/roylu/bin/python3

import os
import time
import json

from utils import *
from config import *
import portalocker

#hostname = os.environ['HOSTNAME'].split('.')[0]

os.makedirs(gpu_info_dir, exist_ok=True)

while True:
    for hostname in ['emeril', 'julia', 'james', 'fred']:
        try:
            gpu_info_path = os.path.join(gpu_info_dir, hostname) 
            stdout = run_cmd(['ssh', hostname, '/g/ssli/sw/roylu/bin/gpustat', '--json'])
            gpus = json.loads(stdout)
            with portalocker.Lock(gpu_info_path, 'w', timeout=5) as f:
                json.dump(gpus, f)
        except Exception as e:
            print('[Error]', e)
    time.sleep(5)
