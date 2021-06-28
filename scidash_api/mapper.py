import os
import binascii
import logging
import copy

import dpath.util

from scidash_api.exceptions import ScidashClientException
from scidash_api.validator import ScidashClientDataValidator


logger = logging.getLogger(__name__)


class ScidashClientMapper(object):
    """ScidashClientMapper
        util class for converting raw data from Sciunit to data acceptable in
        Scidash
    """

    # Expected output format
    OUTPUT_SCHEME = {
            'score_class': {
                'class_name': None,
                'url': None
                },
            'model_instance': {
                'model_class': {
                    'class_name': None,
                    'import_path': None,
                    'url': '',
                    'capabilities': []
                    },
                'backend': None,
                'hash_id': None,
                'attributes': {},
                'name': None,
                'run_params': {},
                'url': None
                },
            'prediction': None,
            'raw': None,
            'related_data': None,
            'score': None,
            'hash_id': None,
            'sort_key': None,
            'score_type': None,
            'summary': None,
            'test_instance': {
                'description': None,
                'test_suites': [],
                'hash_id': None,
                'test_class': {
                    'class_name': None,
                    'import_path': None,
                    'url': None
                    },
                'observation': {
                    'mean': None,
                    'std': None,
                    'url': None
                    },
                'verbose': None
                }
            }

    KEYS_MAPPING = [
            (
                'score_class/class_name',
                '_class#name'
                ),
            (
                'score_class/url',
                '_class#url'
                ),
            (
                'model_instance/model_class/class_name',
                'model#py/state#_class#name'
                ),
            (
                'model_instance/model_class/url',
                'model#py/state#_class#url'
                ),
            (
                'model_instance/model_class/import_path',
                'model#py/state#_class#import_path'
                ),
            (
                'model_instance/name',
                'model#py/state#name'
                ),

            (
                'model_instance/url',
                'model#py/state#url'
                ),
            (
                'prediction',
                'prediction'
                ),
            (
                'raw',
                'raw'
                ),
            (
                'score',
                'score'
                ),
            (
                'score_type',
                'score_type'
                ),
            (
                'summary',
                'summary'
                ),
            (
                'test_instance/description',
                'test#py/state#description'
                ),
            (
                'test_instance/test_class/class_name',
                'test#py/state#name'
                ),
            (
                'test_instance/test_class/url',
                'test#py/state#_class#url'
                ),
            (
                'test_instance/test_class/import_path',
                'test#py/state#_class#import_path'
                ),
            (
                'test_instance/observation',
                'test#py/state#observation'
                ),
            (
                'test_instance/verbose',
                'test#py/state#verbose'
                ),
            ]

    OPTIONAL_KEYS_MAPPING = [
            (
                'model_instance/backend',
                'model/py/state#backend'
                ),
            (
                'model_instance/attrs',
                'model/py/state#attrs'
                ),
            (
                'related_data',
                'related_data',
                )
            ]

    def __init__(self):
        self.errors = []
        self.validator = ScidashClientDataValidator()

    def convert(self, raw_score_data=None, strict=False):
        """convert
        main method for converting

        :param raw_data:dict with data from sciunit

        :returns dict
        """

        if raw_score_data is None:
            return raw_score_data

        raw_data = raw_score_data['py/state']
        _id = raw_score_data['_id']

        if not self.validator.validate_score(raw_data) and strict:
            raise ScidashClientException('CLIENT -> INVALID DATA: '
                    '{}'.format(self.validator.get_errors()))
        elif not self.validator.validate_score(raw_data):
            logger.error('CLIENT -> INVALID DATA: '
                    '{}'.format(self.validator.get_errors()))
            self.errors.append(self.validator.get_errors())
            return None

        result = copy.deepcopy(self.OUTPUT_SCHEME)

        for item, address in self.KEYS_MAPPING:
            dpath.util.set(result, item, dpath.util.get(raw_data, address,'#'))

        for item, address in self.KEYS_MAPPING:
            if item == "test_instance/observation":
                dpath.util.set(result, item, dpath.util.get(raw_data, address,'#'))

        for item, address in self.OPTIONAL_KEYS_MAPPING:
            try:
                dpath.util.set(result, item, dpath.util.get(raw_data, address,'#'))
            except KeyError:
                logger.debug("Optional value {} is not found".format(item))

        for capability in dpath.util.get(raw_data, 'model#py/state#capabilities','#'):
            result.get('model_instance').get('model_class') \
                                        .get('capabilities').append({
                                            'class_name': capability.get('py/type')
                                        })

        try:
            for test_suite in dpath.util.get(raw_data, 'test#py/state#test_suites','#'):
                result.get('test_instance').get('test_suites').append({
                                                'name': test_suite.get('name'),
                                                'hash': _id
                                            })
        except KeyError:
            pass

        model_instance_hash_id = '{}_{}'.format(
                raw_data.get('model').get('hash', '?'), #binascii.b2a_hex(os.urandom(15))),
                _id)

        test_instance_hash_id = '{}_{}'.format(
                raw_data.get('test').get('hash', '?'), #, binascii.b2a_hex(os.urandom(15))),
                _id)

        score_instance_hash_id = '{}_{}'.format(
                raw_score_data.get('hash', '?'), #, binascii.b2a_hex(os.urandom(15))),
                _id)

        sort_key = raw_data.get('norm_score') if not raw_data.get('sort_key',
                                                              False) else \
        raw_data.get('sort_key')

        run_params = raw_data.get('model').get('run_params', False)

        if run_params:
            for key in run_params:
                run_params.update({
                    key: str(run_params.get(key))
                })

        result.get('model_instance').update({'hash_id':
            model_instance_hash_id})

        result.get('test_instance').update({'hash_id':
            test_instance_hash_id})

        result.update({'hash_id':
            score_instance_hash_id})

        result.update({
            'sort_key': sort_key
        })

        if run_params:
            result.get('model_instance').update({
                'run_params': run_params
            })

        if type(result.get('score')) is bool:
            result['score'] = float(result.get('score'))

        return result
