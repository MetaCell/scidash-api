from __future__ import unicode_literals, print_function
import json

import requests
import six
import cerberus

from scidash_api import settings


class ScidashClientException(Exception):
    pass


class ScidashClient(object):

    """Base client class for all actions with Scidash API"""

    SCHEMA = {
            'test_instance': {
                'type': 'dict'
                }
            }

    def __init__(self, config=None, build_info=None, hostname=None):
        self.token = None

        self.config = settings.CONFIG

        self.data = {}

        self.build_info = build_info
        self.hostname = hostname

        self.validator = cerberus.Validator(self.SCHEMA)
        self.validator.allow_unknown = True

        if config is not None:
            self.config.update(config)

    def get_headers(self):
        return {
                'Authorization': 'JWT {}'.format(self.token)
                }

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
        base_url = self.config.get('base_url')

        r = requests.post('{}{}'.format(base_url, auth_url), data=credentials)

        self.token = r.json().get('token')

        return self

    def set_data(self, data=None):

        if isinstance(data, six.string_types):
            data = json.loads(data)

        if self.validator.validate(self.data):
            self.data = data
            self.data.get('test_instance').update({
                "build_info": self.build_info,
                "hostname": self.hostname
                })
        else:
            raise ScidashClientException('WRONG DATA:'
                    '{}'.format(self.validator.errors))

        return self

    def upload(self):
        """
        Private main method for uploading

        :prepared_data: Prepared serialized data for uploading
        :returns: urllib3 requests object

        """

        files = {
                'file': (self.config.get('file_name'), json.dumps(self.data))
                }

        headers = self.get_headers()

        upload_url = \
            self.config.get('upload_url') \
            .format(filename=self.config.get('file_name'))
        base_url = self.config.get('base_url')

        r = requests.put('{}{}'.format(base_url, upload_url), headers=headers,
                files=files)

        return r
