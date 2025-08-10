"""
Used to control the font of the window.
"""

from PyQt6.QtGui import QFontDatabase
import files


def font_load(file_name):

    font_path = files.file_path(file_name, '../assets/fonts')  # gets the font file path

    # loads the font and return the family name
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"Failed to load font from {font_path}")
        return None
    return QFontDatabase.applicationFontFamilies(font_id)[0]


font_size = 8

font_files = [
    'RobotoMono-VariableFont_wght.ttf',  # Roboto Mono (l could be mistaken for a 1, might change later)
    'RobotoMono-Italic-VariableFont_wght.ttf'  # Roboto Mono italicized
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
