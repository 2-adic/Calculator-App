# Calculator App:
Calculator App is a plain text expression simplifier.

![example](https://github.com/user-attachments/assets/63c7ff34-3a8d-4066-afbd-995be43806e1)

# How to Use:

Download the latest release [here](https://github.com/2-adic/Calculator-App/releases/latest).

Follow the steps provided through the installer.

Start typing an expression in the top left text box. Be sure to use the correct [syntax](#syntax).

![typing_expression](https://github.com/user-attachments/assets/ee3b6552-ef8f-4b1f-9895-97fe06cf78de)

Click the answer button to simplify the expression.

![answer_button](https://github.com/user-attachments/assets/dfbfbfd4-7467-4d95-9bea-ce78af995753)

The format button is used to switch between the exact and approximate answer.

![changing_format](https://github.com/user-attachments/assets/458e0b2e-9b52-4546-833c-63cd998057f1)

Variables can be defined as expressions containing functions, constants, and other variables. Functions and constants can be copied from the notation tab.

![variable_expressions](https://github.com/user-attachments/assets/7d14f8c2-a7b3-4cf0-b297-81e291bbe3c1)

# Syntax:

Functions can be typed manually or copied from the notations tab. Some functions require two or more parameters.
- ````sin(π/2 - x)````&emsp;→&emsp;cos(x)
- ````integrate(sin(x) + y, x)````&emsp;→&emsp;C<sub>0</sub> + y * x - cos(x)

Implicit multiplication allows for multiplication without needing to use the '\*' character. Although the '\*' character can still be used for multiplication.
- ````sin(x)cos(x)````&emsp;→&emsp;sin(x) \* cos(x)
- ````xyz````&emsp;→&emsp;x \* y \* z

PEMDAS is used for the order of operations. Parentheses are needed to ensure the expression is read correctly.
- ````e^2x````&emsp;→&emsp;x * e<sup>2</sup>
- ````e^(2x)````&emsp;→&emsp;e<sup>2 * x</sup>

Whitespaces are ignored for calculations. This includes all spaces, tabs, and newlines.
- ````sin(x)  cos(x)````&emsp;→&emsp;sin(x) \* cos(x)
- ````x  +  y  z````&emsp;→&emsp;x + y \* z

Exponents can be expressed using either the '^' symbol or '**' operator.
- ````sin(x)^2````&emsp;→&emsp;sin(x)<sup>2</sup>
- ````xy**3````&emsp;→&emsp;x * y<sup>3</sup>

Comparisons are performed by using the '==' operator.
- ````sin(x)cos(x) == cos(x)sin(x)````&emsp;→&emsp;True
- ````2x + y == y````&emsp;→&emsp;False

# How to Build

Python 3.11+ is required.

### Clone the repo:
````
git clone https://github.com/2-adic/Calculator-App.git
````

It is suggested to use a [virtual environment](https://docs.python.org/3/library/venv.html).

### Install the required libraries:
````
pip install -r requirements.txt
````

Run main.py to start the app.



























