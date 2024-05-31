import sympy as sy
import symbols
import str_format as form
from latex import convert_render_latex
from files import file_path
import constants


class Solve:
    def __init__(self, expression: str, is_value_used: dict[str, bool], render_color: tuple[int, int, int] = (255, 255, 255), render_dpi: int = 300):

        self.funct = {
            '0': self.integrate, '1': self.sin, '2': self.cos
        }

        self.constant_counter = 0  # keeps track of the amount of constants used
        self.expression = expression
        self.expression = self.expression.replace(' ', '')  # removes spaces to fix formatting issues

        self.error = None  # saves the reason for an error
        self.answer_exact = None
        self.answer_approximate = None
        format_expression = self.format_before(self.expression, is_value_used)
        self.expression_solved = self.solve(format_expression)  # solves the expression
        self.exact()  # turns the solution into its exact form
        self.approximate()  # turns the solution into its approximate form
        self.render(render_color, render_dpi)  # renders the image of the exact and approximate solutions
        # self.format_after()  # formats the exact and approximate answer forms

        if self.error is not None:
            print(f'Error: {self.error}')

    def __str__(self):
        return self.expression_solved

    def render(self, color: tuple[int, int, int] = (255, 255, 255), dpi: int = 300):
        """
        Renders images of the solved expression.

        :param color: The color of the rendered text.
        :param dpi: The
        """

        exact = file_path('latex_exact.png')
        approximate = file_path('latex_approximate.png')

        convert_render_latex(self.answer_exact, color, dpi, exact, self.constant_counter)
        convert_render_latex(self.answer_approximate, color, dpi, approximate, self.constant_counter)

    def print(self):
        """
        Prints the initial expression, and the solved expression.
        """

        expression = self.expression  # copies the expression to save the original
        for key in list(self.funct.keys()):
            expression = expression.replace(f'§{key}', symbols.accepted_functions[int(key)])

        print(f'{expression} = {self.expression_solved}')

    def exact(self):
        """
        Turns the answer into its exact form.
        """

        try:
            self.answer_exact = sy.simplify(self.expression_solved)

        except Exception as e:
            self.answer_exact = 'Error'
            self.error = e

    def get_exact(self) -> str:
        """
        Returns the answer in its exact form.
        """

        return self.answer_exact

    def custom_approx(self, expression):
        if expression.is_Atom:
            # if the expression is a number, evaluate it numerically
            if expression.is_Number:
                return expression.evalf()
            # if the expression is a symbol, return it as is
            else:
                return expression
        else:
            # recursively apply self.custom_approx to all arguments of the expression
            return expression.func(*[self.custom_approx(arg) for arg in expression.args])

    def approximate(self):
        """
        Turns the answer into its approximate form.
        """

        try:
            expression = sy.simplify(self.expression_solved)
            self.answer_approximate = self.custom_approx(expression)

        except Exception as e:
            self.answer_approximate = 'Error'
            self.error = e

    def get_approximate(self) -> str:
        """
        Returns the answer in its approximate form.
        """
        return self.answer_approximate

    def format_before(self, expression: str, is_value_used: dict[str, bool]) -> str:
        """
        Formats the expression before it is solved.
        """

        constant_values = constants.get_constant_values(constants.constants, 20)

        for key in list(is_value_used.keys()):
            if is_value_used[key]:
                if key == 'i':
                    expression = expression.replace('i', 'I')
                elif key == 'e':
                    expression = expression.replace('e', 'E')
                elif key == 'π':
                    expression = expression.replace('π', 'pi')

            else:
                expression = expression.replace(key, f'({constant_values[key]})')

        return expression

    def format_after(self):
        """
        Performs some final formatting to the answer in its exact and approximate form.
        """

        self.answer_exact = self.answer_exact.replace('**', '^')
        self.answer_approximate = self.answer_approximate.replace('**', '^')

    def solve(self, string: str) -> str:
        """
        Solves all math functions within the string.

        :param string: The string to be solved.
        :return: The solved string.
        """

        # solves a function with all of its inner functions and loops until all functions are solved
        while '§' in string:
            string = self.function_check(string)

        return string

    def function_check(self, expression: str) -> str:
        """
        Checks for math functions, solves them, and puts the answer back where the function was.

        :param expression: The expression with a possible function to be solved.
        :return: The expression with the solved function.
        """

        function_id, parameters, index_start, index_end = form.get_function_parameters(expression)
        ans = self.funct[function_id](*parameters)

        expression = form.replace_substring(expression, index_start - len(f'§{function_id}'), index_end, ans)

        return expression

    def integrate(self, f: str, x: str) -> str:  # 'Integrate[f, x]' -> ∫(f)dx
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
            f = self.function_check(f)

        # adds a unique constant
        new_constant = 'C' + form.to_subscript(str(self.constant_counter))
        self.constant_counter += 1

        # solves the integration
        return str(sy.integrate(sy.simplify(f), sy.symbols(x))) + ' + ' + new_constant

    def sin(self, x: str):  # Sin[x]
        #x = f'({x})*(180/PI)'
        return f'sin({x})'

    def cos(self, x: str):  # Cin[x]
        return f'cos({x})'
