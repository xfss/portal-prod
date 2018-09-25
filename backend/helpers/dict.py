from copy import deepcopy


def set_path_to_value(original_dict, path, value):
    current_dict = deepcopy(original_dict)
    if isinstance(path, str):
        current_path = path.split('.')
    else:
        current_path = path

    if len(current_path) < 2:
        current_dict[current_path[0]] = value
    else:
        current_dict[current_path[0]] = set_path_to_value(current_dict.get(current_path[0], {}), current_path[1:], value)

    return current_dict
