# scidash-api
SciDash Python API to interact with the SciDash backend from any Python environment

How to use it

```python
from scidash_api import client

# instantiate your client
client_instance = client.ScidashClient()

# or with custom config to point to a specific scidash deployment such as 'http://localhost:8000'
client_instance = client.ScidashClient({'base_url': 'http://api.server.com'})

# then you should login into Scidash Server
client_instance.login({'username': 'username', 'password': 'password'})

# and finally upload your data 
client_instance.upload_json('<json_string>')

# or just an object
client_instance.upload_object({'hello': 'scidash'})

```
