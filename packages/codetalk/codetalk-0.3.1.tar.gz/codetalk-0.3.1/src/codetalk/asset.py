import os

def get_asset(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    asset_path = os.path.join(dir_path, 'assets', file_name)
    with open(asset_path) as fp:
        return fp.read()

def print_logo():
    logo = get_asset('logo.txt')
    print(logo)

def get_version():
    version = get_asset('version.txt')
    print(f"codetalk version: {version}")
