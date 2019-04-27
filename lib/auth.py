from boxsdk import Client, DevelopmentClient
from boxsdk.auth import RedisManagedOAuth2
from smb.SMBConnection import SMBConnection
from socket import gethostname
import json

def get_auth_box_client():
    with open('private.json', 'r') as f:
        auth = json.loads(f.read())['box']

    option = input('Type "1" to pass a developer token, or anything else to authenticate with OAUTH 2\n>')
    if option == "1":
        token = input("Developer token:\n>")
        oauth = RedisManagedOAuth2(
            client_id=auth['client-id'],
            client_secret=auth['client-secret'],
            access_token=token,
            unique_id='foo'
        )
        return DevelopmentClient(oauth=oauth)
    else:
        oauth = RedisManagedOAuth2(
            client_id=auth['client-id'],
            client_secret=auth['client-secret'],
            unique_id='foo'
        )
        auth_url, csrf = oauth.get_authorization_url('http://localhost')
        print("URL:\n" + auth_url)
        code = input('Provide the Authorization Code\n>')
        return Client(oauth)

def get_smb_conn():
    with open('private.json') as f:
        auth = json.loads(f.read())['smb']
    conn = SMBConnection(
        auth['netid_username'],
        auth['netid_password'],
        gethostname()[:15], # computer name can only be 15 characters
        auth['remote_name'],
        domain=auth['domain'])
    conn.connect('cfacfile.byu.edu')
    return conn