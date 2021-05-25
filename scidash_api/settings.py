'''
SciDash API settings file.

Here you can find all common settings for the library
'''
import json
from pathlib import Path
import urllib.request

CONFIG = {
    'base_url': 'http://54.177.242.165',
    'upload_url': '/data/upload/{filename}',
    'auth_url': '/api/login/',
    'file_name': 'data.json'
}

def get_config(attr, kind='prod'):
    path = Path(__file__).parent.parent / 'config.json'
    with open(path, 'r') as f:
        config = json.load(f)
    val = config[kind][attr]
    return val
