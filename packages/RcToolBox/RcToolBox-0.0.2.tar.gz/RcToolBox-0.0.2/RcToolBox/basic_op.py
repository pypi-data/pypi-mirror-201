# some functions copy from nnUnet
import pickle
import os
import yaml
import json
import time
import glob

"""load and save file"""
def load_yaml(file):
    """

    :param file: yaml
    :return:
    """
    return yaml.load(open(file), Loader=yaml.FullLoader)


def load_json(file):
    with open(file, 'r') as f:
        tmp = json.load(f)
    return tmp


def save_json(obj, file, indent=4, sort_keys=False):
    with open(file, 'w') as f:
        json.dump(obj, f, sort_keys=sort_keys, indent=indent)


def load_pkl(path):
    pickle_file = open(path, 'rb')
    obj = pickle.load(pickle_file)
    pickle_file.close()
    return obj


def save_pkl(path, obj):
    pickle_file = open(path, 'wb')
    pickle.dump(obj, pickle_file)
    pickle_file.close()


def load_txt(file):
    filestream = []
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            filestream.append(line)
    return filestream


"""print with highlight"""
def sprint(content, placeholder=40):
    if isinstance(content, str):
        placeholder -= len(content)
        left_placeholder = int(placeholder / 2)
        right_placeholder = int(placeholder - left_placeholder)
        print('\n' + '-' * left_placeholder + content + '-' * right_placeholder)
    else:
        print('content should be str')

"""Timer"""
def programStart():
    return time.time()

def programEnd(start, program_name='it'):
    end = time.time()
    time_slot = end - start
    if time_slot > 3600:
        print('{} cost: {} hour {} min {}s'.format(program_name,time_slot // 3600, time_slot % 3600 // 60, time_slot % 60))
    elif time_slot > 60:
        print('{} cost: {} min {} s'.format(program_name, int(time_slot // 60), int(time_slot % 60)))
    else:
        print('{} cost: {:.1f} s'.format(program_name, time_slot))

"""Date"""

def get_date():
    
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))
        
# shortcut
join = os.path.join

dir_path = os.path.dirname
abs_path = os.path.abspath
exists = os.path.exists

isdir = os.path.isdir
isfile = os.path.isfile

if __name__ == '__main__':
    
    # _start = programStart()
    # programEnd(_start, 'Loop')
    print(get_date())