from smb.SMBConnection import SMBConnection
import os
import json
from time import localtime
password = os.environ['NETID_PASSWORD']
conn = SMBConnection('caw247', password, 'cfacpr-01', 'cfacfile', domain='byu')

conn.connect('cfacfile.byu.edu')
def read_directories(path, depth):
    total_count = 0
    folders = {}
    for f in conn.listPath('Shared', path):
        if f.isDirectory and f.filename not in ['.', '..']:
            print(localtime(f.last_write_time).tm_year, f.file_size)
            total_count += 1
            child_total_count, child_folders = read_directories(path + '/' + f.filename, depth + 1)
            total_count += child_total_count
            folders[f.filename] = child_folders
    return {
        'num_folders': total_count, 
        'folders': folders
        'num_files'

count, data = read_directories('/College/Public Relations/', 0)
print('Total number of directories:\n{0}'.format(count))
with open('directory.json', 'w') as f:
    f.write(json.dumps(data))