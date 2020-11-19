#! /g/ssli/sw/roylu/bin/python3

import os
import re
import csv
import sys
import glob
import json
import subprocess
from termcolor import colored
from pathlib import Path
import portalocker
import yaml
from itertools import product

import config

from normalize_tial_path import normalize_tial_path

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


def read_gpu_info(hostname):
    gpu_info_path = os.path.join(config.gpu_info_dir, hostname)
    with portalocker.Lock(gpu_info_path, 'r', timeout=5) as f:
        gpus = json.load(f)
    return gpus['gpus']


def create_run_script(tmpdir, cmd):
    script_path = os.path.join(tmpdir, 'run.sh')  
    with open(script_path, 'w') as f:
        print('#! /bin/sh', file=f)
        print(' '.join(real_cmd), file=f)
    return script_path


def create_submit_file(condor_params, tmpdir):
    submit_file_path = os.path.join(tmpdir, 'submit_file')
    with open(submit_file_path, 'w') as f:
        for k, v in condor_params.items():
            print(f'{k:20}= {v}', file=f)
        print('Queue', file=f)
    return submit_file_path


def get_executable_cmd(cmd):
    proc = subprocess.Popen(['which', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if stdout:
        return stdout.decode("utf-8").strip(), True
    else:
        cmd = normalize_tial_path(os.path.realpath(cmd))
        if os.path.exists(cmd):
            return cmd, True
        else:
            return cmd, False


def remove_files_in_dir(dir_path):
    for path in glob.glob(os.path.join(dir_path, '*')):
        os.remove(path)


def get_itemdata_and_arguments(path, arguments):
    try:
        with open(path, 'r') as f:
            itemdata = json.load(f)
    except:
        sys.exit(f'[Error] The file ({path}) is not a json file.')
    for k in itemdata[0].keys():
        k_in_arg = f'@{k}@'
        if k_in_arg not in arguments:
            sys.exit(f'[Error] Please make sure the key \"{k}\" in itemdata '
                     f'should be in you command and like this format '
                     f'{k_in_arg}')
        else:
            k_index = arguments.index(k_in_arg)
            arguments[k_index] = f'$({k})'
    return itemdata, arguments


def create_scripts_for_batch_jobs(path):
    try:
        with open(path, 'r') as f:
            y = yaml.load(f, Loader=yaml.FullLoader)
    except:
        sys.exit(f'[Error] The file ({path}) is not a yaml file.')

    assert 'commands' in y
    assert 'params' in y

    for i, ps in enumerate(y['params']):
        v = ps['values']
        assert isinstance(v, str) or isinstance(v, list)
        assert 'values' in ps and 'name' in ps
        if isinstance(v, str):
            try:
                y['params'][i]['values'] = eval(v)
            except Exception as e:
                sys.exit(f'[Error] {e}.')

    keys = [ps['name'] for ps in y['params']]
    params = [ps['values'] for ps in y['params']]
    jobs = list(product(*params))

    assert len(keys) == len(jobs[0])

    seen = set()
    for k in keys:
        if k not in seen:
            seen.add(k)
        else:
            sys.exit(f'[Error] Duplicated parameter\'s name {k} in the yaml file.')

    scripts = []
    for job in jobs:
        cmd = '\n'.join(y['commands'])
        for k, v in zip(keys, job):
            cmd = cmd.replace(f'$({k})', str(v))
        scripts.append(cmd)
    return scripts
