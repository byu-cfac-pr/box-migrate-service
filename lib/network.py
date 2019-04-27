from boxsdk import BoxAPIException
import hashlib

def upload_file(client, folder_id, file_name, file_size, buffer):
    chunk = 1024 * 1024 * 8 # 8 MB, might need to be changed
    upload_session = ''
    try_again = True
    while try_again:    
        try:
            if file_size < 1024 * 1024 * 20:
                client.folder(folder_id).upload('buffer', file_name)
            else:
                upload_session = client.folder(folder_id).create_upload_session(file_size, file_name)
                buffer.seek(0) # start reading at 0 bytes of file pointer
                sha_hash = hashlib.sha1()
                for offset in range(0, file_size, chunk):
                    part_content = buffer.read(chunk)
                    sha_hash.update(part_content)
                    upload_session.upload_part_bytes(part_content, offset, file_size)
                upload_session.commit(sha_hash.digest())
            try_again = False
        except BoxAPIException as err:
            if type(upload_session) is not str:
                upload_session.abort()
            print(err.message)
            if err.status == 400: # it didn't like the chunk size
                print('trying different chunk size for chunked upload')
                chunk *= 2
            if err.status == 401:
                print('refreshing access token')
                client.auth.refresh(client.auth.access_token)
            if err.status == 409:
                print("{0} already exists, skipping".format(file_name))
                try_again = False
        
