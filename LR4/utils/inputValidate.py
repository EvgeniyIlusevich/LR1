def input_data(description, data_type, min_value=None, max_value=None):
    """Prompts the user for input, validates type and value constraints, and returns the valid input"""
    while True:
        try:
            user_input = data_type(input(description))

            if min_value is not None and user_input <= min_value:
                raise ValueError(f"The value have to be greater then {min_value}")

            if max_value is not None and user_input >= max_value:
                raise ValueError(f"The value have to be less then {max_value}")

            return user_input

        except ValueError as e:
            print(f"Error: {e}. Please enter a valid value.")

def input_with_validator(description, validator):
    while True:
        try:
            user_input = input(description)
            if validator(user_input):
                return user_input
            else:
                raise ValueError

        except ValueError as e:
            print(f"Error: {e}. Please enter a valid value.")