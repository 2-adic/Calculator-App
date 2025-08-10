from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication
import files


def font_set(app: QApplication, font: str, font_size: int):
    """
    Sets the font for the application.
    """

    font_family = font_load(font)
    
    if not font_family:
        raise Exception(f"Font was not found: \"{font}\"")
    
    font = QFont(font_family, font_size)
    app.setFont(font)


def font_load(file_name: str):

    font_path = files.file_path(file_name, "../assets/fonts")  # gets the font file path

    # loads the font and return the family name
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"Failed to load font from {font_path}")
        return None
    return QFontDatabase.applicationFontFamilies(font_id)[0]


font_default = "RobotoMono/RobotoMono-VariableFont_wght.ttf"
font_size_default = 8

fonts = [
    "RobotoMono/RobotoMono-VariableFont_wght.ttf",  # Roboto Mono (l could be mistaken for a 1, might change later)
    "RobotoMono/RobotoMono-Italic-VariableFont_wght.ttf"  # Roboto Mono italicized
]
