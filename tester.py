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

        with open('test_data/raw_json_sample_prediction_numeric.json') as f:
            cls.json_numeric = f.read()

        with open('test_data/raw_json_sample_prediction_dict.json') as f:
            cls.json_dict = f.read()

        with open('test_data/raw_json_sample_malformed.json') as f:
            cls.raw_json_dict_malformed = f.read()

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

    def test_upload_numeric(self):
        self.client_instance.set_data(self.json_numeric)
        self.assertIsInstance(self.client_instance.data, dict)
        self.client_instance.set_data(json.loads(self.json_numeric))
        self.assertIsInstance(self.client_instance.data, dict)
        request = self.client_instance.upload_test_score()
        response_data = request.json()
        self.assertTrue(response_data.get('success'))
        self.assertTrue(response_data.get('data').get('test_instance')
                .get('build_info') == self.client_instance.build_info)
        self.assertTrue(response_data.get('data').get('test_instance')
                .get('hostname') == self.client_instance.hostname)

    def test_upload_dict(self):
        self.client_instance.set_data(self.json_dict)
        self.assertIsInstance(self.client_instance.data, dict)
        self.client_instance.set_data(json.loads(self.json_dict))
        self.assertIsInstance(self.client_instance.data, dict)
        request = self.client_instance.upload_test_score()
        response_data = request.json()
        self.assertTrue(response_data.get('success'))
        self.assertTrue(response_data.get('data').get('test_instance')
                .get('build_info') == self.client_instance.build_info)
        self.assertTrue(response_data.get('data').get('test_instance')
                .get('hostname') == self.client_instance.hostname)

    def test_do_not_upload_malformed_data(self):
        r = self.client_instance.upload_score(self.raw_json_dict_malformed)
        self.assertFalse(r)


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

        with open('test_data/raw_json_sample_prediction_numeric.json') as f:
            cls.raw_json_numeric = f.read()

        with open('test_data/raw_json_sample_prediction_dict.json') as f:
            cls.raw_json_dict = f.read()

        with open('test_data/raw_json_sample_malformed.json') as f:
            cls.raw_json_dict_malformed = f.read()

        cls.raw_data_numeric = json.loads(cls.raw_json_numeric)
        cls.raw_data_dict = json.loads(cls.raw_json_dict)
        cls.raw_json_dict_malformed = json.loads(cls.raw_json_dict_malformed)

    def test_is_mapper_works_correctly_numeric(self):

        processed_data = self.mapper_instance.convert(self.raw_data_numeric)

        for item, address in self.mapper_instance.KEYS_MAPPING:
            self.assertEqual(
                    dpath.util.get(self.raw_data_numeric, address),
                    dpath.util.get(processed_data, item)
                    )

    def test_is_mapper_works_correctly_dict(self):

        processed_data = self.mapper_instance.convert(self.raw_data_dict)

        for item, address in self.mapper_instance.KEYS_MAPPING:
            self.assertEqual(
                    dpath.util.get(self.raw_data_dict, address),
                    dpath.util.get(processed_data, item)
                    )

    def test_exception_raising_well(self):
        with self.assertRaises(e.ScidashClientException) as c:
            self.mapper_instance.convert(self.raw_json_dict_malformed,
                    strict=True)

        broken_raw_data = nan_test_object.NAN_OBJECT

        with self.assertRaises(e.ScidashClientException) as c:
            self.mapper_instance.convert(broken_raw_data, strict=True)

    def test_exception_was_not_raised(self):
        result = self.mapper_instance.convert(self.raw_json_dict_malformed,
                strict=False)

        self.assertTrue(result is None)
