import unittest
import json

from scidash_api import client

# client_instance = client.ScidashClient()

# data = None

# request = client_instance.login('admin', 'kavabanga').upload_json(data)


class ScidashApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client_instance = client.ScidashClient()

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
        request = self.client_instance.upload_json(self.json)

        self.assertTrue(request.json().get('success'))

        request = self.client_instance.upload_object(json.loads(self.json))

        self.assertTrue(request.json().get('success'))
