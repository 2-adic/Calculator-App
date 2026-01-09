from inspect import currentframe
from random import randint
import sympy as sy

import core.error_detection as error
from core.latex import convert_render_latex
import core.str_format as str_format
import core.symbols as symbols
from core.system_settings import get_data_path


class Solve:
    def __init__(self, expression: str, terms: dict[str, str] = dict(), answer_display: str = "Image", answer_copy: str = "Text", use_commas: bool = False, render_color: tuple[int, int, int] = (255, 255, 255), render_dpi: int = 300):

        self.__expression = str_format.remove_white_spaces(expression)
        self.__terms = terms.copy()

        self.__answer_display = answer_display
        self.__answer_copy = answer_copy
        self.__use_commas = use_commas
        self.__render_color = render_color
        self.__render_dpi = render_dpi

        self.__functions = tuple(getattr(self, f"_{self.__class__.__name__}__{name.lower()}") for name in symbols.accepted_functions)  # gets a list of all the functions

        self.__split_terms()  # split terms into variables and constants
        self.__format_variables()

        self.__is_approx = self.__is_approximate()

        self.__constant_counter = 0  # keeps track of the amount of constants used
        
        self.__answer_exact = None
        self.__answer_approximate = None

        self.__calculate()

    def __str__(self):
        """
        Returns the string representation of the solved expression.
        """

        return self.__expression_solved

    def print(self) -> None:
        """
        Prints the initial expression, and the solved expressions.
        """

        expression = self.__expression  # copies the expression to save the original
        expression = expression.replace('¦', '')
        for key in range(len(self.__functions)):
            expression = expression.replace(f"§{key}", symbols.accepted_functions[key])

        if self.__is_approx:  # if a constant value was used, only the approximate answer exists
            print(f"{expression} ≈ {self.__answer_approximate}")

        else:
            print(f"{expression} = {self.__answer_exact} ≈ {self.__answer_approximate}")

    def get_terms(self):
        """
        Returns the terms used in the expression.
        """

        return self.__terms

    def get_variables(self):
        """
        Returns the variables used in the expression.
        """

        return self.__variables

    def get_constants(self):
        """
        Returns the constants used in the expression.
        """

        return self.__constants
    
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

    def get_exact_copy(self) -> str:
        """
        Returns the answer to be copied.
        """

        if self.__answer_copy == "Text" or self.__answer_copy == "LaTeX":
            return self.__answer_exact_copy

        else:
            return get_data_path("latex_exact.png")

    def get_approximate_copy(self) -> str:
        """
        Returns the answer to be copied.
        """

        if self.__answer_copy == "Text" or self.__answer_copy == "LaTeX":
            return self.__answer_approximate_copy

        else:
            return get_data_path("latex_approximate.png")

    def is_text_used(self) -> bool:
        """
        Returns if text is used for the display.
        """

        return self.__answer_display == "Text" or self.__answer_display == "LaTeX"

    def uses_constant_literal(self) -> bool:
        """
        Returns True if a constant's literal value is used.
        """
        
        return any(self.__constants[constant] != symbols.constants[constant][0] for constant in self.__constants)

    def __split_terms(self) -> None:
        """
        Split terms into variables and constants.
        """

        self.__variables: dict[str, str] = {}
        self.__constants: dict[str, str] = {}

        for term in self.__terms:
            if term in symbols.accepted_variables: 
                self.__variables[term] = self.__terms[term]
            elif term in symbols.accepted_constants:
                self.__constants[term] = self.__terms[term]

    def __is_approximate(self) -> bool:
        """
        Returns if the expression requires an approximate answer.
        """

        for constant in self.__constants:
            if self.__constants[constant] != symbols.constants[constant][0]:
                return True

        return False

    def __calculate(self) -> None:
        """
        Calculates the solved expression in its exact and approximate form.
        """

        self.__format_before()
        self.__expression_solved = self.__solve(self.__expression_solved)  # solves the expression
        self.__exact()  # turns the solution into its exact form
        self.__approximate()  # turns the solution into its approximate form
        self.__result_simplification()

        if self.__answer_display == "Image" or self.__answer_copy == "Image":
            self.__render()

        self.__answer_exact_copy = self.__answer_exact
        self.__answer_approximate_copy = self.__answer_approximate

        if self.__answer_display != "LaTeX":
            self.__answer_exact = self.__format_after(self.__answer_exact)  # formats the exact and approximate answer
            self.__answer_approximate = self.__format_after(self.__answer_approximate)
        else:
            self.__answer_exact = self.__format_latex(self.__answer_exact)
            self.__answer_approximate = self.__format_latex(self.__answer_approximate)

        if self.__answer_copy == "Text":
            self.__answer_exact_copy = self.__format_after(self.__answer_exact_copy)
            self.__answer_approximate_copy = self.__format_after(self.__answer_approximate_copy)
        elif self.__answer_copy == "LaTeX":
            self.__answer_exact_copy = self.__format_latex(self.__answer_exact_copy)
            self.__answer_approximate_copy = self.__format_latex(self.__answer_approximate_copy)

    def __render(self) -> None:
        """
        Renders images of the solved expression.

        :param color: The color of the rendered text.
        :param dpi: The quality of the image (also affects how much it can be expanded).
        """

        exact = get_data_path("latex_exact.png")
        approximate = get_data_path("latex_approximate.png")

        if self.__answer_exact is not None:  # answer is not rendered if it is none
            convert_render_latex(self.__answer_exact, self.__use_commas, self.__render_color, self.__render_dpi, exact, self.__constant_counter)

        if self.__answer_approximate is not None:  # answer is not rendered if it is none
            convert_render_latex(self.__answer_approximate, self.__use_commas, self.__render_color, self.__render_dpi, approximate, self.__constant_counter)

    def __exact(self) -> None:
        """
        Turns the answer into its exact form.
        """

        if self.__is_approx:  # does not give an approximate value if a value for a constant is used
            return

        self.__answer_exact = sy.simplify(self.__expression_solved)

    def __custom_approximate(self, expression):
        """
        Returns the approximate value of the expression.
        """

        if expression.is_Atom:
            # if the expression is a number, evaluates it numerically
            if expression.is_Number:
                return expression.evalf()
            # if the expression is a symbol, returns it as is
            else:
                return expression

        # prevents exp from being evaluated
        elif expression.func == sy.exp:
            arg = expression.args[0]
            return sy.exp(self.__custom_approximate(arg), evaluate=False)

        else:
            # recursively applies custom_approx to all arguments of the expression
            return expression.func(*[self.__custom_approximate(arg) for arg in expression.args])

    def __approximate(self) -> None:
        """
        Turns the answer into its approximate form.
        """

        expression = sy.simplify(self.__expression_solved)
        self.__answer_approximate = self.__custom_approximate(expression)

    def __format_variables(self) -> None:
        """
        Sets blank variables equal to themselves.
        Performs variable substitution, and checks for circularly defined variables.
        """

        # sets blank variables equal to themselves
        for key in self.__variables:
            if self.__variables[key] == '':
                self.__variables[key] = key

        # apply function_convert to handle functions within variables
        for key in self.__variables:
            self.__variables[key] = str_format.function_convert(self.__variables[key])

        # performs chained variable substitution: a=b and b=5 -> a=5
        # keep iterating until no more substitutions can be made
        max_iterations = len(self.__variables) + 1  # prevent infinite loops
        for iteration in range(max_iterations):
            changes_made = False
            
            for var_name in self.__variables:
                if self.__variables[var_name] == var_name:
                    continue
                    
                # check if this variable's definition contains other variables
                if not str_format.contains_substring(self.__variables[var_name], list(self.__terms.keys())):
                    continue
                
                # substitute all other variables in this variable's definition
                original_value = self.__variables[var_name]
                for other_var in self.__variables:
                    if other_var != var_name and other_var in self.__variables[var_name]:
                        # replace variable with its definition
                        self.__variables[var_name] = self.__variables[var_name].replace(other_var, f"({self.__variables[other_var]})")
                
                # check for any changes
                if self.__variables[var_name] != original_value:
                    changes_made = True
            
            # if no changes, end loop
            if not changes_made:
                break

        error.circularly_defined(self.__variables)  # checks for circularly defined variables

    def __format_before(self) -> None:
        """
        Formats the expression before it is solved.
        """

        expression = self.__expression
        error.valid_symbols(expression)
        expression = str_format.function_convert(expression)  # converts functions to a format so implicit multiplication won't change them

        for x in expression:  # replaces all terms with their defined values
            if x in self.__variables:
                expression = expression.replace(f"{x}", f"({self.__variables[x]})")

        expression = self.__implicit_to_explicit(expression)  # changes the expression to use explicit multiplication
        expression = expression.replace('¦', '')  # removes the special character after implicit multiplication is formatted

        for key in sorted(self.__constants.keys(), key=lambda key: symbols.constant_order[key]):  # sorts the order to avoid substring replacement errors
            if self.__constants[key] == symbols.constants[key][0]:
                expression = expression.replace(key, symbols.constants[key][0])  # replaces the constant with it's recognized sympy symbol

            else:
                expression = expression.replace(key, f"({symbols.constant_values[key]})")

        self.__expression_solved = expression

    def __format_after(self, expression: str) -> str:
        """
        Performs some final formatting to the answer in its exact and approximate form.

        Used for copying purposes.
        """

        expression = str(expression)
        expression = expression.replace("**", '^')

        for key in symbols.name_change_all_keys:
            expression = expression.replace(key, symbols.name_change_all[key])

        return expression

    def __format_latex(self) -> str:
        """
        Formats the answer to be in LaTeX form.
        """

        # converts to LaTeX form
        latex = sy.latex(self.__expression, fold_short_frac=False)

        # replaces some symbols for proper latex formatting
        for key in list(symbols.replace_latex.keys()):
            latex = latex.replace(key, symbols.replace_latex[key])

        # replaces some functions names
        for key in symbols.name_change_all_keys:
            latex = latex.replace(key, symbols.name_change_all[key])

        latex = latex.replace(r"\bmod", r"\operatorname{mod}")  # fixes the latex formatting for mod

        return latex

    def __result_simplification(self) -> None:
        """
        Some functions require steps to be further simplified.
        """

        if not self.__is_approx:
            self.__answer_exact = sy.expand_log(self.__answer_exact, force=True)  # ln(e^x) -> x, ln(x^n) -> nln(x), etc

        self.__answer_approximate = sy.expand_log(self.__answer_approximate, force=True)  # ln(e^x) -> x, ln(x^n) -> nln(x), etc

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
                if num == '.':  # user error; displays "error" in answer box
                    print("Not yet fixed, do later")

                elif num != '' and '.' in num:  # num is not blank, and is a decimal
                    # replaces the first instance of each number
                    string = string.replace(num, f"({sy.Rational(num)})", 1)

                num = ''  # resets num

        return string

    def __solve(self, expression: str) -> str:
        """
        Solves all math functions within the string.

        :param expression: The string to be solved.
        :return: The solved string.
        """

        # solves a function with all of its inner functions and loops until all functions are solved
        while '§' in expression:
            expression = self.__function_check(expression)

        return expression

    def __function_check(self, expression: str) -> str:
        """
        Checks for math functions, solves them, and puts the answer back where the function was.

        :param expression: The expression with a possible function to be solved.
        :return: The expression with the solved function.
        """

        function_id, parameters, index_start, index_end = str_format.get_function_parameters(expression)
        ans = self.__functions[int(function_id)](*parameters)

        expression = str_format.replace_substring(expression, index_start - len(f"§{function_id}"), index_end, ans)

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

    def __integrate(self, f: str, x: str) -> str:  # "integrate(f, x)" -> ∫(f)dx
        """
        Integrates the expression given.

        :param f: The expression to integrate.
        :param x: Integrates with respect to the variable in x.
        """

        x = str(sy.simplify(x))  # x cannot contain parentheses
        error.char_is_variable(x, currentframe().f_code.co_name)  # checks if the independent variable/s are valid

        f = self.__solve(f)  # solves functions within this function before solving it

        # adds a unique constant
        new_constant = 'C' + str_format.to_subscript(str(self.__constant_counter))
        self.__constant_counter += 1

        # solves the integration
        return str(sy.integrate(sy.simplify(f), sy.symbols(x))) + " + " + new_constant

    def __log(self, x: str, b: str) -> str:
        return f"log({x},{b})"

    def __ln(self, x: str) -> str:
        return f"ln({x})"

    def __exp(self, x: str) -> str:
        return f"exp({x})"

    def __pow(self, x: str, y: str) -> str:
        return f"({x})**({y})"

    def __root(self, x: str, y: str) -> str:
        return f"({x})**(1/{y})"

    def __sqrt(self, x: str) -> str:
        return f"sqrt({x})"

    def __floor(self, x: str) -> str:
        return f"floor({x})"

    def __ceil(self, x: str) -> str:
        return f"ceiling({x})"

    def __sign(self, x: str) -> str:
        return f"sign({x})"

    def __random(self, a: str, b: str) -> str:

        a = str(sy.simplify(a))
        b = str(sy.simplify(b))

        error.all_is_int((a, b), currentframe().f_code.co_name)

        return f"{randint(int(a), int(b))}"

    def __abs(self, x: str) -> str:
        return f"Abs({x})"

    def __mod(self, x: str, y: str) -> str:
        return f"Mod({x},{y})"

    def __sin(self, x: str) -> str:
        return f"sin({x})"

    def __cos(self, x: str) -> str:
        return f"cos({x})"

    def __tan(self, x: str) -> str:
        return f"tan({x})"

    def __csc(self, x: str) -> str:
        return f"csc({x})"

    def __sec(self, x: str) -> str:
        return f"sec({x})"

    def __cot(self, x: str) -> str:
        return f"cot({x})"

    def __asin(self, x: str) -> str:
        return f"asin({x})"

    def __acos(self, x: str) -> str:
        return f"acos({x})"

    def __atan(self, x: str) -> str:
        return f"atan({x})"

    def __acsc(self, x: str) -> str:
        return f"acsc({x})"

    def __asec(self, x: str) -> str:
        return f"asec({x})"

    def __acot(self, x: str) -> str:
        return f"acot({x})"

    def __sinh(self, x: str) -> str:
        return f"sinh({x})"

    def __cosh(self, x: str) -> str:
        return f"cosh({x})"

    def __tanh(self, x: str) -> str:
        return f"tanh({x})"

    def __csch(self, x: str) -> str:
        return f"csch({x})"

    def __sech(self, x: str) -> str:
        return f"sech({x})"

    def __coth(self, x: str) -> str:
        return f"coth({x})"

    def __asinh(self, x: str) -> str:
        return f"asinh({x})"

    def __acosh(self, x: str) -> str:
        return f"acosh({x})"

    def __atanh(self, x: str) -> str:
        return f"atanh({x})"

    def __acsch(self, x: str) -> str:
        return f"acsch({x})"

    def __asech(self, x: str) -> str:
        return f"asech({x})"

    def __acoth(self, x: str) -> str:
        return f"acoth({x})"
