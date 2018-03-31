import unittest
import json
import copy

import dpath.util

from scidash_api.client import ScidashClient
from scidash_api import mapper
from scidash_api import exceptions as e
from scidash_api import validator

from test_data import nan_test_object


class ScidashApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client_instance = copy.deepcopy(ScidashClient(config={
            'base_url': 'http://localhost:8000'
        }, hostname='test_host'))

        with open('test_data/raw_json_sample.json') as f:
            cls.json = f.read()

        cls.test_user = {
                'username': 'admin_test',
                'password': 'admin_test_password'
                }

        cls.broken_user = {
            'username': 'lol',
            'password': 'rofl'
        }

    def test_login(self):
        with self.assertRaises(e.ScidashClientException) as c:
            self.client_instance.login(**self.broken_user)

        self.client_instance.login(**self.test_user)
        self.assertFalse(self.client_instance.token is None)

    def test_upload(self):
        self.client_instance.set_data(self.json)

        self.assertIsInstance(self.client_instance.data, dict)

        self.client_instance.set_data(json.loads(self.json))

        self.assertIsInstance(self.client_instance.data, dict)

        request = self.client_instance.upload_score()

        response_data = request.json()

        self.assertTrue(response_data.get('success'))
        self.assertTrue(response_data.get('data').get('test_instance')
                .get('build_info') == self.client_instance.build_info)

        self.assertTrue(response_data.get('data').get('test_instance')
                .get('hostname') == self.client_instance.hostname)

    def test_config_checking(self):
        with self.assertRaises(e.ScidashClientWrongConfigException) as c:
            broken_instance = ScidashClient(config={
                'base_url': 'http://broken_url/'
                })


class ScidashValidatorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.validator = validator.ScidashClientDataValidator()
        cls.nan_data = nan_test_object.NAN_OBJECT

    def test_nan_validation(self):
        self.assertFalse(self.validator.validate_score(self.nan_data))


class ScidashMapperTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.mapper_instance = mapper.ScidashClientMapper()

        with open('test_data/raw_json_sample.json') as f:
            cls.raw_json = f.read()

        cls.raw_data = json.loads(cls.raw_json)

    def test_is_mapper_works_correctly(self):

        processed_data = self.mapper_instance.convert(self.raw_data)

        for item, address in self.mapper_instance.KEYS_MAPPING:
            self.assertEqual(
                    dpath.util.get(self.raw_data, address),
                    dpath.util.get(processed_data, item)
                    )

    def test_exception_raising_well(self):
        broken_raw_data = copy.deepcopy(self.raw_data)

        broken_raw_data['test'] = []

        with self.assertRaises(e.ScidashClientException) as c:
            self.mapper_instance.convert(broken_raw_data)

        broken_raw_data = nan_test_object.NAN_OBJECT

        with self.assertRaises(e.ScidashClientException) as c:
            self.mapper_instance.convert(broken_raw_data)
