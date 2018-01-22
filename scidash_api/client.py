from __future__ import unicode_literals, print_function
import json

import requests
import six
import cerberus
import platform

from scidash_api import settings
from scidash_api.exceptions import ScidashClientException
from scidash_api.mapper import ScidashClientMapper


class ScidashClient(object):

    """Base client class for all actions with Scidash API"""

    SCHEMA = {
            'test_instance': {
                'type': 'dict'
                }
            }

    def __init__(self, config=None, build_info=None, hostname=None):
        """__init__

        :param config:
        :param build_info:
        :param hostname:
        """
        self.token = None

        self.config = settings.CONFIG

        self.data = {}

        self.build_info = build_info if build_info is not None else platform.platform()
        self.hostname = hostname

        self.validator = cerberus.Validator(self.SCHEMA)
        self.validator.allow_unknown = True

        self.mapper = ScidashClientMapper()

        if config is not None:
            self.config.update(config)

    def get_headers(self):
        """
        Shortcut for gettings headers for uploading
        """
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
        """
        Sets data for uploading

        :param data:
        :returns: self
        """

        if isinstance(data, six.string_types):
            data = json.loads(data)

        if self.validator.validate(self.data):
            self.data = self.mapper.convert(data)
            self.data.get('test_instance').update({
                "build_info": self.build_info,
                "hostname": self.hostname
                })
        else:
            raise ScidashClientException('WRONG DATA:'
                    '{}'.format(self.validator.errors))

        return self

    def upload(self, data=None):
        """
        Private main method for uploading

        :returns: urllib3 requests object
        """

        if data is not None:
            self.set_data(data)

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
