SciDash Python API to upload data to SciDash from any Python environment

How to use it

.. code:: python

    from scidash_api import client

    # instantiate your client
    client_instance = client.ScidashClient()

    # or with optional build_info and hostname attributes
    client_instance = client.ScidashClient(build_info="SUPER BUILD", hostname="EXTRAORDINARY HOST")

    # or with custom config to point to a specific scidash deployment such as 'http://localhost:8000'
    client_instance = client.ScidashClient({'base_url': 'http://api.server.com'}, build_info="EXCEPTIONAL BUILD") // and with build_info for example

    # then you should login into Scidash Server
    client_instance.login({'username': 'username', 'password': 'password'})

    # and then call upload method
    client_instance.upload(data=data)
