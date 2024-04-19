import matplotlib.pyplot as plt
import sympy as sy
import str_format
from functions import constant_counter


def render_latex(latex_str, filename='latex_answer.png', dpi=300, text_color='white'):
    """Renders a LaTeX string as an image."""

    # sets up a plot without axes or frames
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f'${latex_str}$', fontsize=12, color=text_color)  # Surround the LaTeX string with $...$ to enter math mode

    # removes all axes and white space around the LaTeX string
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # saves the figure as an image
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.015, transparent=True)
    plt.close()


def convert_render_latex(string: str, dpi=300) -> str:
    """
    Takes a math expression as a string, and converts it into the LaTeX format.
    Also renders the image of the LaTeX string as a png named "latex_answer.png".

    :param string: String to be converted into LaTeX format
    :param dpi: Sets the resolution of the image.
    :return: The formatted LaTeX string.
    """

    for x in range(constant_counter):
        string = string.replace('C' + str_format.to_subscript(str(x)), f'C_{x}')

    sy_string = sy.sympify(string)
    latex = sy.latex(sy_string, fold_short_frac=False)

    render_latex(latex, dpi=dpi)

    return latex
