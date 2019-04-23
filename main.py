from lib.auth import get_auth_box_client, get_smb_conn
import hashlib
import os

client = get_auth_box_client()
conn = get_smb_conn()
SHARED_DRIVE_PATH = '/College/Public Relations/'
TEST_FOLDER_ID = "63992343393"

buffer = open('buffer', 'rb+')

###
# Get file from Shared Drive, save to buffer file
###
buffer.seek(0)
conn.retrieveFile('Shared', SHARED_DRIVE_PATH + 'Dance Video Interviews/DSC_0004.MOV', buffer)
buffer.truncate()
###
# Send file to Box, reading in chunks
###

file_name = 'DSC_0004.MOV'
file_size = os.path.getsize('buffer')

upload_session = client.folder(TEST_FOLDER_ID).create_upload_session(file_size, file_name)
chunk = 1024 * 1024 * 32 # send 32 MB chunks
sha_hash = hashlib.sha1()
buffer.seek(0)

for offset in range(0, file_size, chunk):
    print(offset)
    part_content = buffer.read(chunk)
    sha_hash.update(part_content)
    upload_session.upload_part_bytes(part_content, offset, file_size)
upload_session.commit(sha_hash.digest())
