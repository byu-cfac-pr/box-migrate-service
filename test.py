from lib.auth import get_auth_client
import hashlib
import os

client = get_auth_client()
test_folder_id = "63992343393"

f = open('data.txt', 'rb')
file_name = f.name
file_size = os.path.getsize(file_name)

upload_session = client.folder(test_folder_id).create_upload_session(file_size, file_name)
chunk = 8388608
sha_hash = hashlib.sha1()
for offset in range(0, file_size, chunk):
    print(offset)
    part_content = f.read(chunk)
    sha_hash.update(part_content)
    upload_session.upload_part_bytes(part_content, offset, file_size)
upload_session.commit(sha_hash.digest())