import copy
import dpath.util


class ScidashClientMapper(object):
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

    def convert(self, raw_data=None):

        if raw_data is None:
            return self.OUTPUT_SCHEME

        result = copy.deepcopy(self.OUTPUT_SCHEME)

        for item, address in self.KEYS_MAPPING:
            dpath.util.set(result, item, dpath.util.get(raw_data, address))

        return result
