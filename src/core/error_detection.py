from core.symbols import accepted_characters, accepted_variables


def valid_symbols(expression: str) -> None:
    """
    Raises an error if an unknown symbol is used in the expression.
    """

    for char in expression:
        if char not in accepted_characters:
            raise Exception(f"unknown symbol '{char}'")


def char_is_variable(char: str, function_name: str) -> None:
    """
    Checks if the second parameter for integration and differentiation is valid.

    This function will be changed once the user can put multiple variables for the second parameter.
    """

    function_name = function_name[2:]  # removes the underscores from the function name

    if len(char) != 1:
        raise Exception(f"{function_name}; second parameter can only include one variable")

    if char not in accepted_variables:
        raise Exception(f"{function_name}; '{char}' is not an accepted variable")


def all_is_int(array: tuple[str, ...], function_name: str) -> None:
    """
    Checks if all the elements in a list are ints or not.

    Assumes all elements are in the form: _ or _.__
    """

    function_name = function_name[2:]  # removes the underscores from the function name

    for element in array:
        if '/' in element:  # number is a fraction (not an int since fractions are simplified)
            raise Exception(f"{function_name}; a parameter is not an int")

        if '.' in element:  # if a non 0 appears after a decimal point, it is not an int

            element = element[element.find('.') + 1:]

            for char in element:
                if char != '0':
                    raise Exception(f"{function_name}; a parameter is not an int")


def circularly_defined(variables: dict[str, str]) -> None:
    """
    Raises an error if a variable is circularly defined.
    """

    for x in variables:
        if x in variables[x] and f"({x})" != variables[x] and x != variables[x]:
            raise Exception(f"'{x}' is circularly defined")
