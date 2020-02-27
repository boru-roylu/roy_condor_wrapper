import getpass
import http.client
from urllib.parse import urlencode
import os
import json
import slurm

monitor_host = 'master'
monitor_port = '80'

cpu_min = 1
cpu_max = 32
mem_min = 0.1
mem_max = 376
gpu_max = 8
#TODO: Need to customize the following
gpu_models = ['TITAN X (Pascal)', 'TAITAN Xp', '2080Ti']
gpu_node2gpu_max = {'julia': 2, 'james': 2, 'fred': 2, 'emeril': 8}
#partitions = ['3d','10d']
#age_factor_max_seconds = slurm.get_priority_max_age()
# too slow
# max_billing_per_account, spot_billing_ratio = slurm.get_qos_settings()
max_billing_per_account = 'UNLIMITED'
spot_billing_ratio = 0.2

username = getpass.getuser()
defaults_path = os.path.join(os.environ['HOME'], '.hconfig')
auth_cookie_path = os.path.join(os.environ['HOME'], '.hauthcookie')
cookie = None


def get_defaults():
    try:
        with open(defaults_path) as f:
            ret = json.load(f)
        return ret
    except:
        return {}


def set_defaults(key, value):
    defaults = get_defaults()
    defaults[key] = value
    with open(defaults_path, 'w') as f:
        json.dump(defaults, f)


def get_cookie():
    try:
        with open(auth_cookie_path) as f:
            cookie = f.read()
        return cookie
    except:
        return None


def check_auth():
    global cookie
    cookie = get_cookie()
    if cookie is None:
        return False

    h1 = http.client.HTTPConnection(
        monitor_host, timeout=600,
        port=monitor_port,
    )
    h1.request("POST", "/check",
               headers={
                   "Content-type": "application/json",
                   "Accept": "text/plain",
                   "Cookie": cookie,
               }
               )
    resp = h1.getresponse()

    return resp.status == 200


#def login():
#    global cookie
#    print('=== Login ===')
#    print(f'Username: {username}')
#    passwd = getpass.getpass()
#
#    h1 = http.client.HTTPConnection(
#        monitor_host, timeout=600,
#        port=monitor_port,
#    )
#    h1.request("POST", "/login",
#               body=urlencode({'username': username, 'password': passwd}).encode(),
#               headers={
#                   "Content-type": "application/x-www-form-urlencoded",
#                   "Accept": "text/plain",
#               }
#               )
#    resp = h1.getresponse()
#
#    if resp.status != 200:
#        return False
#
#    cookie = None
#    for k, v in resp.getheaders():
#        if k == 'Set-Cookie':
#            cookie = v
#
#    if cookie is not None:
#        with open(auth_cookie_path, 'w') as f:
#            f.write(cookie)
#
#    return True
#
#
#def check_login():
#    if check_auth():
#        return True
#
#    # not logged in 
#    login()
#
#    return check_auth()
#
#
#if not check_login():
#    exit('Error: login failed.')
#
