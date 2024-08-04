from PyQt6.QtWidgets import QLineEdit
from random import randint


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


def test_colors(settings) -> None:
    """
    Changes the colors of the windows to test if all colors are changing.
    """

    '''
    settings.color_background = 54, 92, 46
    settings.color_text = 177, 58, 58
    settings.color_text_highlight_active = 168, 171, 45
    settings.color_text_highlight_inactive = 163, 71, 45
    settings.color_text_secondary = 130, 135, 162
    settings.color_title_bar = 81, 40, 48
    settings.color_title_bar_text = 175, 178, 61
    settings.color_title_bar_button_hover = 40, 53, 141
    settings.color_title_bar_button_press = 182, 46, 119
    settings.color_title_bar_button_exit_hover = 181, 96, 133
    settings.color_title_bar_button_exit_press = 47, 137, 88
    settings.color_box_background = 58, 88, 104
    settings.color_box_hover = 148, 66, 155
    settings.color_box_selected = 139, 164, 32
    settings.color_box_border = 150, 196, 188
    settings.color_line_primary = 82, 54, 66
    settings.color_line_secondary = 20, 140, 51
    settings.color_scrollbar_background = 134, 51, 75
    '''

    '''
    settings.color_background = 49, 89, 153
    settings.color_text = 181, 96, 133
    settings.color_text_highlight_active = 168, 171, 45
    settings.color_text_highlight_inactive = 163, 71, 45
    settings.color_text_secondary = 130, 135, 162
    settings.color_title_bar = 23, 37, 51
    settings.color_title_bar_text = settings.color_text
    settings.color_title_bar_button_hover = 40, 53, 141
    settings.color_title_bar_button_press = 182, 46, 119
    settings.color_title_bar_button_exit_hover = 181, 96, 133
    settings.color_title_bar_button_exit_press = 47, 137, 88
    settings.color_box_background = 55, 68, 74
    settings.color_box_hover = 148, 66, 155
    settings.color_box_selected = 139, 164, 32
    settings.color_box_border = 54, 37, 47
    settings.color_line_primary = 82, 54, 66
    settings.color_line_secondary = 20, 140, 51
    settings.color_scrollbar_background = 134, 51, 75

    settings.color_latex = settings.color_text
    '''

    settings.color_background = 49, 89, 153
    settings.color_text = 255, 255, 255
    settings.color_text_highlight_active = 168, 171, 45
    settings.color_text_highlight_inactive = 163, 71, 45
    settings.color_text_secondary = 48, 55, 56
    settings.color_title_bar = 23, 37, 51
    settings.color_title_bar_text = settings.color_text
    settings.color_title_bar_button_hover = 18, 28, 38
    settings.color_title_bar_button_press = 181, 96, 133
    settings.color_title_bar_button_exit_hover = 158, 24, 75
    settings.color_title_bar_button_exit_press = 181, 96, 133
    settings.color_box_background = 99, 106, 115
    settings.color_box_hover = 98, 151, 156
    settings.color_box_selected = 47, 111, 130
    settings.color_box_border = settings.color_title_bar
    settings.color_line_primary = 15, 38, 71
    settings.color_line_secondary = 19, 49, 92
    settings.color_scrollbar_background = 59, 63, 69

    settings.color_latex = settings.color_text


def generate_new_colors() -> None:
    """
    Prints out new random rgb values to paste into the test_colors function.
    """

    color_min = 20
    color_max = 200

    string = (
        '''
        settings.color_background
        settings.color_text
        settings.color_text_highlight_active
        settings.color_text_highlight_inactive
        settings.color_text_secondary
        settings.color_title_bar
        settings.color_title_bar_text
        settings.color_title_bar_button_hover
        settings.color_title_bar_button_press
        settings.color_title_bar_button_exit_hover
        settings.color_title_bar_button_exit_press
        settings.color_box_background
        settings.color_box_hover
        settings.color_box_selected
        settings.color_box_border
        settings.color_line_primary
        settings.color_line_secondary
        settings.color_scrollbar_background
        '''
    )

    string = string.replace(' ', '')

    lines = string.split('\n')
    lines.pop(0)
    lines.pop(-1)

    result = ''
    for line in lines:
        line += f' = {randint(color_min, color_max)}, {randint(color_min, color_max)}, {randint(color_min, color_max)}'
        result += line + '\n'

    print(result)


# generate_new_colors()
