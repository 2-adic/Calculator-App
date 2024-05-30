import sympy as sy
import symbols
import str_format as form
from latex import convert_render_latex


class Solve:
    def __init__(self, expression: str):

        self.funct = {
            0: self.integrate, 1: self.sin, 2: self.cos
        }

        self.constant_counter = 0  # keeps track of the amount of constants used
        self.expression = expression
        self.expression = self.expression.replace(' ', '')  # removes spaces to fix formatting issues

        self.expression_solved = self.solve(self.expression)

    def __str__(self):
        return self.expression_solved

    def render(self, color: tuple[int, int, int] = (255, 255, 255)):
        """
        Renders an image of the solved expression.

        :param color: The color of the rendered text.
        """

        convert_render_latex(self.expression_solved, color, constant_amount=self.constant_counter)

    def print(self):
        """
        Prints the initial expression, and the solved expression.
        """

        print(f'{self.expression} = {self.expression_solved}')

    def solve(self, string: str) -> str:
        """
        Solves all math functions within the string.

        :param string: The string to be solved.
        :return: The solved string.
        """

        # solves a function with all of its inner functions and loops until all functions are solved
        while form.contains(string, symbols.accepted_functions):
            string = self.function_check(string)

        return string

    def function_check(self, f: str) -> str:
        """
        Checks for math functions, solves them, and puts the answer back where the function was.

        :param f: The expression with a possible function to be solved.
        :return: The expression with the solved function.
        """

        # may not need to check for this
        if not form.contains(f, symbols.accepted_functions):
            return f

        # need to redo this to make it easier to work with
        function = form.find_substring_index(f, symbols.accepted_functions)
        info = form.get_elements_in_bracket(f, function[1])
        parameter = info[0]

        if function[0] == 'Integrate':
            ans = self.integrate(parameter[0], parameter[1])

            f = form.replace_substring(f, function[1] - len('Integrate'), info[1], ans)
            return f

        elif function[0] == 'Sin':
            ans = self.sin(parameter[0])

            f = form.replace_substring(f, function[1] - len('Sin'), info[1], ans)
            return f

        elif function[0] == 'Cos':
            ans = self.cos(parameter[0])

            f = form.replace_substring(f, function[1] - len('Cos'), info[1], ans)
            return f

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

        # solves other functions inside the integral before solving the integral
        if form.contains(f, symbols.accepted_functions):
            f = self.function_check(f)

        # adds a unique constant
        new_constant = 'C' + form.to_subscript(str(self.constant_counter))
        self.constant_counter += 1

        # solves the integration
        return str(sy.integrate(sy.sympify(f), sy.symbols(x))) + ' + ' + new_constant

    def sin(self, x: str):  # Sin[x]
        return f'sin({x})'

    def cos(self, x: str):  # Cin[x]
        return f'cos({x})'
