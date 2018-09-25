def find_choice_by_name(choices, value):
    if value or value == 0:
        if isinstance(value, str):
            for choice in choices:
                if choice[1].lower() == value.lower():
                    return choice[0]
            else:
                raise Exception('Choice not found by value.')
        elif isinstance(value, int):
            # Value is already an integer, so just give it back
            return value
