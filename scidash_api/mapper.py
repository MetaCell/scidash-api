import copy

import cerberus
import dpath.util

from scidash_api.exceptions import ScidashClientException
from scidash_api.validator import ScidashClientDataValidator


class ScidashClientMapper(object):
    """ScidashClientMapper
        util class for converting raw data from Sciunit to data acceptable in
        Scidash
    """

    # Expected output format
    OUTPUT_SCHEME = {
            'model_instance': {
                'model_class': {
                    'class_name': None,
                    'url': '',
                    'capabilities': []
                    },
                'attributes': {},
                'name': None,
                'run_params': {},
                'url': None
                },
            'prediction': None,
            'raw': None,
            'related_data': {},
            'score': None,
            'sort_key': None,
            'score_type': None,
            'summary': None,
            'test_instance': {
                'description': None,
                'test_suites': [],
                'test_class': {
                    'class_name': None,
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
                'model_instance/model_class/class_name',
                'model/_class/name'
                ),
            (
                'model_instance/model_class/url',
                'model/_class/url'
                ),
            (
                'model_instance/attributes',
                'model/attrs'
                ),
            (
                'model_instance/name',
                'model/name'
                ),
            (
                'model_instance/run_params',
                'model/run_params'
                ),
            (
                'model_instance/url',
                'model/url'
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
                'related_data',
                'related_data'
                ),
            (
                'score',
                'score'
                ),
            (
                'sort_key',
                'sort_key'
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
                'test/description'
                ),
            (
                'test_instance/test_class/class_name',
                'test/name'
                ),
            (
                'test_instance/test_class/url',
                'test/_class/url'
                ),
            (
                'test_instance/observation',
                'test/observation'
                ),
            (
                'test_instance/verbose',
                'test/verbose'
                ),
            ]

    def __init__(self):
        self.validator = ScidashClientDataValidator()


    def convert(self, raw_data=None):
        """convert
        main method for converting

        :param raw_data:dict with data from sciunit

        :returns dict
        """

        if raw_data is None:
            return self.OUTPUT_SCHEME

        if not self.validator.validate_score(raw_data):
            raise ScidashClientException('WRONG DATA:'
                    '{}'.format(self.validator.get_errors()))

        result = copy.deepcopy(self.OUTPUT_SCHEME)

        for item, address in self.KEYS_MAPPING:
            dpath.util.set(result, item, dpath.util.get(raw_data, address))

        for capability in dpath.util.get(raw_data, 'model/capabilities'):
            result.get('model_instance').get('model_class') \
                                        .get('capabilities').append({
                                            'class_name': capability
                                        })

        try:
            for test_suite in dpath.util.get(raw_data, 'test/test_suites'):
                result.get('test_instance').get('test_suites').append({
                                                'name': test_suite.get('name'),
                                                'hash': test_suite.get('hash')
                                            })
        except KeyError:
            pass

        return result
