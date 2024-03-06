"""
Used to control the font of the window.
"""

import os
from PyQt6.QtGui import QFontDatabase


def font_load(file_name):
    file_name = 'fonts/' + file_name  # uses fonts in the font folder

    # gets the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # constructs the full path to the font file
    font_path = os.path.join(dir_path, file_name)

    # loads the font and return the family name
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"Failed to load font from {font_path}")
        return None
    return QFontDatabase.applicationFontFamilies(font_id)[0]


font_size = 10

font_files = [
    'RobotoMono-VariableFont_wght.ttf',  # Roboto Mono (l could be mistaken for a 1, might change later)
    'RobotoMono-Italic-VariableFont_wght'  # Roboto Mono italicized
]

# Within the window file, run the following code to use the font:
'''
font_family = fontcontrol.font_load(fontcontrol.font_files[0])
if font_family:
    font = QFont(font_family, fontcontrol.font_size)
    app.setFont(font)
else:
    print("Error: Font didn't load, default system font will be used instead.")
'''
