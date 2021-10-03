"""
This function is provided by Hao Fang.
"""
import os
from re import sub

def normalize_tial_path(path):
    path = path.rstrip()

    path = sub(r'^/atm/(nest|chicken|turkey)/vol/(tial|ssli)/sw', r'/g/tial/sw', path)

    # Note: must do in the correct order, otherwise need to use if-else.
    path = sub(r'^/atm/(nest|chicken|turkey)/vol/data', r'/g/tial/data', path)
    path = sub(r'^/atm/(nest|chicken|turkey)/vol/projects', r'/g/tial/projects', path)
    path = sub(r'^/atm/(nest|chicken|turkey|ente|goose|quail)/vol/home', r'/homes', path)
    path = sub(r'^/atm/(nest|chicken|goose|turkey|nest|pheasant|rooster|duck)/vol/transitory', r'/g/tial/transitory', path)
    path = sub(r'^/atm/(duck)/(nest|chicken)/transitory', r'/g/tial/transitory', path)
    path = sub(r'^/atm/ente/(tial|ssli)', r'/g/tial', path)
    path = sub(r'^/atm', r'/n', path)
    path = sub(r'^/afs/ee.washington.edu/nikola', r'/usr/nikola', path)

    # BABEL
    # TODO: also /g/(tial|ssli)/data
    path = sub(r'^/g/(tial|ssli)/projects/babel-', r'/g/tial/projects/babel/', path)

    # DEFT
    # TODO: also /g/(tial|ssli)/data
    path = sub(r'^/g/(tial|ssli)/projects/deft/', r'/g/tial/projects/DEFT/', path)
    path = sub(r'^/g/(tial|ssli)/projects/deft-cep/', r'/g/tial/projects/DEFT-CEP/', path)

    # BOLT
    # TODO: also /g/(tial|ssli)/data
    path = sub(r'^/g/(tial|ssli)/projects/bolt-bc-', r'/g/tial/projects/bolt-bc/', path)

    return path


def tial_abspath(path):
    return normalize_tial_path(os.path.abspath(path))
