import os
import re
import json
import requests
from random import randint
from requests.utils import quote
from scidash_api import client


class ScidashRestApiClient(object):

    def __init__(self, base_url, username, password):
        self.api_test_class_url = f'{base_url}/api/test-classes/'
        self.api_test_instance_url = f'{base_url}/api/test-instances/'
        self.api_model_class_url = f'{base_url}/api/model-classes/'
        self.api_model_instance_url = f'{base_url}/api/model-instances/'
        self.api_compatibility_url = f'{base_url}/api/compatibility/'
        self.api_schedule_url = f'{base_url}/api/schedule/'
        client_instance = client.ScidashClient(
            config={'base_url': base_url},
            hostname=os.uname().nodename)
        client_instance.login(
            username=username,
            password=password)
        self.headers = client_instance.get_headers()

    @classmethod
    def _generateId(cls, max, min):
        return randint(min, min + max)

    @classmethod
    def _generateHash(cls, string):
        hash = 0
        if len(string) == 0:
            return hash
        for chr in string:
            hash = (hash << 5) - hash + ord(chr)
            hash |= 0  # Convert to 32bit integer
        return abs(hash)

    @classmethod
    def _generateHashId(cls, string):
        saltedName = f'{string}_{cls._generateId(2000, 100000)}'
        hash = cls._generateHash(saltedName)
        id = cls._generateId(1000000, 9999999)
        return f'{hash}_{id}'

    def _get_test_class(self, import_path):
        r = requests.get(
                self.api_test_class_url,
                headers=self.headers)
        test_classes = json.loads(r.content)
        found = list(filter(lambda tc: (tc['import_path'] == import_path), test_classes))[0]
        found["class_name"] = re.sub(r' (\(.*\))', '', found["class_name"])
        return found

    def create_test(self, test_instance, test_class_import_path):
        test_instance['hash_id'] = self._generateHashId(test_instance['name'])
        test_instance['test_class'] = self._get_test_class(test_class_import_path)
        r = requests.post(
                self.api_test_instance_url,
                headers=self.headers,
                json=test_instance)
        if r.status_code == 201:
            return json.loads(r.content)
        raise Exception(r.text)

    def get_model_classes(self, model_url):
        url = quote(model_url)
        r = requests.get(
                f'{self.api_model_class_url}?model_url={url}',
                headers=self.headers)
        return json.loads(r.content)

    def create_model(self, model_instance, model_class):
        model_instance['hash_id'] = self._generateHashId(model_instance['name'])
        model_instance['model_class'] = model_class
        model_instance['status'] = 'a'
        r = requests.post(
                self.api_model_instance_url,
                headers=self.headers,
                json=model_instance)
        if r.status_code == 201:
            return json.loads(r.content)
        raise Exception(r.text)

    def _check_compatibility(self, tests, models):
        r = requests.post(
                self.api_compatibility_url,
                headers=self.headers,
                json={
                    'tests': tests,
                    'models': models
                })
        if r.status_code == 200:
            return json.loads(r.content)
        raise Exception(r.text)

    def schedule(self, test_instances, model_instances, suite_name=''):
        tests = list(map(lambda t: t['id'], test_instances))
        models = list(map(lambda m: m['id'], model_instances))
        # first check if everything is compatible
        self._check_compatibility( tests, models)
        # schedule it
        matrix = {}
        for model in models:
            matrix[model] = tests
        r = requests.post(
                self.api_schedule_url,
                headers=self.headers,
                json={
                    'suiteName': suite_name,
                    'matrix': matrix
                })
        if r.status_code == 200:
            return json.loads(r.content)
        raise Exception(r.text)
