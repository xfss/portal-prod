from helpers.dict import set_path_to_value


def test_config_validator():
    original_dict = {
        'a': {
            'b': {
                'c': "example string 1"
            }
        }
    }

    # This is needed to make sure there is no side effects for our function
    untouched_original_dict = {
        'a': {
            'b': {
                'c': "example string 1"
            }
        }
    }

    path = ['a', 'b', 'c']
    untouched_path = ['a', 'b', 'c']

    result1 = set_path_to_value(original_dict, 'a.b.c', 'changed string')
    result2 = set_path_to_value(original_dict, path, 'changed string')

    target_dict = {
        'a': {
            'b': {
                'c': "changed string"
            }
        }
    }

    # Test for side effects
    assert original_dict == untouched_original_dict
    assert path == untouched_path

    # Test expected results
    assert result1 == target_dict
    assert result2 == target_dict

    path = ['a', 'd']
    untouched_path = ['a', 'd']

    result1 = set_path_to_value(original_dict, 'a.d', 1)
    result2 = set_path_to_value(original_dict, path, 1)

    target_dict = {
        'a': {
            'b': {
                'c': "example string 1"
            },
            'd': 1
        }
    }

    # Test for side effects
    assert original_dict == untouched_original_dict
    assert path == untouched_path

    # Test expected results
    assert result1 == target_dict
    assert result2 == target_dict
