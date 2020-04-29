import os

import jsonschema
import pytest
import yaml

from deplane.cli import cli_impl

HERE = os.path.dirname(__file__)
SCHEMA = os.path.join(HERE, 'deplane-schema.yaml')

with open(SCHEMA) as f:
    validator = jsonschema.Draft7Validator(yaml.safe_load(f))

def _schema(fname):
    return os.path.join(HERE, '..', 'schemas', fname)

def _validate(fname):
    __tracebackhide__ = True
    with open(_schema(fname)) as i:
        instance = yaml.safe_load(i)

    errors = '\n\n'.join(str(v) for v in validator.iter_errors(instance))
    if errors:
        pytest.fail(errors)
    return instance

def test_service():
    _validate('service-v1.yaml')

def test_service_dep_en():
    cli_impl('en', _schema('service-v1.yaml'), '/dev/null')

def test_service_dep_fr():
    cli_impl('fr', _schema('service-v1.yaml'), '/dev/null')
