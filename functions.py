import sympy as sy
import symbols
import str_format

constant_counter = 0  # keeps track of the amount of constants used


def solve(string: str) -> str:
    """
    Solves all math functions within the string.

    :param string: The string to be solved.
    :return: The solved string.
    """

    # removes spaces to fix formatting issues
    string = string.replace(' ', '')

    # solves a function with all of its inner functions and loops until all functions are solved
    while str_format.contains(string, symbols.accepted_functions):
        string = function_check(string)

    return string


def function_check(f: str) -> str:
    """
    Checks for math functions, solves them, and puts the answer back where the function was.

    :param f: The expression with a possible function to be solved.
    :return: The expression with the solved function.
    """

    # may not need to check for this
    if not str_format.contains(f, symbols.accepted_functions):
        return f

    function = str_format.find_substring_index(f, symbols.accepted_functions)
    info = str_format.get_elements_in_bracket(f, function[1])
    elements = info[0]

    if function[0] == 'Integrate':
        ans = integrate(elements[0], elements[1])

        f = str_format.replace_substring(f, function[1] - len('Integrate'), info[1], ans)
        return f


def integrate(f: str, x: str) -> str:  # 'Integrate[f, x]' -> ∫(f)dx
    """
    Integrates the expression given.

    :param f: The expression to integrate.
    :param x: Integrates with respect to the variable in x.
    :return:
    """

    # b can only be one variable
    if x not in symbols.accepted_variables:
        raise 'Error: Second parameter not formatted correctly'

    # solves other functions inside the integral before solving the integral
    if str_format.contains(f, symbols.accepted_functions):
        f = function_check(f)

    # adds a unique constant
    global constant_counter
    new_constant = 'C' + str_format.to_subscript(str(constant_counter))
    constant_counter += 1

    # solves the integration
    return str(sy.integrate(sy.sympify(f), sy.symbols(x))) + ' + ' + new_constant
