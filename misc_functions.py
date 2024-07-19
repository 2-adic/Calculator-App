from PyQt6.QtWidgets import QLineEdit


def get_position_change(key_list_prev: list, key_list_curr: list, string: str) -> int:

    i_curr = 0
    i_prev = 0

    for i, key in enumerate(key_list_prev):
        if key == string:
            i_prev = i
            break

    for i, key in enumerate(key_list_curr):
        if key == string:
            i_curr = i
            break

    return i_curr - i_prev


def get_line_edit_key(dictionary: dict, line_edit: QLineEdit) -> str:

    for i, key in enumerate(sorted(dictionary.keys())):
        if dictionary[key][1] == line_edit:
            return key


def is_all_int(array: tuple[str, ...]) -> bool:
    """
    Checks if all the elements in a list are ints or not.

    Assumes all elements are in the form: _ or _.__
    """

    for element in array:
        if '/' in element:  # number is a fraction (not an int since fractions are simplified)
            return False

        if '.' in element:  # if a non 0 appears after a decimal point, it is not an int

            element = element[element.find('.') + 1:]

            for char in element:
                if char != '0':
                    return False

    return True


def get_constant_values(dictionary: dict, digits: int) -> dict:
    """
    Sets the amount of digits for the constants.

    :param dictionary: The dictionary of the constants.
    :param digits: The amount of digits for the constants (counting from after the decimal place).
    :return: Returns the dictionary, but the constants have the amount of digits specified.
    """

    max_digits = 100
    if digits > max_digits:
        print(f'Constants will use their maximum saved value of {max_digits}, since the specified value is over that amount: {digits}')
        digits = max_digits

    elif digits < 1:
        print(f'Constants will be 1 digit long, since the specified value is under that amount: {digits}')
        digits = 1

    digits += 2  # since digits are counted from after the decimal place, 2 is added to address this

    # adds each constant value to the new dictionary with the specified amount of digits
    ans = {}
    for key in sorted(dictionary.keys()):
        ans[key] = dictionary[key][1][:digits]

    return ans
