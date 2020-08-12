import os
from os.path import isfile, join


def get_subfolders(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]


def get_files(path):
    ret_list = []
    for f in os.listdir(path):
        fullpath = os.path.join(path, f)
        if isfile(fullpath):
            ret_list.append(fullpath)
    return ret_list
