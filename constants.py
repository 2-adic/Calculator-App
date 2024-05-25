def get_constants(dictionary: dict) -> list:
    return sorted(dictionary.keys())


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
        ans[key] = dictionary[key][:digits]

    return ans


constants = {
    'i': 'i',
    'e': '2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274',
    'π': '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679',
    'φ': '1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374',
    'γ': '0.5772156649015328606065120900824024310421593359399235988057672348848677267776646709369470632917467495'
}
