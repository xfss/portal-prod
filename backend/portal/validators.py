from glom import glom

from helpers.dict import set_path_to_value
from portal.models import PublicationConfigRule


def publication_config_validator(value, exception_to_raise):
    config_rules = PublicationConfigRule.objects.all()

    result = {}
    for rule in config_rules:
        if rule.path:
            config_value = glom(value, rule.path, default=None)
            if config_value:
                if rule.type and type(config_value).__name__ != rule.type:
                    raise exception_to_raise(f'Configuration value type mismatch. [name] {rule.name} [path]: {rule.path} [type] {type(config_value).__name__} [expected_type] {rule.type}')
                result = set_path_to_value(result, rule.path, config_value)
            elif rule.mandatory:
                raise exception_to_raise(f'Mandatory configuration value not found. [name] {rule.name} [path] {rule.path}')
        else:
            raise exception_to_raise(f'No path for configuration rule. This should never happen. [name] {rule.name}')
    return result
