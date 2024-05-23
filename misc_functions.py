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
