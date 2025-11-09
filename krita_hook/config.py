import os
import json


CONFIG_PATH = 'krita.json'


try:
    with open(CONFIG_PATH, 'r') as json_file:
        config = json.load(json_file)
except:
    config = None
