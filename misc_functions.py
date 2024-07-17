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
