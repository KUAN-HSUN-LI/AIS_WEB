import json
from glob import glob
import os
from typing import List

def load_gpu_info_from_files(gpu_info_dir) -> List[dict]:
    paths = glob(os.path.join(gpu_info_dir, '*'))
    gpus = []
    for path in paths:
        with open(path, "r") as f:
            obj = json.load(f)
        gpus += parse_server_gpu(obj)
    return gpus

def parse_server_gpu(server_info: dict) -> dict:
    for gpu in server_info['gpus']:
        gpu['hostname'] = server_info['hostname']
        gpu['time'] = server_info['query_time']
        for process in gpu['processes']:
            process['username'] = mask_username(process['username'])

    return server_info['gpus']

def mask_username(username: str) -> str:
    if len(username) == 1:
        return username[0] + "***"
    return username[0] + "***" + username[-1]