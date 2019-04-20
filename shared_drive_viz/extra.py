from smb.SMBConnection import SMBConnection
import os
import json
from time import localtime
import time
password = os.environ['NETID_PASSWORD']
conn = SMBConnection('caw247', password, 'cfacpr-01', 'cfacfile', domain='byu')
PATH = '/College/Public Relations/'
SECONDS_2017 = time.mktime(time.strptime("01 Jan 17", "%d %b %y"))

conn.connect('cfacfile.byu.edu')

base_folders = []
for f in conn.listPath('Shared', PATH):
    if f.isDirectory and f.filename not in ['.', '..']:
        base_folders.append(f)

def folder_content_size(path):
    data = {
        'size': 0,
        'num_files': 0,
        'num_before_2017': 0
    }
    for _f in conn.listPath('Shared', path):
        if not _f.isDirectory and _f.filename not in ['.', '..']:
            data['num_files'] += 1
            data['size'] += _f.file_size
            if _f.last_write_time < SECONDS_2017:
                data['num_before_2017'] += 1
        elif _f.isDirectory and _f.filename not in ['.', '..']:
            _data = folder_content_size(path + '/' + _f.filename)
            data['size'] += _data['size']
            data['num_files'] += _data['num_files']
            data['num_before_2017'] += _data['num_before_2017']
    return data

with open('folder_stats.csv', 'w') as f:
    f.write('Folder,Content Size,Num Files,Num Before 2017\n')
    for folder in base_folders:
        data = folder_content_size(PATH + '/' + folder.filename)
        f.write('{0},{1},{2},{3}\n'.format(folder.filename, data['size'], data['num_files'], data['num_before_2017'])) 