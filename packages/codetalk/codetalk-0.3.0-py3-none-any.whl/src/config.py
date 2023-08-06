import json
import os

CONF_DIR = os.path.join(os.getenv('HOME'), '.config', 'codetalk')
CONF_FILE = os.path.join(CONF_DIR, 'settings.json')

if not os.path.exists(CONF_DIR):
    os.makedirs(CONF_DIR, exist_ok=True)

def get_config(conf_key):
    try:
        with open(CONF_FILE) as fp:
            conf = json.load(fp)
    except:
        conf = {}

    return conf.get(conf_key)

def set_config(conf_key, value):
    try:
        with open(CONF_FILE) as fp:
            conf = json.load(fp)
    except:
        conf = {} # TODO

    conf[conf_key] = value
    with open(CONF_FILE, 'w') as fp:
        json.dump(conf, fp)
