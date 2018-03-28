scidash-api
===========

SciDash Python API to upload data to SciDash from any Python environment

How to use it

.. code:: python

    from scidash_api import client

    # instantiate your client with defaults
    client_instance = client.ScidashClient()

    # or with optional build_info and hostname attributes
    client_instance = client.ScidashClient(build_info="SUPER BUILD", hostname="EXTRAORDINARY HOST")

    # or with custom config to point to a specific scidash deployment such as 'http://localhost:8000' and hostname
    client_instance = client.ScidashClient({'base_url': 'http://localhost:8000'}, hostname="EXTRAORDINARY HOST")

    # login into Scidash Server
    client_instance.login({'username': 'my_username', 'password': 'my_secret_password'})

    # and then call upload method for score object from sciunit
    client_instance.upload_score(score)

    # or call upload_suite method passing suite and score_matrix sciunit objects
    client_instance.upload_suite(suite, score_matrix)