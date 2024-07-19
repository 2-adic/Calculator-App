from misc_functions import get_constant_values

constants = {
    'i': ('I', 'i'),
    'e': ('E',              '2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274'),
    'π': ('pi',             '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'),
    'φ': ('GoldenRatio',    '1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374'),
    'γ': ('EulerGamma',     '0.5772156649015328606065120900824024310421593359399235988057672348848677267776646709369470632917467495')
}

accepted_variables = sorted([
    'a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'θ'
])

accepted_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

accepted_misc = [
    '(', ')', ',', '.',
    '=', '<', '>',
    '+', '*', '-', '/', '^', '!', '%'
]

functions = [
    'diff',
    'integrate',
    'log',
    'ln',
    'exp',
    'abs',
    'mod',
    'floor',
    'ceil',
    'random',
    'sin',
    'cos',
    'tan',
    'csc',
    'sec',
    'cot',
    'arcsin',
    'arccos',
    'arctan',
    'arccsc',
    'arcsec',
    'arccot',
    'sinh',
    'cosh',
    'tanh',
    'csch',
    'sech',
    'coth',
    'arcsinh',
    'arccosh',
    'arctanh',
    'arccsch',
    'arcsech',
    'arccoth'
]

name_change_function = {  # the function names to replace after the expression has been solved
    'log': 'ln',  # replaces log with ln since log is treated as log base e
    'Abs': 'abs',
    'Mod': 'mod',
    'ceiling': 'ceil',
    'asin': 'arcsin',
    'acos': 'arccos',
    'atan': 'arctan',
    'acsc': 'arccsc',
    'asec': 'arcsec',
    'acot': 'arccot',
    'asinh': 'arcsinh',
    'acosh': 'arccosh',
    'atanh': 'arctanh',
    'acsch': 'arccsch',
    'asech': 'arcsech',
    'acoth': 'arccoth'
}

copy_notation = [
    ['π', 'φ', 'γ', 'θ'],
    functions
]

subscript = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
    'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ', 'v': 'ᵥ', 'x': 'ₓ', '+': '₊', '-': '₋', '=': '₌',
    '(': '₍', ')': '₎'
}

constant_values = get_constant_values(constants, 20)  # amount of digits used for calculations
constant_preview = get_constant_values(constants, 2)

# used for checking the type of symbol / if they are allowed -------------------------------------

accepted_constants = sorted(constants.keys())
accepted_functions = sorted(functions, key=len, reverse=True)  # sorts the functions from longest to shortest, so substring function errors won't occur: such as arcsin being misidentified as sin
accepted_characters = accepted_misc + accepted_variables + accepted_numbers + accepted_constants

# ------------------------------------------------------------------------------------------------

# used for changing the names of functions shown to the user -------------------------------------

name_change_function_keys = sorted(name_change_function.keys(), key=len, reverse=True)  # sorts the keys from longest to shortest

temp = {}
for key in constants:
    temp[constants[key][0]] = key

name_change_all = name_change_function.copy()
name_change_all.update(temp)

name_change_all_keys = sorted(name_change_all.keys(), key=len, reverse=True)

# ------------------------------------------------------------------------------------------------
