import math
import numbers

from scidash_api.exceptions import ScidashClientException
from cerberus import Validator


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
            'model': {
                'type': 'dict',
                'schema': {
                    '_class': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string'
                                },
                            'url': {
                                'type': 'string'
                                }
                            }
                        },
                    'attrs': {
                        'type': 'dict',
                        'required': False
                        },
                    'capabilities': {
                        'type': 'list',
                        'schema': {
                            'type': 'string'
                            }
                        },
                    'name': {
                        'type': 'string'
                        },
                    'run_params': {
                        'type': 'dict',
                        'required': False
                        },
                    'url': {
                        'type': 'string'
                        }
                    }
                },
            'observation': {
                'type': 'dict'
                },
            'prediction': {
                'type': ['number', 'dict'],
                'isnan': False
                },
            'raw': {
                'type': 'string'
                },
            'related_data': {
                'type': 'dict'
                },
            'score': {
                'type': 'number',
                'isnan': False
                },
            'score_type': {
                    'type': 'string'
                    },
            'sort_key': {
                    'type': 'number',
                    'isnan': False
                    },
            'summary': {
                    'type': 'string'
                    },
            'test': {
                    'type': 'dict',
                    'schema': {
                        '_class': {
                            'type': 'dict',
                            'schema': {
                                'name': {
                                    'type': 'string'
                                    },
                                'url': {
                                    'type': 'string'
                                    }
                                }
                            },
                        'description': {
                            'type': 'string',
                            'nullable': True
                            },
                        'name': {
                            'type': 'string'
                            },
                        'observation': {
                            'type': 'dict'
                            },
                        'verbose': {
                            'type': 'number',
                            'isnan': False
                            }
                        }
                    }
            }

    def validate_score(self, raw_data):
        """
        Checks, is score raw data valid and can be processed

        :raw_data: raw data dictionary
        :returns: boolean

        """

        validator = ValidatorExtended(self.SCORE_SCHEMA)
        validator.allow_unknown = True

        valid = validator.validate(raw_data)

        if not valid:
            self.errors = validator.errors

        return valid

    def get_errors(self):
        """
        Returns errors from last validation procedure, if any
        """
        return self.errors

    def validate_suite(self, raw_data):
        raise NotImplementedError("Not implemented yet")
