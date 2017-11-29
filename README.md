# scidash-api
SciDash Python API to interact with the SciDash backend from any Python environment

How to use it

```python
from scidash_api import client

client_instance = client.ScidashClient()

# or with custom config

client_instance = client.ScidashClient({
            'base_url': 'http://api.server.com'
        })

# config format
CONFIG = {
    'base_url': 'http://localhost:8000',
    'upload_url': '/data/upload/{filename}', # {filename} is required, it will be replaced with file name at the time of the request
    'auth_url': '/api/login/',
    'file_name': 'data.json'
}

# then you should login into Scidash Server

client_instance.login({'username': 'username', 'password': 'password'})

# and finally upload

client_instance.upload_json('<json_string>')

# or just an object

client_instance.upload_object({'hello': 'scidash'})

```
