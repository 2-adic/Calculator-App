import matplotlib.pyplot as plt
import sympy as sy
import str_format
from functions import constant_counter


def render_latex(latex_str, filename='latex_answer.png', dpi=300, text_color='white'):
    """Renders a LaTex string into an image without clipping issues."""

    # create a figure
    fig = plt.figure()

    # dynamically adjust the figsize based on text content
    text = fig.text(0, 0, f'${latex_str}$', fontsize=12, color=text_color)
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)

    # convert pixel bbox to inches
    bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())

    # add padding to avoid clipping
    padding = 0  # adjust as needed
    figsize = (bbox_inches.width + padding, bbox_inches.height + padding)

    # set the new figsize based on calculated dimensions
    fig.set_size_inches(figsize)

    # remove axes and other plot elements
    plt.axis('off')

    # save the plot with tight bounding box
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=padding, transparent=True)

    # close the figure
    plt.close(fig)


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
