from __future__ import unicode_literals, print_function
import json
import logging
from platform import platform, system

import requests
import six

from scidash_api import settings
from scidash_api.mapper import ScidashClientMapper
from scidash_api import exceptions
from scidash_api import helper

logger = logging.getLogger(__name__)


class ScidashClient(object):

    """Base client class for all actions with Scidash API"""

    def __init__(self, config=None, build_info=None, hostname=None):
        """__init__

        :param config:
        :param build_info:
        :param hostname:
        """
        self.token = None

        self.config = settings.CONFIG

        self.data = {}
        self.errors = []

        if build_info is None:
            self.build_info = "{}/{}".format(platform(), system())
        else:
            self.build_info = build_info

        self.hostname = hostname

        self.mapper = ScidashClientMapper()

        if config is not None:
            self.config.update(config)

        self.test_config()

    def test_config(self):
        """
        Check, is config is fine
        :returns: void
        :raises: ScidashClientWrongConfigException
        """
        if self.config.get('base_url')[-1] is '/':
            raise exceptions.ScidashClientWrongConfigException('Remove last '
                                                               'slash '
                                                               'from base_url')

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

        try:
            self.token = r.json().get('token')
        except Exception as e:
            raise exceptions.ScidashClientException('Authentication'
                                                    ' Failed: {}'.format(e))

        if self.token is None:
            raise exceptions.ScidashClientException('Authentication Failed: '
                    '{}'.format(r.json()))

        return self

    def set_data(self, data=None):
        """
        Sets data for uploading

        :param data:
        :returns: self
        """
        if isinstance(data, six.string_types):
            data = json.loads(data)
        elif not isinstance(data, dict):
            data = json.loads(data.json(add_props=True, string=True))

        self.data = self.mapper.convert(data)

        if self.data is not None:
            self.data.get('test_instance').update({
                "build_info": self.build_info,
                "hostname": self.hostname
                })
        else:
            self.errors = self.errors + self.mapper.errors

        return self

    def upload_test_score(self, data=None):
        """
        Main method for uploading

        :returns: urllib3 requests object
        """

        if data is not None:
            self.set_data(data)

        if self.data is None:
            return False

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

        if r.status_code == 400 or r.status_code == 500:
            self.errors.append(r.text)

            if r.status_code == 400:
                logger.error('SERVER -> INVALID DATA: '
                        '{}'.format(self.errors))

            if r.status_code == 500:
                logger.error('SERVER -> SERVER ERROR: '
                        '{}'.format(self.errors))

        return r

    def upload_score(self, data=None):
        helper.deprecated(method_name="upload_score()",
                will_be_removed="2.0.0", replacement="upload_test_score()")

        return self.upload_test_score(data)

    def upload_suite_score(self, suite, score_matrix):
        """upload_suite

        uploading score matrix with suite information

        :param suite:
        :param score_matrix:

        :returns: urllib3 requests object list
        """
        if isinstance(suite, six.string_types):
            suite = json.loads(suite)
        elif not isinstance(suite, dict):
            suite = json.loads(suite.json(add_props=True, string=True))

        if isinstance(score_matrix, six.string_types):
            score_matrix = json.loads(score_matrix)
        elif not isinstance(score_matrix, dict):
            score_matrix = json.loads(score_matrix.json(add_props=True,
                string=True))

        hash_list = []

        for test in suite.get('tests'):
            hash_list.append(test.get('hash'))

        responses = []
        raw_score_list = score_matrix.get('scores')

        flat_score_list = [score for score_list in raw_score_list for score in
                score_list]

        for score in flat_score_list:
            if score.get('test').get('hash') in hash_list:
                if 'test_suites' not in score.get('test'):
                    score.get('test').update({
                        'test_suites': []
                        })

                score.get('test').get('test_suites').append(suite)

            responses.append(self.upload_test_score(data=score))

        return responses

    def upload_suite(self, suite, score_matrix):
        helper.deprecated(method_name="upload_suite()",
                will_be_removed="2.0.0", replacement="upload_suite_score()")

        return self.upload_suite_score(suite, score_matrix)
