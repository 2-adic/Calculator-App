import symbols

symbol_front = '┌'
symbol_back = '┐'


def to_subscript(string: str) -> str:
    """
    Converts a string to subscript of the same characters.

    :param string: String to convert.
    :return: Converted string.
    """

    # loops each character and adds to an output string based on a dictionary
    final = ''
    for x in string:
        final += symbols.subscript[x]

    return final


def contains(string: str, array: list) -> bool:
    """
    Returns if a string contains at least one substring + '[' from a list of strings.

    :param string: String which may contain substring + '['.
    :param array: List of substrings to check in string.
    """

    for x in array:
        x += '['
        if x in string:
            return True

    return False


def find_substring_index(string: str, array: list) -> tuple[str, int]:
    """
    Finds the first substring from the array within the string, and returns the index of the '[' after the substring.

    :param string: String to be checked for a substring.
    :param array: List of possible substrings.
    """

    for substring in array:
        if substring in string:

            return substring, string.find(substring) + len(substring)


def get_elements_in_bracket(string: str, index: int) -> tuple[list, int]:
    """
    Only call this function if a mathematical function with brackets is in the string.

    :param string: The string with the mathematical function.
    :param index: The index of the left bracket.
    :return: A list with the elements separated by commas within the brackets.
    """

    element_array = []
    nested_level = 0

    element = ''

    # loops through each character starting at the starting bracket
    for i in range(index, len(string)):
        char = string[i]

        # gets the bracket level
        if char == '[':
            nested_level += 1
        elif char == ']':
            nested_level -= 1

            # if the ending bracket is found, the array is returned
            if nested_level == 0:
                element_array.append(element)
                return element_array, i

        # if a comma separates an element of the base bracket level, the old element is stored, and the element string is reset
        if char == ',' and nested_level == 1:

            # checks if teh element is empty
            if element == '':
                print('Error: String not formatted properly; an element is empty.')

            element_array.append(element)
            element = ''

        # if the element is not the starting bracket, it is added to the element string
        elif i != index:
            element += char

    # if no last bracket is found, the string is formatted incorrectly
    raise 'Error: String not formatted properly; No final bracket found.'


def replace_substring(original: str, start: int, end: int, replacement: str) -> str:
    """
    Replaces the given substring with the new substring.

    :param original: The string with the substring.
    :param start: The first index of the substring to be replaced.
    :param end: The last index of the substring to be replaced.
    :param replacement: The substring to replace the old substring.
    :return: The finalized string.
    """

    # Ensure the end index is not beyond the string length
    end = min(end, len(original))
    # Slice the original string and insert the replacement
    return original[:start] + '(' + str(replacement) + ')' + original[end + 1:]


def contains_substring(string: str, array: list) -> bool:
    """
    Returns if a substring is in the given string.

    :param string: String to be checked.
    :param array: List of all substrings to check.
    :return:
    """

    # tests all substring in the array
    for x in array:
        if x in string:
            return True  # if one is found, a substring was in the string

    return False  # if none were found, a substring is not in the string


# --------------------------------------------------------------------------------------------------------


def function_convert(string: str) -> str:
    """
    Transforms all functions into a format that won't get messed up by the implicit multiplication converter.
    """

    for i in range(len(symbols.accepted_functions)):
        string = string.replace(symbols.accepted_functions[i], f'{symbol_front}{i}{symbol_back}')

    return string


def function_unconvert(string: str) -> str:
    """
    Changes all converted function into their unconverted form.
    """

    for i in range(len(symbols.accepted_functions)):
        string = string.replace(f'{symbol_front}{i}{symbol_back}', symbols.accepted_functions[i])

    return string


def remove_parentheses(string: str) -> str:
    """
    Only use if 1 variable / number is in the string.
    ((x)) -> x
    """

    string = string.replace('(', '')
    string = string.replace(')', '')

    return string


def generate_function_dictionary(dictionary_name: str) -> None:
    """
    Used to replace the function dictionary when more functions are added.
    """

    string = f'{dictionary_name} = {{\n    '

    for i, function in enumerate(symbols.accepted_functions):
        string += f'{i}: self.{function.lower()}, '

    string = string[:-2]
    string += '\n}'

    print(string)
