from __future__ import unicode_literals, print_function
import json

import requests
import settings


class ScidashClient(object):

    """Base client class for all actions with Scidash API"""

    def __init__(self, config=None):
        self.token = None

        # Check, should we use default settings
        if config is None:
            self.config = settings.CONFIG
        else:
            self.config = config

    def login(self, username, password):
        """
        Getting API token from Scidash

        :param username:
        :param password:
        """
        credentials = {
                "username": username,
                "password": password
                }

        auth_url = self.config.get('auth_url')
        base_url = self.config.get('scidash_server_url')

        r = requests.post('{}{}'.format(base_url, auth_url), data=credentials)

        return r

    def upload_json(self, data):
        """
        Upload method for JSON string

        :param data: JSON string
        """
        self._upload(data)

    def upload_object(self, _object):
        """
        Upload method for serializable object

        :param _object: dict or list
        """
        serialized_object = json.dumps(_object)

        self._upload(serialized_object)

    def _upload(self, prepared_data):
        """
        Private main method for uploading

        :prepared_data: Prepared serialized data for uploading
        :returns: urllib3 requests object

        """
        print(prepared_data)
