import sympy as sy
import symbols
import str_format as form
from latex import convert_render_latex
from files import file_path


class Solve:
    def __init__(self, expression: str, constant_symbol_used: dict[str, bool], render_color: tuple[int, int, int] = (255, 255, 255), render_dpi: int = 300):

        self.__funct = tuple(getattr(self, f'_{self.__class__.__name__}__{name.lower()}') for name in symbols.accepted_functions)  # gets a list of all the functions

        self.__constant_counter = 0  # keeps track of the amount of constants used
        self.__expression = expression
        self.__expression = self.__expression.replace(' ', '')  # removes spaces to fix formatting issues

        self.__is_value_used = not all(constant_symbol_used.values())  # gets a bool for if a constant value was used
        self.__error = None  # saves the reason for an error
        self.__answer_exact = None
        self.__answer_approximate = None

        format_expression = self.__format_before(self.__expression, constant_symbol_used)
        self.__expression_solved = self.__solve(format_expression)  # solves the expression
        self.__exact()  # turns the solution into its exact form
        self.__approximate()  # turns the solution into its approximate form
        self.__render(render_color, render_dpi)  # renders the image of the exact and approximate solutions
        self.__format_after()  # formats the exact and approximate answer

        if self.__error is not None:
            print(f'Error: {self.__error}')

    def __str__(self):
        return self.__expression_solved

    def print(self):
        """
        Prints the initial expression, and the solved expressions.
        """

        expression = self.__expression  # copies the expression to save the original
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

    def __render(self, color: tuple[int, int, int] = (255, 255, 255), dpi: int = 300):
        """
        Renders images of the solved expression.

        :param color: The color of the rendered text.
        :param dpi: The
        """

        exact = file_path('latex_exact.png')
        approximate = file_path('latex_approximate.png')

        if self.__answer_exact is not None:  # answer is not rendered if it is none
            convert_render_latex(self.__answer_exact, color, dpi, exact, self.__constant_counter)

        if self.__answer_approximate is not None:  # answer is not rendered if it is none
            convert_render_latex(self.__answer_approximate, color, dpi, approximate, self.__constant_counter)

    def __exact(self):
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
            # if the expression is a number, evaluate it numerically
            if expression.is_Number:
                return expression.evalf()
            # if the expression is a symbol, return it as is
            else:
                return expression
        else:
            # recursively apply custom_approx to all arguments of the expression
            return expression.func(*[self.__custom_approx(arg) for arg in expression.args])

    def __approximate(self):
        """
        Turns the answer into its approximate form.
        """

        try:
            expression = sy.simplify(self.__expression_solved)
            self.__answer_approximate = self.__custom_approx(expression)

        except Exception as e:
            self.__answer_approximate = 'Error'
            self.__error = e

    def __format_before(self, expression: str, constant_symbol_used: dict[str, bool]) -> str:
        """
        Formats the expression before it is solved.
        """

        for key in list(constant_symbol_used.keys()):
            if constant_symbol_used[key]:
                expression = expression.replace(key, symbols.constants[key][0])  # replaces the constant with it's recognized sympy symbol

            else:
                expression = expression.replace(key, f'({symbols.constant_values[key]})')

        return expression

    def __format_after(self):
        """
        Performs some final formatting to the answer in its exact and approximate form.
        """

        self.__answer_exact = str(self.__answer_exact).replace('**', '^')
        self.__answer_approximate = str(self.__answer_approximate).replace('**', '^')

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

    def __integrate(self, f: str, x: str) -> str:  # 'Integrate[f, x]' -> ∫(f)dx
        """
        Integrates the expression given.

        :param f: The expression to integrate.
        :param x: Integrates with respect to the variable in x.
        """

        # checks if the independent variable is a valid variable
        x = form.remove_parentheses(x)  # x cannot contain parentheses
        if x not in symbols.accepted_variables:
            raise 'Error: Second parameter not formatted correctly'

        # solves other functions inside the function before solving the function
        while '§' in f:
            f = self.__function_check(f)

        # adds a unique constant
        new_constant = 'C' + form.to_subscript(str(self.__constant_counter))
        self.__constant_counter += 1

        # solves the integration
        return str(sy.integrate(sy.simplify(f), sy.symbols(x))) + ' + ' + new_constant

    def __ln(self, x: str):  # Ln[x]
        return f'ln({x})'

    def __sin(self, x: str):  # Sin[x]
        # x = f'({x})*(pi/180)'
        print('Add functionality for degrees.')
        return f'sin({x})'

    def __cos(self, x: str):  # Cos[x]
        return f'cos({x})'


''' 
Needs fixing:
Displays log in terms of e.
Doesn't display the log base, and instead does 'log(x, base)' -> log(x)/log(base).
Made it so a default base value is not given so the user has to specify the specific value. (clears confusing about the default base being e vs 10 vs 2)

def log(self, x: str, base: str):  # Log[x, base]
    return f'log({x}, {base})'
'''
