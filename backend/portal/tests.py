import pytest
from rest_framework.serializers import ValidationError

from portal.models import PublicationConfigRule
from portal.serializers import PublicationSerializer


@pytest.mark.django_db
def test_config_validator():
    PublicationConfigRule(name='name1', path='a.b.c', type=PublicationConfigRule.STRING, mandatory=False).save()
    PublicationConfigRule(name='name2', path='a.d', type=PublicationConfigRule.INT, mandatory=True).save()
    PublicationConfigRule(name='name3', path='x.y', type=PublicationConfigRule.LIST, mandatory=False).save()

    # Positive tests
    config = {'a': {'d': 5}}
    result = PublicationSerializer.validate_configuration(config)
    assert result == {'a': {'d': 5}}

    config = {'a': {'b': {}, 'd': 5}}
    result = PublicationSerializer.validate_configuration(config)
    assert result == {'a': {'d': 5}}

    config = {'a': {'b': {'c': 'test string'}, 'd': 5}}
    result = PublicationSerializer.validate_configuration(config)
    assert result == {'a': {'b': {'c': 'test string'}, 'd': 5}}

    config = {'a': {'b': {'c': 'test string'}, 'd': 5}, 'x': {'y': [1, 2, 'z']}}
    result = PublicationSerializer.validate_configuration(config)
    assert result == {'a': {'b': {'c': 'test string'}, 'd': 5}, 'x': {'y': [1, 2, 'z']}}

    # Negative tests
    config = {'a': {'b': {'c': 'test string'}}}
    try:
        PublicationSerializer.validate_configuration(config)
    except ValidationError as e:
        assert e.detail == ['Mandatory configuration value not found. [name] name2 [path] a.d']

    config = {'a': {'d': {'c': 'test string'}}}
    try:
        PublicationSerializer.validate_configuration(config)
    except ValidationError as e:
        assert e.detail == ['Configuration value type mismatch. [name] name2 [path]: a.d [type] dict [expected_type] int']

    config = {'a': {'d': 5}, 'unknown_key': 'unknown_val'}
    result = PublicationSerializer.validate_configuration(config)
    assert result == {'a': {'d': 5}}
