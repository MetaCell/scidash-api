import unittest
import json

from scidash_api import client

# client_instance = client.ScidashClient()

# data = None

# request = client_instance.login('admin', 'kavabanga').upload_json(data)


class ScidashApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client_instance = client.ScidashClient(build_info="test_info",
                hostname="test_host")

        with open('json_sample.json') as f:
            cls.json = f.read()

        cls.test_user = {
                'username': 'admin_test',
                'password': 'admin_test'
                }

    def test_login(self):
        self.client_instance.login(**self.test_user)

        self.assertFalse(self.client_instance.token is None)

    def test_upload(self):
        self.client_instance.set_data(self.json)

        self.assertIsInstance(self.client_instance.data, dict)

        self.client_instance.set_data(json.loads(self.json))

        self.assertIsInstance(self.client_instance.data, dict)

        request = self.client_instance.upload()

        response_data = request.json()

        self.assertTrue(response_data.get('success'))
        self.assertTrue(response_data.get('data').get('test_instance')
                .get('build_info') == self.client_instance.build_info)

        self.assertTrue(response_data.get('data').get('test_instance')
                .get('hostname') == self.client_instance.hostname)
