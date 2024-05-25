import matplotlib.pyplot as plt
import sympy as sy
import str_format
from functions import constant_counter
from PIL import Image
from files import file_path


def render_latex(latex_str, filename, dpi=300, text_color=(1, 1, 1)):
    """Renders a LaTex string into an image without clipping issues."""

    text_color = text_color[0] / 255, text_color[1] / 255, text_color[2] / 255

    # create a figure
    fig = plt.figure()

    # dynamically adjust the figsize based on text content
    text = fig.text(0, 0, f'${latex_str}$', fontsize=12, color=text_color)
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)

    # convert pixel bbox to inches
    bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())

    # add padding to avoid clipping
    padding = .1  # used to ensure noting gets cut off
    figsize = (bbox_inches.width + padding, bbox_inches.height + padding)

    # set the new figsize based on calculated dimensions
    fig.set_size_inches(figsize)

    # remove axes and other plot elements
    plt.axis('off')

    # save the plot with tight bounding box
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=padding, transparent=True)

    # close the figure
    plt.close(fig)


def crop_image(filename):

    image_path = file_path(filename)
    with Image.open(image_path) as img:
        # Get image data
        img_data = img.getdata()

        # Find the bounding box of the non-transparent pixels
        left = img.width
        top = img.height
        right = 0
        bottom = 0

        for y in range(img.height):
            for x in range(img.width):
                pixel = img_data[y * img.width + x]
                if pixel[3] != 0:  # Check the alpha channel
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)

        # Crop the image to the bounding box
        cropped_img = img.crop((left, top, right + 1, bottom + 1))
        cropped_img.save(image_path)


def convert_render_latex(string: str, color: tuple[int, int, int], dpi: int = 300, filename: str = 'Untitled.png') -> str:
    """
    Takes a math expression as a string, and converts it into the LaTeX format.
    Also renders the image of the LaTeX string as a png named "latex_answer.png".

    :param string: String to be converted into LaTeX format
    :param color: Color of the text as a rgb value.
    :param dpi: Sets the resolution of the image.
    :param filename: The filename of the resulting image.
    :return: The formatted LaTeX string.
    """

    for x in range(constant_counter):
        string = string.replace('C' + str_format.to_subscript(str(x)), f'C_{x}')

    sy_string = sy.sympify(string)
    latex = sy.latex(sy_string, fold_short_frac=False)

    render_latex(latex, filename, text_color=color, dpi=dpi)
    crop_image(filename)

    return latex
