#! /g/ssli/sw/roylu/bin/python3

import os
import re
import csv
import http.client
from io import StringIO
#import config
import json
import subprocess
from termcolor import colored
from pathlib import Path

from config import *

def colored_by_ratio(text, ratio, thres=[0.5, 0.999999]):
    if ratio < thres[0]:
        clr = 'green'
    elif ratio < thres[1]:
        clr = 'yellow'
    # elif ratio < thres[2]:
        # clr = 'orange'
    else:
        clr = 'red'
    return colored(text, clr)


def thres_red(text, val, thres=1):
    if val < thres:
        return colored(text, 'red')
    else:
        return colored(text, 'white')


def uniq(arr):
    # ref: https://mail.python.org/pipermail/python-dev/2017-December/151283.html
    return list(dict.fromkeys(arr))


def run_cmd(args):
    try:
        out = subprocess.Popen(args,
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        stdout, stderr = out.communicate(timeout=3)
    except Exception as e:
        if type(e) == subprocess.TimeoutExpired:
            return None
        print('[Error]', e)
        exit(1)
    return stdout.decode("utf-8")


def clean_duplicate_nodes(nodes):
    new_nodes = []
    existing_node = set()
    for node in nodes:
        name = node['Machine']
        if name not in existing_node: 
            existing_node.add(name)
            new_nodes.append(node)
    return new_nodes


def get_node_names():
    stdout = run_cmd(['condor_status', '-long', '-json'])
    nodes = json.loads(stdout)
    nodes = clean_duplicate_nodes(nodes)
    nodes = [node['Machine'].split('.')[0] for node in nodes]
    return nodes


def get_gpu_info():
    stdout = run_cmd(['nvidia-smi', '--query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu', '--format=csv'])
    hostname = os.environ['HOSTNAME']
    try:
        rows = list(csv.DictReader(StringIO(stdout), delimiter=',', skipinitialspace=True))
        new_rows = []
        for r in rows:
            d = {}
            d['gpu_model'] = r['name'].strip()#.split(' ')[:2])
            d['gpu_mem_total'] = int(r['memory.total [MiB]'].split(' ')[0])
            d['gpu_mem_util'] = int(r['memory.used [MiB]'].split(' ')[0])
            d['gpu_util'] = int(r['utilization.gpu [%]'].split(' ')[0])
            d['gpu_temp'] = int(r['temperature.gpu'])
            new_rows.append(d)
        return new_rows
    except Exception as e:
        print('[Error]', e)
        return {}


def gpu_info_lock(hostname):
    gpu_lock_path = os.path.join(gpu_info_dir, f'{hostname}.lock')
    Path(gpu_lock_path).touch()


def gpu_info_unlock(hostname):
    gpu_lock_path = os.path.join(gpu_info_dir, f'{hostname}.lock')
    if os.path.exists(gpu_lock_path):
        os.remove(gpu_lock_path)
