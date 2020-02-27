import re
import http.client
#import config
import json
import subprocess
from termcolor import colored

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
    except Exception as e:
        print('[Error]', e)
        exit(1)
    stdout, stderr = out.communicate()
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
