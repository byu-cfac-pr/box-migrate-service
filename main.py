from lib.auth import get_auth_box_client, get_smb_conn
from lib.network import upload_file
from lib.helper import RunningTotal
from boxsdk import BoxAPIException
import hashlib
import os

client = get_auth_box_client()
conn = get_smb_conn()
SHARED_DRIVE_PATH = '/College/Public Relations/'
rt = RunningTotal("Files uploaded:")

buffer = open('buffer', 'rb+')

result = input("Currently copying Shared Drive files from {0}. Is this ok? (n)\n>".format(SHARED_DRIVE_PATH))
if result == 'n':
    SHARED_DRIVE_PATH = input("Provide the path to copy files from\n>")
BOX_FOLDER_ID = input("What Box folder to upload to (folder id)\n>")

def upload_folder_contents(path, folder_id):
    folder = client.folder(folder_id)
    for f in conn.listPath('Shared', path):
        if not f.isDirectory and f.filename not in ['.', '..']:
            rt.next()
            buffer.seek(0)
            conn.retrieveFile('Shared', path + f.filename, buffer)
            buffer.truncate()
            upload_file(client, folder_id, f.filename, f.file_size, buffer)
        elif f.isDirectory and f.filename not in ['.', '..']:
            try:
                subfolder = folder.create_subfolder(f.filename)
            except BoxAPIException:
                for _f in folder.get_items():
                    if _f.get().name == f.filename:
                        subfolder = _f
                        break
            upload_folder_contents(path + f.filename + '/', subfolder.object_id)

upload_folder_contents(SHARED_DRIVE_PATH, BOX_FOLDER_ID)
