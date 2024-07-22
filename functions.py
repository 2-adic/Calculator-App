import sympy as sy
import symbols
import str_format as form
from latex import convert_render_latex
from files import file_path
import str_format
from random import randint
import error_detection as error
from inspect import currentframe


class Solve:
    def __init__(self, expression: str, variables: dict[str, str] = dict(), constant_symbol_used: dict[str, bool] = dict(), use_degrees: bool = False, use_commas: bool = False, render_color: tuple[int, int, int] = (255, 255, 255), render_dpi: int = 300):

        self.__funct = tuple(getattr(self, f'_{self.__class__.__name__}__{name.lower()}') for name in symbols.accepted_functions)  # gets a list of all the functions

        self.__use_degrees = use_degrees
        self.__use_commas = use_commas

        self.__constant_counter = 0  # keeps track of the amount of constants used
        self.__expression_save = self.__remove_white_spaces(expression)

        self.__is_value_used = not all(constant_symbol_used.values())  # gets a bool for if a constant value was used
        self.__error = None  # saves the reason for an error
        self.__answer_exact = None
        self.__answer_approximate = None

        self.__format_before(variables, constant_symbol_used)
        self.__expression_solved = self.__solve(self.__expression_solved)  # solves the expression
        self.__exact()  # turns the solution into its exact form
        self.__approximate()  # turns the solution into its approximate form
        self.__result_simplification()
        self.__render(render_color, render_dpi)  # renders the image of the exact and approximate solutions
        self.__format_after()  # formats the exact and approximate answer

        if self.__error is not None:
            print(f'Error: {self.__error}')

    def __str__(self):
        return self.__expression_solved

    def print(self) -> None:
        """
        Prints the initial expression, and the solved expressions.
        """

        expression = self.__expression_save  # copies the expression to save the original
        expression = expression.replace('¦', '')
        for key in range(len(self.__funct)):
            expression = expression.replace(f'§{key}', symbols.accepted_functions[key])

        if self.__is_value_used:  # if a constant value was used, only the approximate answer exists
            print(f'{expression} ≈ {self.__answer_approximate}')

        else:
            print(f'{expression} = {self.__answer_exact} ≈ {self.__answer_approximate}')

    def get_exact(self) -> str:
        """
        Returns the answer in its exact form.
        """

        return self.__answer_exact

    def get_approximate(self) -> str:
        """
        Returns the answer in its approximate form.
        """
        return self.__answer_approximate

    def __render(self, color: tuple[int, int, int] = (255, 255, 255), dpi: int = 300) -> None:
        """
        Renders images of the solved expression.

        :param color: The color of the rendered text.
        :param dpi: The
        """

        exact = file_path('latex_exact.png')
        approximate = file_path('latex_approximate.png')

        if self.__answer_exact is not None:  # answer is not rendered if it is none
            convert_render_latex(self.__answer_exact, self.__use_commas, color, dpi, exact, self.__constant_counter)

        if self.__answer_approximate is not None:  # answer is not rendered if it is none
            convert_render_latex(self.__answer_approximate, self.__use_commas, color, dpi, approximate, self.__constant_counter)

    def __exact(self) -> None:
        """
        Turns the answer into its exact form.
        """

        if self.__is_value_used:  # does not give an approximate value if a value for a constant is used
            return

        try:
            self.__answer_exact = sy.simplify(self.__expression_solved)

        except Exception as e:
            self.__answer_exact = 'Error'
            self.__error = e

    def __custom_approx(self, expression):
        if expression.is_Atom:
            # if the expression is a number, evaluates it numerically
            if expression.is_Number:
                return expression.evalf()
            # if the expression is a symbol, returns it as is
            else:
                return expression
        else:
            # recursively applies custom_approx to all arguments of the expression
            return expression.func(*[self.__custom_approx(arg) for arg in expression.args])

    def __approximate(self) -> None:
        """
        Turns the answer into its approximate form.
        """

        try:
            expression = sy.simplify(self.__expression_solved)
            self.__answer_approximate = self.__custom_approx(expression)

        except Exception as e:
            self.__answer_approximate = 'Error'
            self.__error = e

    def __format_before(self, variables: dict[str, str], constant_symbol_used: dict[str, bool]) -> None:
        """
        Formats the expression before it is solved.
        """

        expression = self.__expression_save
        error.valid_symbols(expression)
        expression = str_format.function_convert(expression)  # converts functions to a format so implicit multiplication won't change them

        for x in expression:  # replaces all variables with their defined values
            if x in variables:
                expression = expression.replace(f'{x}', f'({variables[x]})')

        expression = self.__implicit_to_explicit(expression)  # changes the expression to use explicit multiplication
        expression = expression.replace('¦', '')  # removes the special character after implicit multiplication is formatted

        for key in sorted(constant_symbol_used.keys(), key=lambda key: symbols.constant_order[key]):  # sorts the order to avoid substring replacement errors
            if constant_symbol_used[key]:
                expression = expression.replace(key, symbols.constants[key][0])  # replaces the constant with it's recognized sympy symbol

            else:
                expression = expression.replace(key, f'({symbols.constant_values[key]})')

        self.__expression_solved = expression

    def __format_after(self) -> None:
        """
        Performs some final formatting to the answer in its exact and approximate form.

        Used for copying purposes.
        """

        self.__answer_exact = str(self.__answer_exact)
        self.__answer_approximate = str(self.__answer_approximate)

        self.__answer_exact = self.__answer_exact.replace('**', '^')
        self.__answer_approximate = self.__answer_approximate.replace('**', '^')

        for key in symbols.name_change_all_keys:
            self.__answer_exact = self.__answer_exact.replace(key, symbols.name_change_all[key])
            self.__answer_approximate = self.__answer_approximate.replace(key, symbols.name_change_all[key])

    def __result_simplification(self) -> None:
        """
        Some functions require steps to be further simplified.
        """

        # this is needed for: ln(e^x) -> x, ln(x^n) -> nln(x), etc
        if not self.__is_value_used:
            self.__answer_exact = sy.expand_log(self.__answer_exact, force=True)

        self.__answer_approximate = sy.expand_log(self.__answer_approximate, force=True)

    def __remove_white_spaces(self, string) -> str:
        """
        Removes all white spaces.
        """

        string = string.replace(' ', '')
        string = string.replace('\n', '')
        string = string.replace('\t', '')

        return string

    def __implicit_to_explicit(self, string: str) -> str:
        """
        Reformats the expression from implicit multiplication to explicit multiplication.

        Gives the user more freedom to type expressions different ways.
        """

        # adds multiplication symbol for implicit multiplication
        x = 0
        while x < len(string) - 1:
            if string[x] in symbols.accepted_variables or string[x] in symbols.accepted_constants or string[x] in symbols.accepted_numbers or string[x] == ')' or string[x] == ']' or string[x] == '.':
                if string[x + 1] in symbols.accepted_variables or string[x + 1] in symbols.accepted_constants or string[x + 1] == '(' or string[x + 1] == '§':
                    # inserts in front of x
                    string = string[:x + 1] + '*' + string[x + 1:]
                    x -= 1
            x += 1

        # turns all decimals into rationals
        temp = string + ' '  # character added to end of string to recognize final number
        num = ''
        for x in temp:
            if x in symbols.accepted_numbers or x == '.':
                num += x
            else:
                if num == '.':  # user error; displays 'error' in answer box
                    print('Not yet fixed, do later')

                elif num != '' and '.' in num:  # num is not blank, and is a decimal
                    # replaces the first instance of each number
                    string = string.replace(num, f'({sy.Rational(num)})', 1)

                num = ''  # resets num

        return string

    def __solve(self, string: str) -> str:
        """
        Solves all math functions within the string.

        :param string: The string to be solved.
        :return: The solved string.
        """

        # solves a function with all of its inner functions and loops until all functions are solved
        while '§' in string:
            string = self.__function_check(string)

        return string

    def __function_check(self, expression: str) -> str:
        """
        Checks for math functions, solves them, and puts the answer back where the function was.

        :param expression: The expression with a possible function to be solved.
        :return: The expression with the solved function.
        """

        function_id, parameters, index_start, index_end = form.get_function_parameters(expression)
        ans = self.__funct[int(function_id)](*parameters)

        expression = form.replace_substring(expression, index_start - len(f'§{function_id}'), index_end, ans)

        return expression

    def __diff(self, f: str, x: str) -> str:
        """
        Differentiates the expression given.

        :param f: The expression to differentiate.
        :param x: Differentiates with respect to the variable in x.
        """

        x = str(sy.simplify(x))  # x cannot contain parentheses
        error.char_is_variable(x, currentframe().f_code.co_name)  # checks if the independent variable is valid

        f = self.__solve(f)  # solves functions within this function before solving it

        # solves the differentiation
        return str(sy.diff(sy.simplify(f), sy.symbols(x)))

    def __integrate(self, f: str, x: str) -> str:  # 'integrate(f, x)' -> ∫(f)dx
        """
        Integrates the expression given.

        :param f: The expression to integrate.
        :param x: Integrates with respect to the variable in x.
        """

        x = str(sy.simplify(x))  # x cannot contain parentheses
        error.char_is_variable(x, currentframe().f_code.co_name)  # checks if the independent variable/s are valid

        f = self.__solve(f)  # solves functions within this function before solving it

        # adds a unique constant
        new_constant = 'C' + form.to_subscript(str(self.__constant_counter))
        self.__constant_counter += 1

        # solves the integration
        return str(sy.integrate(sy.simplify(f), sy.symbols(x))) + ' + ' + new_constant

    def __log(self, x: str, b: str) -> str:
        return f'log({x},{b})'

    def __ln(self, x: str) -> str:
        return f'ln({x})'

    def __exp(self, x: str) -> str:
        return f'exp({x})'

    def __pow(self, x: str, y: str) -> str:
        return f'{x}**{y}'

    def __root(self, x: str, y: str) -> str:
        return f'{x}**(1/{y})'

    def __floor(self, x: str) -> str:
        return f'floor({x})'

    def __ceil(self, x: str) -> str:
        return f'ceiling({x})'

    def __sign(self, x: str) -> str:
        return f'sign({x})'

    def __random(self, a: str, b: str) -> str:

        a = str(sy.simplify(a))
        b = str(sy.simplify(b))

        error.all_is_int((a, b), currentframe().f_code.co_name)

        return f'{randint(int(a), int(b))}'

    def __abs(self, x: str) -> str:
        return f'Abs({x})'

    def __mod(self, x: str, y: str) -> str:
        return f'Mod({x},{y})'

    def __sin(self, x: str) -> str:
        '''
        if self.__use_degrees:
            x = f'({x})*(pi/180)'
        '''
        return f'sin({x})'

    def __cos(self, x: str) -> str:
        return f'cos({x})'

    def __tan(self, x: str) -> str:
        return f'tan({x})'

    def __csc(self, x: str) -> str:
        return f'csc({x})'

    def __sec(self, x: str) -> str:
        return f'sec({x})'

    def __cot(self, x: str) -> str:
        return f'cot({x})'

    def __arcsin(self, x: str) -> str:
        return f'asin({x})'

    def __arccos(self, x: str) -> str:
        return f'acos({x})'

    def __arctan(self, x: str) -> str:
        return f'atan({x})'

    def __arccsc(self, x: str) -> str:
        return f'acsc({x})'

    def __arcsec(self, x: str) -> str:
        return f'asec({x})'

    def __arccot(self, x: str) -> str:
        return f'acot({x})'

    def __sinh(self, x: str) -> str:
        return f'sinh({x})'

    def __cosh(self, x: str) -> str:
        return f'cosh({x})'

    def __tanh(self, x: str) -> str:
        return f'tanh({x})'

    def __csch(self, x: str) -> str:
        return f'csch({x})'

    def __sech(self, x: str) -> str:
        return f'sech({x})'

    def __coth(self, x: str) -> str:
        return f'coth({x})'

    def __arcsinh(self, x: str) -> str:
        return f'asinh({x})'

    def __arccosh(self, x: str) -> str:
        return f'acosh({x})'

    def __arctanh(self, x: str) -> str:
        return f'atanh({x})'

    def __arccsch(self, x: str) -> str:
        return f'acsch({x})'

    def __arcsech(self, x: str) -> str:
        return f'asech({x})'

    def __arccoth(self, x: str) -> str:
        return f'acoth({x})'
