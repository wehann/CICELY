import json
import start
import os


json_file = '..' + os.path.sep + 'configs' + os.path.sep + 'config_RQ2.json'
work_folder = '..' + os.path.sep + 'runtime'
with open(json_file, 'r') as load_f:
    print('Reading json configs...')
    configs = json.load(load_f)
    print('Read complete.\n')
print('Start analyzing...')
start.start(configs, work_folder)
