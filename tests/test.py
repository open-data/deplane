import os

import jsonschema
import pytest
import yaml

HERE = os.path.dirname(__file__)
SCHEMA = os.path.join(HERE, 'deplane-schema.yaml')

with open(SCHEMA) as f:
    validator = jsonschema.Draft7Validator(yaml.safe_load(f))

def _validate(fname):
    __tracebackhide__ = True
    instance_name = os.path.join(HERE, '..', 'schemas', fname)
    with open(instance_name) as i:
        instance = yaml.safe_load(i)

    errors = '\n\n'.join(str(v) for v in validator.iter_errors(instance))
    if errors:
        pytest.fail(errors)
    return instance

def test_service():
    _validate('service-v1.yaml')
