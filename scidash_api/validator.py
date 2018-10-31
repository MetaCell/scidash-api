import math
import numbers

from cerberus import Validator

from scidash_api.exceptions import ScidashClientValidatorException


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
                            'required': True
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
                    'required': True
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
                                'required': True
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
                        'verbose': {
                            'type': 'number',
                            'isnan': False,
                            'required': True
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

        if not raw_data.get('sort_key', False):
            if not raw_data.get('norm_score', False):
                raise ScidashClientValidatorException("sort_key or norm_score"
                                                      "not found")

        return valid

    def get_errors(self):
        """
        Returns errors from last validation procedure, if any
        """
        return self.errors

    def validate_suite(self, raw_data):
        raise NotImplementedError("Not implemented yet")
