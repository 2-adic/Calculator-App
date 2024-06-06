def generate_function_dictionary(dictionary_name: str) -> None:
    """
    Used to replace the function dictionary when more functions are added.
    """

    string = f'{dictionary_name} = {{\n    '

    for i, function in enumerate(accepted_functions):
        string += f"'{i}': self.{function.lower()}, "

    string = string[:-2]
    string += '\n}'

    print(string)


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

accepted_constants = sorted(constants.keys())

accepted_variables = sorted([
    'a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'θ'
])

accepted_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

copy_symbols = ['π', 'φ', 'γ', 'θ']

accepted_functions = [
    'Integrate',
    'Ln',
    'Sin',
    'Cos',
]

subscript = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
    'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ', 'v': 'ᵥ', 'x': 'ₓ', '+': '₊', '-': '₋', '=': '₌',
    '(': '₍', ')': '₎'
}

# generate_function_dictionary('self.funct')
