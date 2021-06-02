import math
import numbers
import importlib
import json
import jsonpickle
import sciunit
import sciunit.scores

from cerberus import Validator
from copy import deepcopy

from scidash_api.exceptions import ScidashClientValidatorException


def build_destructured_unit(unit_dict):
    unit = pq.UnitQuantity(
        unit_dict.get('name'),
        import_class(unit_dict.get('base').get('quantity')) *
        unit_dict.get('base').get('coefficient'), unit_dict.get('symbol')
    )

    return unit


def import_class(import_path: str) -> object:
    """ Import class from import_path

    :type str:
    :param import_path: path to module similar to path.to.module.ClassName

    :returns: imported class
    """

    splitted = import_path.split('.')

    class_name = splitted[-1:][0]
    module_path = ".".join(splitted[:-1])

    imported_module = importlib.import_module(module_path)
    klass = getattr(imported_module, class_name)

    return klass


class ValidatorExtended(Validator):

    def _validate_isnan(self, isnan, field, value):
        """
        Check, is value NaN or not

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """

        if not isinstance(value, numbers.Number):
            return

        if not isnan and math.isnan(value):
            self._error(field, "Value can't be NaN")


class ScidashClientDataValidator():

    errors = None

    # Validation schema for raw score
    SCORE_SCHEMA = {
            '_class': {
                'type': 'dict',
                'schema': {
                    'url': {
                        'type': 'string',
                        'required': True
                        },
                    'name': {
                        'type': 'string',
                        'required': True
                        }
                    }
                },
            'model': {
                'py/state': {
                    'type': 'dict',
                    'schema': {
                        '_class': {
                            'type': 'dict',
                            'schema': {
                                'name': {
                                    'type': 'string'
                                    },
                                'url': {
                                    'type': 'string',
                                    'required': True
                                    }
                                }
                            },
                        'attrs': {
                            'type': 'dict',
                            'required': False
                            },
                        'hash': {
                                'type': 'string',
                                'required': False
                                },
                        '_id': {
                                'type': 'number',
                                'required': True
                                },
                        'capabilities': {
                            'type': 'list',
                            'required': True,
                            'schema': {
                                'type': 'string'
                                }
                            },
                        'name': {
                            'type': 'string',
                            'required': True
                            },
                        'run_params': {
                            'type': 'dict',
                            'required': False
                            },
                        'url': {
                            'type': 'string',
                            'required': True
                            }
                        }
                    },
                 },
            'observation': {
                'type': 'dict',
                'required': True
                },
            'prediction': {
                'type': ['number', 'dict'],
                'required': True,
                'isnan': False
                },
            'raw': {
                'type': 'string',
                'required': True
                },
            'score': {
                'type':['number', 'boolean'],
                'isnan': False,
                'required': True
                },
            'score_type': {
                    'type': 'string'
                    },
            'sort_key': {
                    'type': 'number',
                    'isnan': False,
                    'required': False
            },
            'norm_score': {
                    'type': 'number',
                    'isnan': False,
                    'required': False
            },
            'summary': {
                    'type': 'string',
                    'required': True
                    },
            'hash': {
                    'type': 'string',
                    'required': False
                    },
            '_id': {
                    'type': 'number',
                    'required': True
                    },
            'test': {
                    'type': 'dict',
                    'schema': {
                        '_class': {
                            'type': 'dict',
                            'schema': {
                                'name': {
                                    'type': 'string',
                                    'required': True
                                    },
                                'url': {
                                    'type': 'string',
                                    'required': True
                                    }
                                },
                            'required': True
                            },
                        'description': {
                            'type': 'string',
                            'nullable': True,
                            'required': True
                            },
                        'hash': {
                                'type': 'string',
                                'required': False
                                },
                        '_id': {
                                'type': 'number',
                                'required': True
                                },
                        'name': {
                            'type': 'string',
                            'required': True
                            },
                        'observation': {
                            'type': 'dict',
                            'required': True
                            },
                        }
                    }
            }

    def validate_score(self, data):
        """
        Checks, is score raw data valid and can be processed

        :raw_data: raw data dictionary
        :returns: boolean

        """
        try:
            # old style
            sciunit.settings['PREVALIDATE'] = True
        except:
            # new style
            try:
                sciunit.config_set('PREVALIDATE', True)
            except:
                sciunit.config.set('PREVALIDATE', True)

        class_data = data.get('test_class')
        if not class_data:
            class_data = data.get('test').get("py/state").get('_class')

        if not class_data.get('import_path', False):
            return data

        test_class = import_class(class_data.get('import_path'))

        observation = deepcopy(data.get('observation'))  # json of observation
        # Thicken the JSON with metadata required for deserialization
        for key, value in observation.items():
            if isinstance(value, dict) and 'units' in value:
                observation[key] = {'py/object': 'quantities.quantity.Quantity',
                                    'py/state': value}
        observation = json.dumps(observation)  # As string for decoding
        observation = jsonpickle.decode(observation)  # decode
        test_class(observation)
        return True


    def get_errors(self):
        """
        Returns errors from last validation procedure, if any
        """
        return self.errors

    def validate_suite(self, raw_data):
        raise NotImplementedError("Not implemented yet")
