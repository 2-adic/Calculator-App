import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton, QLabel, QWidget, QLineEdit, QVBoxLayout, QPlainTextEdit, QScrollArea, QHBoxLayout, QFrame, QSizePolicy, QRadioButton, QButtonGroup, QSpacerItem, QGridLayout
from PyQt6.QtGui import QColor, QPainter, QIcon, QFont, QPalette, QMouseEvent, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize, pyqtSignal, pyqtSlot
import pyperclip
import fontcontrol
from files import file_path
from str_format import contains_substring, function_convert
from PIL import Image
import system_settings
import misc_functions
from functions import Solve
import symbols


class Settings:
    def __init__(self):
        # Window ------------------------------------------------------------------------------------------------

        self.__window_start_size_main = (
            100,  # initial x position
            100,  # initial y position
            800,  # initial x size
            600  # initial y size
        )

        self.__window_settings_scale = .8  # number that the settings window's dimensions will be scaled by
        self.__window_start_size_settings = (
            int(self.__window_start_size_main[2] * self.__window_settings_scale),  # initial x size
            int(self.__window_start_size_main[3] * self.__window_settings_scale)  # initial y size
        )

        self.__widget_resize_size = 5  # thickness of the resizing widgets
        self.__window_size_min_main = 650, 450  # min size of the main window
        self.__window_size_min_settings = int(self.window_size_min_main[0] * self.__window_settings_scale), int(self.window_size_min_main[1] * self.__window_settings_scale)  # min size of the settings window

        # title bar
        self.__title_bar_height = 22  # height of the title bar
        self.__title_bar_button_width = int(1.5 * self.__title_bar_height)  # width of the title bar buttons
        self.__title_bar_settings_icon_scale = .8  # the size of the icon relative to the button size
        self.__title_bar_settings_spacing = int(self.__title_bar_height / 11)  # spacing between the button and the top / bottom of the title bar
        self.__title_bar_settings_width = self.__title_bar_height - (2 * self.__title_bar_settings_spacing)  # width of the settings button
        self.__title_bar_settings_separate = 20  # spacing between the settings button, and the other buttons

        self.__window_title_main = 'Calculator'
        self.__window_title_settings = 'Settings'
        self.__window_title_position = (
            int(5 + (self.__title_bar_height / 2) - (22 / 2)),  # x position
            int(3 + (self.__title_bar_height / 2) - (22 / 2))  # y position
        )

        # Testing Buttons ---------------------------------------------------------------------------------------

        self.__test_padding = 2  # starts after this one
        self.__test_between_spacing = 10
        self.__test_horizontal_offset = 90
        self.__test_button_width = 50

        # Boxes -------------------------------------------------------------------------------------------------

        # general
        self.__box_width_left = 1/2  # fraction of screen width
        self.__box_padding = 20  # amount of spacing between the boxes
        self.__box_border = 4  # the border thickness for all widgets
        self.__box_border_radius = self.__box_border * 2  # the curvature of the border corners

        # text box
        self.__bar_button_width = 80  # width of the bar buttons under the text box
        self.__bar_button_height = 40  # height of the bar buttons under the text box

        # answer box
        self.__answer_default = 'Answer'
        self.__answer_format_size = 20  # the size of the symbol that shows the current selected answer format

        self.__box_answer_height_scale = 2/5  # fraction of screen height
        self.__box_answer_padding = 12  # distance from the image to the border of the answer box
        self.__latex_image_dpi = 800

        # multi box
        self.__content_margin = 10  # distance between the scroll content, and the border
        self.__select_height = 50  # height of the selector buttons
        self.__symbols_button_width = 50, 120  # width of the copy buttons within the symbols tab, a tuple is used for the width of different sections
        self.__symbols_button_height = 50  # height of the copy buttons, all buttons have the same height

        # buttons
        self.__button_text_hover_raise = 5  # the height text is raised when a button is being hovered

        # Colors ------------------------------------------------------------------------------------------------
        # all int values in this section can be from 0 to 255

        # background
        self.__color_background = 49, 51, 56
        self.__color_background_transparent_amount = 150  # the transparency value of the background: lower means more transparent
        self.__color_background_blurred = True  # blurs the background if it is transparent,

        # text
        self.__color_text = 255, 255, 255
        self.__color_text_highlight_active = 70, 115, 156
        self.__color_text_highlight_inactive = 176, 176, 176
        self.__color_text_secondary = 35, 36, 41

        # title bar
        self.__color_title_bar = 30, 31, 34
        self.__color_title_bar_text = 148, 155, 164
        self.__color_title_bar_button_hover = 45, 46, 51
        self.__color_title_bar_button_press = 53, 54, 60
        self.__color_title_bar_button_exit_hover = 242, 63, 66
        self.__color_title_bar_button_exit_press = 241, 112, 122

        # boxes
        self.__color_box_background = 85, 88, 97
        self.__color_box_hover = 81, 100, 117
        self.__color_box_selected = 51, 75, 97
        self.__color_box_border = 35, 36, 40
        
        # other
        self.__color_line_primary = 41, 42, 47
        self.__color_line_secondary = 49, 51, 56
        self.__color_scrollbar_background = 63, 65, 72
        self.__color_latex = self.__color_text

        # Other -------------------------------------------------------------------------------------------------

        self.__use_degrees = False
        self.__use_commas = False

    def __load_defaults(self) -> None:
        """
        Converts all settings to their default values.
        """

        self.__init__()

    @property
    def window_start_size_main(self) -> tuple[int, int, int, int]:
        return self.__window_start_size_main

    @window_start_size_main.setter
    def window_start_size_main(self, value: tuple[int, int, int, int]) -> None:
        self.__window_start_size_main = value

    @property
    def window_settings_scale(self) -> float:
        return self.__window_settings_scale

    @window_settings_scale.setter
    def window_settings_scale(self, value: float) -> None:
        self.__window_settings_scale = value

    @property
    def window_start_size_settings(self) -> tuple[int, int]:
        return self.__window_start_size_settings

    @window_start_size_settings.setter
    def window_start_size_settings(self, value: tuple[int, int]) -> None:
        self.__window_start_size_settings = value

    @property
    def widget_resize_size(self) -> int:
        return self.__widget_resize_size

    @widget_resize_size.setter
    def widget_resize_size(self, value: int) -> None:
        self.__widget_resize_size = value

    @property
    def window_size_min_main(self) -> tuple[int, int]:
        return self.__window_size_min_main

    @window_size_min_main.setter
    def window_size_min_main(self, value: tuple[int, int]) -> None:
        self.__window_size_min_main = value

    @property
    def window_size_min_settings(self) -> tuple[int, int]:
        return self.__window_size_min_settings

    @window_size_min_settings.setter
    def window_size_min_settings(self, value: tuple[int, int]) -> None:
        self.__window_size_min_settings = value

    @property
    def title_bar_height(self) -> int:
        return self.__title_bar_height

    @title_bar_height.setter
    def title_bar_height(self, value: int) -> None:
        self.__title_bar_height = value

    @property
    def title_bar_button_width(self) -> int:
        return self.__title_bar_button_width

    @title_bar_button_width.setter
    def title_bar_button_width(self, value: int) -> None:
        self.__title_bar_button_width = value

    @property
    def title_bar_settings_icon_scale(self) -> float:
        return self.__title_bar_settings_icon_scale

    @title_bar_settings_icon_scale.setter
    def title_bar_settings_icon_scale(self, value: float) -> None:
        self.__title_bar_settings_icon_scale = value

    @property
    def title_bar_settings_spacing(self) -> int:
        return self.__title_bar_settings_spacing

    @title_bar_settings_spacing.setter
    def title_bar_settings_spacing(self, value: int) -> None:
        self.__title_bar_settings_spacing = value

    @property
    def title_bar_settings_width(self) -> int:
        return self.__title_bar_settings_width

    @title_bar_settings_width.setter
    def title_bar_settings_width(self, value: int) -> None:
        self.__title_bar_settings_width = value

    @property
    def title_bar_settings_separate(self) -> int:
        return self.__title_bar_settings_separate

    @title_bar_settings_separate.setter
    def title_bar_settings_separate(self, value: int) -> None:
        self.__title_bar_settings_separate = value

    @property
    def window_title_main(self) -> str:
        return self.__window_title_main

    @window_title_main.setter
    def window_title_main(self, value: str) -> None:
        self.__window_title_main = value

    @property
    def window_title_settings(self) -> str:
        return self.__window_title_settings

    @window_title_settings.setter
    def window_title_settings(self, value: str) -> None:
        self.__window_title_settings = value

    @property
    def window_title_position(self) -> tuple[int, int]:
        return self.__window_title_position

    @window_title_position.setter
    def window_title_position(self, value: tuple[int, int]) -> None:
        self.__window_title_position = value

    @property
    def test_padding(self) -> int:
        return self.__test_padding

    @test_padding.setter
    def test_padding(self, value: int) -> None:
        self.__test_padding = value

    @property
    def test_between_spacing(self) -> int:
        return self.__test_between_spacing

    @test_between_spacing.setter
    def test_between_spacing(self, value: int) -> None:
        self.__test_between_spacing = value

    @property
    def test_horizontal_offset(self) -> int:
        return self.__test_horizontal_offset

    @test_horizontal_offset.setter
    def test_horizontal_offset(self, value: int) -> None:
        self.__test_horizontal_offset = value

    @property
    def test_button_width(self) -> int:
        return self.__test_button_width

    @test_button_width.setter
    def test_button_width(self, value: int) -> None:
        self.__test_button_width = value

    @property
    def box_width_left(self) -> float:
        return self.__box_width_left

    @box_width_left.setter
    def box_width_left(self, value: float) -> None:
        self.__box_width_left = value

    @property
    def box_padding(self) -> int:
        return self.__box_padding

    @box_padding.setter
    def box_padding(self, value: int) -> None:
        self.__box_padding = value

    @property
    def box_border(self) -> int:
        return self.__box_border

    @box_border.setter
    def box_border(self, value: int) -> None:
        self.__box_border = value

    @property
    def box_border_radius(self) -> int:
        return self.__box_border_radius

    @box_border_radius.setter
    def box_border_radius(self, value: int) -> None:
        self.__box_border_radius = value

    @property
    def bar_button_width(self) -> int:
        return self.__bar_button_width

    @bar_button_width.setter
    def bar_button_width(self, value: int) -> None:
        self.__bar_button_width = value

    @property
    def bar_button_height(self) -> int:
        return self.__bar_button_height

    @bar_button_height.setter
    def bar_button_height(self, value: int) -> None:
        self.__bar_button_height = value

    @property
    def answer_default(self) -> str:
        return self.__answer_default

    @answer_default.setter
    def answer_default(self, value: str) -> None:
        self.__answer_default = value

    @property
    def answer_format_size(self) -> int:
        return self.__answer_format_size

    @answer_format_size.setter
    def answer_format_size(self, value: int) -> None:
        self.__answer_format_size = value

    @property
    def box_answer_height_scale(self) -> float:
        return self.__box_answer_height_scale

    @box_answer_height_scale.setter
    def box_answer_height_scale(self, value: float) -> None:
        self.__box_answer_height_scale = value

    @property
    def box_answer_padding(self) -> int:
        return self.__box_answer_padding

    @box_answer_padding.setter
    def box_answer_padding(self, value: int) -> None:
        self.__box_answer_padding = value

    @property
    def latex_image_dpi(self) -> int:
        return self.__latex_image_dpi

    @latex_image_dpi.setter
    def latex_image_dpi(self, value: int) -> None:
        self.__latex_image_dpi = value

    @property
    def content_margin(self) -> int:
        return self.__content_margin

    @content_margin.setter
    def content_margin(self, value: int) -> None:
        self.__content_margin = value

    @property
    def select_height(self) -> int:
        return self.__select_height

    @select_height.setter
    def select_height(self, value: int) -> None:
        self.__select_height = value

    @property
    def symbols_button_width(self) -> tuple[int, int]:
        return self.__symbols_button_width

    @symbols_button_width.setter
    def symbols_button_width(self, value: tuple[int, int]) -> None:
        self.__symbols_button_width = value

    @property
    def symbols_button_height(self) -> int:
        return self.__symbols_button_height

    @symbols_button_height.setter
    def symbols_button_height(self, value: int) -> None:
        self.__symbols_button_height = value

    @property
    def button_text_hover_raise(self) -> int:
        return self.__button_text_hover_raise

    @button_text_hover_raise.setter
    def button_text_hover_raise(self, value: int) -> None:
        self.__button_text_hover_raise = value

    @property
    def color_background(self) -> tuple[int, int, int]:
        return self.__color_background

    @color_background.setter
    def color_background(self, value: tuple[int, int, int]) -> None:
        self.__color_background = value

    @property
    def color_background_transparent_amount(self) -> int:
        return self.__color_background_transparent_amount

    @color_background_transparent_amount.setter
    def color_background_transparent_amount(self, value: int) -> None:
        self.__color_background_transparent_amount = value

    @property
    def color_background_blurred(self) -> bool:
        return self.__color_background_blurred

    @color_background_blurred.setter
    def color_background_blurred(self, value: bool) -> None:
        self.__color_background_blurred = value

    @property
    def color_text(self) -> tuple[int, int, int]:
        return self.__color_text

    @color_text.setter
    def color_text(self, value: tuple[int, int, int]) -> None:
        self.__color_text = value

    @property
    def color_text_highlight_active(self) -> tuple[int, int, int]:
        return self.__color_text_highlight_active

    @color_text_highlight_active.setter
    def color_text_highlight_active(self, value: tuple[int, int, int]) -> None:
        self.__color_text_highlight_active = value

    @property
    def color_text_highlight_inactive(self) -> tuple[int, int, int]:
        return self.__color_text_highlight_inactive

    @color_text_highlight_inactive.setter
    def color_text_highlight_inactive(self, value: tuple[int, int, int]) -> None:
        self.__color_text_highlight_inactive = value

    @property
    def color_text_secondary(self) -> tuple[int, int, int]:
        return self.__color_text_secondary

    @color_text_secondary.setter
    def color_text_secondary(self, value: tuple[int, int, int]) -> None:
        self.__color_text_secondary = value

    @property
    def color_title_bar(self) -> tuple[int, int, int]:
        return self.__color_title_bar

    @color_title_bar.setter
    def color_title_bar(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar = value

    @property
    def color_title_bar_text(self) -> tuple[int, int, int]:
        return self.__color_title_bar_text

    @color_title_bar_text.setter
    def color_title_bar_text(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_text = value

    @property
    def color_title_bar_button_hover(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_hover

    @color_title_bar_button_hover.setter
    def color_title_bar_button_hover(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_hover = value

    @property
    def color_title_bar_button_press(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_press

    @color_title_bar_button_press.setter
    def color_title_bar_button_press(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_press = value

    @property
    def color_title_bar_button_exit_hover(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_exit_hover

    @color_title_bar_button_exit_hover.setter
    def color_title_bar_button_exit_hover(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_exit_hover = value

    @property
    def color_title_bar_button_exit_press(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_exit_press

    @color_title_bar_button_exit_press.setter
    def color_title_bar_button_exit_press(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_exit_press = value

    @property
    def color_box_background(self) -> tuple[int, int, int]:
        return self.__color_box_background

    @color_box_background.setter
    def color_box_background(self, value: tuple[int, int, int]) -> None:
        self.__color_box_background = value

    @property
    def color_box_selected(self) -> tuple[int, int, int]:
        return self.__color_box_selected

    @color_box_selected.setter
    def color_box_selected(self, value: tuple[int, int, int]) -> None:
        self.__color_box_selected = value

    @property
    def color_box_border(self) -> tuple[int, int, int]:
        return self.__color_box_border

    @color_box_border.setter
    def color_box_border(self, value: tuple[int, int, int]) -> None:
        self.__color_box_border = value

    @property
    def color_box_hover(self) -> tuple[int, int, int]:
        return self.__color_box_hover

    @color_box_hover.setter
    def color_box_hover(self, value: tuple[int, int, int]) -> None:
        self.__color_box_hover = value

    @property
    def color_line_primary(self) -> tuple[int, int, int]:
        return self.__color_line_primary

    @color_line_primary.setter
    def color_line_primary(self, value: tuple[int, int, int]) -> None:
        self.__color_line_primary = value

    @property
    def color_line_secondary(self) -> tuple[int, int, int]:
        return self.__color_line_secondary

    @color_line_secondary.setter
    def color_line_secondary(self, value: tuple[int, int, int]) -> None:
        self.__color_line_secondary = value

    @property
    def color_scrollbar_background(self) -> tuple[int, int, int]:
        return self.__color_scrollbar_background

    @color_scrollbar_background.setter
    def color_scrollbar_background(self, value: tuple[int, int, int]) -> None:
        self.__color_scrollbar_background = value

    @property
    def color_latex(self) -> tuple[int, int, int]:
        return self.__color_latex

    @color_latex.setter
    def color_latex(self, value: tuple[int, int, int]) -> None:
        self.__color_latex = value

    @property
    def use_degrees(self) -> bool:
        return self.__use_degrees

    @use_degrees.setter
    def use_degrees(self, value: bool) -> None:
        self.__use_degrees = value

    @property
    def use_commas(self) -> bool:
        return self.__use_commas

    @use_commas.setter
    def use_commas(self, value: bool) -> None:
        self.__use_commas = value


class ControlWindow(QWidget):
    def __init__(self, settings: Settings | None = None):

        QWidget.__init__(self)

        # used to keep track of any settings the user changes within the window
        if settings is None:
            self._settings_user = Settings()
        else:  # allows for the settings class object to be shared between multiple windows
            self._settings_user = settings

        self.__op = system_settings.OperatingSystem()  # initializes settings depending on the operating system

        # Window ------------------------------------------------------------------------------------------------

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)  # removes default title bar

        # Title Bar ---------------------------------------------------------------------------------------------

        self.__window_moving = False  # initial state of the window moving
        self.__offset = None  # initial state of the window offset

        # window move widget
        self.__widget_move = QWidget(self)

        # close button
        self.__button_close = QPushButton('', self)
        self.__button_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__button_close.setIcon(QIcon(file_path('button_close_icon.png', 'icons')))
        self.__button_close.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_exit_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_exit_press};
            }}
            '''
        )
        self.__button_close.clicked.connect(self.__button_logic_close)
        self.__button_close.pressed.connect(self.__button_close_press)
        self.__button_close.released.connect(self.__button_close_release)

        # maximize button
        self.__button_maximize = QPushButton('', self)
        self.__button_maximize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__button_maximize.setIcon(QIcon(file_path('button_maximize_icon.png', 'icons')))
        self.__button_maximize.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_press};
            }}
            '''
        )
        self.__button_maximize.clicked.connect(self.__button_logic_maximize)

        # minimize button
        self.__button_minimize = QPushButton('', self)
        self.__button_minimize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__button_minimize.setIcon(QIcon(file_path('button_minimize_icon.png', 'icons')))
        self.__button_minimize.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_press};
            }}
            QPushButton::icon {{
                margin-bottom: -5px; 
            }}
            '''
        )
        self.__button_minimize.clicked.connect(self.showMinimized)

        # Resizing Widgets --------------------------------------------------------------------------------------

        self.__window_resize = True  # initial state of resizing
        self.__window_resize_direction = None  # initial direction of resizing
        self.__widget_resize_toggle = True  # toggles resizing functionality

        self.__window_resize_allowed = True  # only allows resizing once the timer is over
        self.__window_resize_timer = QTimer(self)  # timer for resizing
        self.__window_resize_timer.setSingleShot(True)  # timer triggers once before its cooldown
        self.__window_resize_timer.timeout.connect(self.__window_resize_enable)  # enables the timer after its cooldown
        self.__widget_resize = tuple(QWidget(self) for _ in range(8))

        self.__widget_resize[0].setCursor(Qt.CursorShape.SizeHorCursor)  # right
        self.__widget_resize[4].setCursor(Qt.CursorShape.SizeHorCursor)  # left

        self.__widget_resize[1].setCursor(Qt.CursorShape.SizeBDiagCursor)  # top right
        self.__widget_resize[5].setCursor(Qt.CursorShape.SizeBDiagCursor)  # bottom left

        self.__widget_resize[2].setCursor(Qt.CursorShape.SizeVerCursor)  # top
        self.__widget_resize[6].setCursor(Qt.CursorShape.SizeVerCursor)  # bottom

        self.__widget_resize[3].setCursor(Qt.CursorShape.SizeFDiagCursor)  # top left
        self.__widget_resize[7].setCursor(Qt.CursorShape.SizeFDiagCursor)  # bottom right

        # -------------------------------------------------------------------------------------------------------

        # configures transparency
        if self.__op.system_name == 'Windows':
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # -------------------------------------------------------------------------------------------------------

    def _set_title(self, title: str):
        """
        Sets the title of the window.
        """

        self.setWindowTitle(title)

        # displays title
        self.__title_label = QLabel(title, self)
        self.__title_label.setStyleSheet(
            f'''
            color: rgb{self._settings_user.color_title_bar_text};
            font-weight: bold;
            font-size: 11px;
            '''
        )
        self.__title_label.move(self._settings_user.window_title_position[0], self._settings_user.window_title_position[1])

    def _set_geometry(self, size: tuple[int, int, int, int]):
        """
        Sets the initial size of the window.

        :param size: initial x position, initial y position, initial x size, initial y size.
        """
        self.setGeometry(*size)  # initial window size / position

    def _set_size_min(self, size: tuple[int, int]):
        self.setMinimumSize(*size)  # sets the minimum size of the window (used for macOS since the OS automatically controls the resizing)

        self.size_min = size

    def _window_normal(self) -> None:
        """
        Returns the window to its normal state, and enables all resizing widgets. Takes the window out of all modes.
        """

        self.showNormal()

        for widget in self.__widget_resize:  # enables all resizing widgets
            widget.setEnabled(True)

        self.__widget_resize_toggle = True  # allows the window to be resized

    def _update_control(self) -> None:
        """
        Updates the positions of all widgets in the control class.
        """

        # move widget
        self.__widget_move.move(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_move.resize(self.width() - self._settings_user.widget_resize_size - (3 * self._settings_user.title_bar_height), self._settings_user.title_bar_height - self._settings_user.widget_resize_size)

        # close button
        self.__button_close.move(self.width() - self._settings_user.title_bar_button_width, 0)
        self.__button_close.resize(self._settings_user.title_bar_button_width, self._settings_user.title_bar_height)

        # maximize button
        self.__button_maximize.move(self.width() - (2 * self._settings_user.title_bar_button_width), 0)
        self.__button_maximize.resize(self._settings_user.title_bar_button_width, self._settings_user.title_bar_height)

        # minimize button
        self.__button_minimize.move(self.width() - (3 * self._settings_user.title_bar_button_width), 0)
        self.__button_minimize.resize(self._settings_user.title_bar_button_width, self._settings_user.title_bar_height)

        # Resize Widgets, Order: right, top right, top, top left, left, bottom left, bottom, bottom right
        self.__widget_resize[0].move(self.width() - self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[0].resize(self._settings_user.widget_resize_size, self.height() - (2 * self._settings_user.widget_resize_size))
        self.__widget_resize[1].move(self.width() - self._settings_user.widget_resize_size, 0)
        self.__widget_resize[1].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[2].move(self._settings_user.widget_resize_size, 0)
        self.__widget_resize[2].resize(self.width() - (2 * self._settings_user.widget_resize_size), self._settings_user.widget_resize_size)
        self.__widget_resize[3].move(0, 0)
        self.__widget_resize[3].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[4].move(0, self._settings_user.widget_resize_size)
        self.__widget_resize[4].resize(self._settings_user.widget_resize_size, self.height() - (2 * self._settings_user.widget_resize_size))
        self.__widget_resize[5].move(0, self.height() - self._settings_user.widget_resize_size)
        self.__widget_resize[5].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[6].move(self._settings_user.widget_resize_size, self.height() - self._settings_user.widget_resize_size)
        self.__widget_resize[6].resize(self.width() - (2 * self._settings_user.widget_resize_size), self._settings_user.widget_resize_size)
        self.__widget_resize[7].move(self.width() - self._settings_user.widget_resize_size, self.height() - self._settings_user.widget_resize_size)
        self.__widget_resize[7].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)

    def _update_colors_control(self) -> None:
        """
        Updates the colors for the ControlWindow.

        Updates the title bar button colors, and the title label color.
        """

        self.__button_close.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_exit_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_exit_press};
            }}
            '''
        )

        self.__button_maximize.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_press};
            }}
            '''
        )

        self.__button_minimize.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_press};
            }}
            QPushButton::icon {{
                margin-bottom: -5px; 
            }}
            '''
        )

        self.__title_label.setStyleSheet(
            f'''
            color: rgb{self._settings_user.color_title_bar_text};
            font-weight: bold;
            font-size: 11px;
            '''
        )

    def __button_close_press(self) -> None:
        self.__button_close.setIcon(QIcon(file_path('button_close_press_icon.png', 'icons')))

    def __button_close_release(self) -> None:
        self.__button_close.setIcon(QIcon(file_path('button_close_icon.png', 'icons')))

    def __window_resize_enable(self) -> None:
        """
        Re-enables resizing after the timer expires.
        """

        self.__window_resize_allowed = True

    def __button_logic_close(self) -> None:
        """
        Closes the window.
        """

        self.close()

    def __button_logic_maximize(self) -> None:
        """
        Maximizes the screem using the maximize button.
        """

        if self.__op.system_name == 'Darwin':  # on macOS, the maximize button fullscreens the window
            self.__logic_full_screen()
            return

        if self.isMaximized():
            # return to state before maximized
            self.showNormal()
            self.__widget_resize_toggle = True

            for widget in self.__widget_resize:  # enables all resizing widgets
                widget.setEnabled(True)

        else:
            # maximize window
            self.showMaximized()
            self.__widget_resize_toggle = False

            for widget in self.__widget_resize:  # disables all resizing widgets
                widget.setEnabled(False)

        self.resizeEvent(None)  # resizes the window

    def __logic_full_screen(self) -> None:
        """
        Fullscreens the window.
        """

        if self.isFullScreen():
            # return to state before fullscreened
            self.showNormal()
            self.__widget_resize_toggle = True

            for widget in self.__widget_resize:  # enables all resizing widgets
                widget.setEnabled(True)

        else:
            # maximize window
            self.showFullScreen()
            self.__widget_resize_toggle = False

            for widget in self.__widget_resize:  # disables all resizing widgets
                widget.setEnabled(False)

        self.resizeEvent(None)  # resizes the window

    def paintEvent(self, event) -> None:
        """
        Gives the background and titlebar their colors.
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # title bar
        painter.fillRect(0, 0, self.width(), self._settings_user.title_bar_height, QColor(*self._settings_user.color_title_bar))

        # center window
        color_background_transparent_amount = max(1, self._settings_user.color_background_transparent_amount)  # if set to 0, the background isn't there, and lets the user click things behind the window (this is prevented by making the minimum value 1)
        painter.fillRect(0, self._settings_user.title_bar_height, self.width(), self.height() - self._settings_user.title_bar_height, QColor(*self._settings_user.color_background, color_background_transparent_amount))

    def showEvent(self, event):
        super().showEvent(event)

        if self._settings_user.color_background_blurred:
            self.__op.enable_blur(self)

    def keyPressEvent(self, event) -> None:

        # maximizes the window based on the operating system's shortcut
        if self.__op.is_maximize_shortcut(event):
            self.__logic_full_screen()

            # focuses the window
            self.activateWindow()
            self.raise_()
            self.setFocus()

        else:
            super().keyPressEvent(event)  # passes other key presses

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        """
        Sets moving variables to false if the user stops hold left click.

        :param event: Detects when a mouse button is released.
        """

        if event.button() == Qt.MouseButton.LeftButton:
            self.__window_moving = False
            self.__window_resize = False

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """
        Detects if the user pressed left click to resize or move the window.

        :param event: Detects when a mouse button is pressed.
        """

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.__offset = event.position().toPoint()

            # moving Window
            self.__window_moving = False
            if self.__widget_move.rect().contains(self.__widget_move.mapFrom(self, self.__offset)):
                self.__window_moving = True
                self.__offset = event.globalPosition().toPoint() - self.pos()
                return

            # resizing Widgets
            self.__window_resize = False
            if self.__widget_resize_toggle:

                for i in range(len(self.__widget_resize)):  # checks if cursor is in any of the resizing widgets
                    if self.__widget_resize[i].rect().contains(self.__widget_resize[i].mapFrom(self, self.__offset)):
                        self.__window_resize_direction = i
                        self.__window_resize = True
                        break

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        """
        Detects when the user moves their mouse.

        Use to detect if the user trying to move or resize the window.

        :param event: Detects when the mouse is left-clicked and moves.
        """

        # Moving Window
        if self.__window_moving:

            # exits the maximized setting
            if self.isMaximized():

                offset_x = min(int(self.normalGeometry().width() * (self.__offset.x() / self.width())), self.normalGeometry().width() - (3 * self._settings_user.title_bar_button_width))
                self.__offset = QPoint(offset_x, self.__offset.y())

                self.__button_logic_maximize()

                mouse_position = event.globalPosition().toPoint() - self.__offset

            elif self.isFullScreen():

                offset_x = min(int(self.normalGeometry().width() * (self.__offset.x() / self.width())), self.normalGeometry().width() - (3 * self._settings_user.title_bar_button_width))
                self.__offset = QPoint(offset_x, self.__offset.y())

                self.__logic_full_screen()

                mouse_position = event.globalPosition().toPoint() - self.__offset

            else:
                mouse_position = event.globalPosition().toPoint() - self.__offset

            self.move(mouse_position)

        # Resizing Widgets
        elif self.__window_resize:

            # right
            if self.__window_resize_direction == 0:
                new_width = event.position().toPoint().x()
                if new_width >= self.size_min[0]:
                    self.resize(new_width, self.height())

            # bottom
            elif self.__window_resize_direction == 6:
                new_height = event.position().toPoint().y()
                if new_height >= self.size_min[1]:
                    self.resize(self.width(), new_height)

            # top right
            elif self.__window_resize_direction == 1 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                new_width = event.position().toPoint().x()
                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_width >= self.size_min[0] and new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, new_width, new_height)

                elif new_width >= self.size_min[0]:
                    # resizes the window to the new size
                    self.resize(new_width, self.height())

                elif new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # bottom left
            elif self.__window_resize_direction == 5 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x
                new_height = event.position().toPoint().y()

                if new_width >= self.size_min[0] and new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, new_height)

                elif new_width >= self.size_min[0]:
                    # resizes the window to the new size
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

                elif new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.resize(self.width(), new_height)

            # top
            elif self.__window_resize_direction == 2 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # left
            if self.__window_resize_direction == 4 and self.__window_resize_allowed:  # Check if resizing is allowed

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x

                if new_width >= self.size_min[0]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

            # top left
            elif self.__window_resize_direction == 3 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x
                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_width >= self.size_min[0] and new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y() + temp_event_y, new_width, new_height)

                elif new_width >= self.size_min[0]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

                elif new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # bottom right
            elif self.__window_resize_direction == 7:

                new_width = max(self.size_min[0], event.position().toPoint().x())
                new_height = max(self.size_min[1], event.position().toPoint().y())
                self.resize(new_width, new_height)


class SettingsWindow(ControlWindow):

    button_apply_signal = pyqtSignal()  # lets the apply button connect to the MainWindow class

    def __init__(self, settings: Settings, position: tuple[int, int]):
        super().__init__(settings)
        self._set_title(self._settings_user.window_title_settings)
        self._set_geometry(position + self._settings_user.window_start_size_settings)
        self._set_size_min(self._settings_user.window_size_min_settings)

        # Settings Menu -----------------------------------------------------------------------------------------

        settings_list = (
            ('General', (
                # function, default option number, setting label, option 1, option2, ... option n
                (self.__degree_units, 0, 'Angle Unit', 'Radians', 'Degrees'),
                (self.__formatting_commas, 0, 'Number Format', 'Standard', 'Commas'))),

            ('Colors', (
                (self.__button_clicked, 0, 'Button 0', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 1', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 2', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 3', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 4', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 5', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 6', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 7', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 8', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 9', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 10', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 11', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 12', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 13', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 14', 'On', 'Off'),
                (self.__button_clicked, 0, 'Button 15', 'On', 'Off'))),

            ('Other', (
                (self.__button_clicked, 0, 'Button 0', 'Option 0', 'Option 1', 'Option 2'),
                (self.__button_clicked, 1, 'Button 1', 'Option 0', 'Option 1', 'Option 2'),
                (self.__button_clicked, 1, 'Button 2', 'Option 0', 'Option 1', 'Option 2'),
                (self.__button_clicked, 2, 'Button 3', 'Option 0', 'Option 1', 'Option 2')))
        )

        self.__menu = QWidget(self)
        self.__menu.setStyleSheet(
            f'''
            QWidget {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                background-color: rgb{self._settings_user.color_box_background};
                border-radius: {self._settings_user.box_border_radius}px;
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QPushButton {{ 
                width: 100px;
                max-width: 100px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
            }}
            QPushButton:checked {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self._settings_user.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self._settings_user.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )

        main_layout = QVBoxLayout(self.__menu)
        button_layout = QHBoxLayout()  # layout for the section buttons
        self.__button_storage = []  # keeps track of buttons for future stylesheet changes

        # section button spacers
        top_spacer = QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        right_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        button_layout.addItem(left_spacer)  # adds spacing to the left of the top section buttons

        top_button_group = QButtonGroup(self)
        stacked_widget = QStackedWidget()
        stacked_widget.setStyleSheet(
            f'''
            * {{
                border: none;
            }}
            '''
        )

        for i, section in enumerate(settings_list):
            button = QPushButton(section[0])  # creates the section buttons
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setCheckable(True)  # allows the buttons to be toggleable
            button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

            if i == 0:  # the first section is selected by default
                button.setChecked(True)

            button_layout.addWidget(button)
            top_button_group.addButton(button)  # adds the button to a group so only one is active at a time

            container = self.__sections_initialize(section[1])  # gets the container for all the settings in a specific section
            stacked_widget.addWidget(container)
            button.clicked.connect(lambda checked, widget=container: stacked_widget.setCurrentWidget(widget))  # allows the section buttons to change the container

        button_layout.addItem(right_spacer)  # adds spacing to the right of the top section buttons

        # adds the apply button
        self.__button_apply = QPushButton('Apply')  # keeps track of button for future stylesheet changes
        self.__button_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__button_apply.setStyleSheet(
            f'''
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            '''
        )
        self.__button_apply.clicked.connect(self.__apply_settings)
        layout = QHBoxLayout()
        layout.addWidget(self.__button_apply)

        # main_layout
        main_layout.addItem(top_spacer)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(stacked_widget)

        main_layout.addLayout(layout)

    def __sections_initialize(self, settings_list):
        """
        Creates the container for each section in the settings.
        """

        section_widget = QWidget()
        layout = QVBoxLayout()

        for function, default_option, setting_name, *options in settings_list:
            h_layout = QHBoxLayout()
            label = QLabel(setting_name)

            h_layout.addWidget(label)
            h_layout.addStretch()

            button_group = QButtonGroup(self)  # a button group lets the user select one option per setting
            button_group.setExclusive(True)  # makes it so only one button can be selected at a time

            for i, option in enumerate(options):  # creates a button for each option
                button = QPushButton(option)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.__button_storage.append(button)
                button.setCheckable(True)
                button.setStyleSheet(
                    f'''
                    QPushButton {{
                        border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                        width: 80px;
                    }}
                    '''
                )

                button_group.addButton(button)

                # connects the buttons to their specified function
                button.clicked.connect(lambda checked, f=function, l=option: f(l) if checked else None)

                if i == default_option:  # logic for if the button is the default one
                    button.setChecked(True)  # visually shows the default button as selected
                    button.click()  # activates the button to run its logic

                h_layout.addWidget(button)

            layout.addLayout(h_layout)

        layout.addStretch()
        section_widget.setLayout(layout)

        # creates a scroll area and sets the section widget as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(section_widget)
        scroll_area.setWidgetResizable(True)

        # creates a container widget for the scroll area
        container_widget = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(scroll_area)
        container_widget.setLayout(container_layout)

        return container_widget

    def __apply_settings(self) -> None:
        """
        Refreshes the windows / rendered answer to apply the new settings.
        """

        self.button_apply_signal.emit()  # runs the _apply_settings_all function within the RunWindow class
        self.__update_colors_settings()

    def __update_colors_settings(self) -> None:
        """
        Updates the colors for the SettingWindow.
        """

        self.repaint()  # updates the colors for the title bar and background

        self._update_colors_control()  # updates the colors of stuff in the title bar

        self.__button_apply.setStyleSheet(
            f'''
            QPushButton {{ 
                max-width: 100px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected}
            }}
            '''
        )

        for button in self.__button_storage:
            button.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    width: 80px;
                }}
                '''
            )

        self.__menu.setStyleSheet(
            f'''
            QWidget {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                background-color: rgb{self._settings_user.color_box_background};
                border-radius: {self._settings_user.box_border_radius}px;
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QPushButton {{
                width: 100px; 
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
            }}
            QPushButton:checked {{
                background-color: rgb{self._settings_user.color_box_selected};
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self._settings_user.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self._settings_user.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )

    def __button_clicked(self, label: str):
        """
        Used to test if the settings buttons work.

        Will be replaced by different functions in the future
        """

        return

    def __formatting_commas(self, label: str):
        """
        Toggles the comma formatting for numbers.
        """

        if label == 'Standard':
            self._settings_user.use_commas = False
        else:
            self._settings_user.use_commas = True

    def __degree_units(self, label: str):
        """
        Changes the angle unit between degrees or radians.
        """

        if label == 'Radians':
            self._settings_user.use_degrees = False
        else:
            # self._settings_user.use_degrees = True
            print('Degrees not enabled yet.')

    def __update_setting(self) -> None:
        """
        Updates the position of everything in the settings window.
        """

        self.__menu.move(self._settings_user.box_padding, self._settings_user.title_bar_height + self._settings_user.box_padding)
        self.__menu.resize(self.width() - (2 * self._settings_user.box_padding), self.height() - self._settings_user.title_bar_height - (2 * self._settings_user.box_padding))

    def resizeEvent(self, event):
        self._update_control()
        self.__update_setting()


class MainWindow(ControlWindow):
    def __init__(self):
        super().__init__()
        self._set_title(self._settings_user.window_title_main)
        self._set_geometry(self._settings_user.window_start_size_main)
        self._set_size_min(self._settings_user.window_size_min_main)

        # settings button
        self.__button_settings = QPushButton('', self)
        self.__button_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__button_settings.clicked.connect(self.__window_settings_open)
        self.__button_settings.setIcon(QIcon(file_path('gear_icon.png', 'icons')))
        size = int(self._settings_user.title_bar_settings_icon_scale * (self._settings_user.title_bar_height - (2 * self._settings_user.title_bar_settings_spacing)))
        self.__button_settings.setIcon(QIcon(QPixmap(file_path('gear_icon.png', 'icons')).scaled(size, size)))
        self.__button_settings.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border-radius: 3px
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_press}
            }}
            '''
        )

        # answer box
        self.__answer = None  # user shouldn't be able to access this string yet
        self.__answer_temp = self._settings_user.answer_default
        self.__solution = None
        self.__flip_type_toggle = False
        self._icon_aspect_ratio_inverse = None

        self._box_answer = QPushButton(self._settings_user.answer_default, self)
        self._box_answer.setCursor(Qt.CursorShape.PointingHandCursor)
        self._box_answer.clicked.connect(self.__copy)
        self._box_answer.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            '''
        )

        self.__answer_image_path_exact = file_path('latex_exact.png')  # gets the path of the latex image
        self.__answer_image_path_approximate = file_path('latex_approximate.png')  # gets the path of the latex image

        # answer format label
        self._box_answer_format_label = QLabel('', self)
        self._box_answer_format_label.setFixedWidth(25)
        self._box_answer_format_label.setStyleSheet(
            f'''
            QLabel {{
                font-size: {self._settings_user.answer_format_size}px;
                color: rgb{self._settings_user.color_text}
            }}
            '''
        )

        # text box
        self._user_select = None
        self._box_text = QPlainTextEdit(self)
        self._box_text.textChanged.connect(self._text_update)
        self.__set_custom_context_menu(self._box_text)
        self._box_text.setStyleSheet(
            f'''
            QPlainTextEdit {{
                border-top: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-left: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-right: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                background-color: rgb{self._settings_user.color_box_background};
                border-top-left-radius: {self._settings_user.box_border_radius}px;
                border-top-right-radius: {self._settings_user.box_border_radius}px;
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self._settings_user.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self._settings_user.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )

        self._bar_blank = QWidget(self)  # adds a blank space to the right of the bar buttons
        self._bar_blank.setStyleSheet(
            f'''
            QWidget {{
                border-bottom: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-right: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-bottom-right-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
            }}
            '''
        )

        self._bar_answer = QPushButton('Answer', self)  # the button that lets the user compute the answer
        self._bar_answer.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bar_answer.clicked.connect(lambda: self._get_answer())

        self._bar_format = QPushButton('Format', self)  # the button that changes the format of the answer
        self._bar_format.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bar_format.clicked.connect(self._flip_type)
        self.__button_format_visibility(False)  # sets the style for the answer button
        self._bar_format.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-top-right-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            '''
        )

        # storage
        self._symbols = ({}, {}, {})
        self._symbols_prev_keys = []

        self.__is_constant_value_used = False

        # settings Window
        self.window_settings = None

        # other
        self._text_update_lambda = lambda: self._text_update()  # used to keep track of the function for when it gets disconnected

    def _get_answer(self, stop_format_reset: bool | None = None) -> None:
        """
        Calculates the answer from the user input.

        Displays the answer in the answer box.
        """

        if stop_format_reset is None:
            self.__flip_type_toggle = False  # resets the format type
        else:  # stops the format from flipping if the apply button was pressed
            self.__flip_type_toggle = not stop_format_reset

        self.__button_format_visibility(True)  # shows the format button

        text = self._box_text.toPlainText()  # gets the string from the text box

        try:
            self.__solution = Solve(text, self.__variable_formatting(self._symbols), self.__generate_value_used_bool(), self._settings_user.use_degrees, self._settings_user.use_commas, self._settings_user.color_latex, self._settings_user.latex_image_dpi)
            self.__solution.print()  # shows the before and after expressions (for testing purposes)
            self.__answer = self.__solution.get_exact()

            if self.__is_constant_value_used:  # hides the format button if a constant value was used
                self.__button_format_visibility(False)

            self._flip_type()

        except Exception as error:
            self.__box_answer_set(f'Error: {error}', f'Error:\n{error}')  # displays the error
            print(f'Error: {error}')

    def _flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        if self.__answer == self._settings_user.answer_default:
            return

        self._box_answer.setText('')

        # uses answer_temp to save the answer
        if self.__flip_type_toggle or self.__is_constant_value_used:
            self.__answer_temp = self.__solution.get_approximate()  # turns the answer into its decimal format
            image_path = self.__answer_image_path_approximate
            self._box_answer_format_label.setText('≈')
        else:
            self.__answer_temp = self.__answer  # returns the original answer
            image_path = self.__answer_image_path_exact
            self._box_answer_format_label.setText('=')

        self.__flip_type_toggle = not self.__flip_type_toggle  # keeps track of which format is being displayed

        # use this for an option that lets the user set the non latex image as the answer
        # self._box_answer.setText(self.__answer_temp)  # displays the answer

        self._box_answer.setIcon(QIcon(image_path))
        image = Image.open(image_path)
        self._icon_aspect_ratio_inverse = image.size[1] / image.size[0]

        self.resizeEvent(None)

    def _text_update(self, activated: bool = False) -> None:
        """
        Activates each time a user changes their input in the text box.

        Adds and removes variables in the variables box based on the new user input.
        Removes the answer from the answer box.
        """

        if activated:  # if the _text_update was activated automatically, then sender is set the text box
            self._user_select = self._box_text
        else:
            self._user_select = self.sender()  # saves which text box the user was typing in

        text = self._box_text.toPlainText()
        text = function_convert(text)

        temp = set()  # used later for deleting variables in self._symbols which are not in the text box

        self._symbols_prev_keys = sorted(self._symbols[0].keys())

        # adds all variables from the text box to a dictionary
        for x in text:
            # checks if the character is in one of the accepted lists
            if x in symbols.accepted_variables:
                index = 0
                temp.add(x)
            elif x in symbols.accepted_constants:
                index = 1
                temp.add(x)
            else:
                continue

            # adds the character's label and line edit to the correct dictionary in symbols
            if x not in self._symbols[index]:
                if index == 0:
                    label = QLabel(f'{x} =', self)

                    text_box = QLineEdit(self)
                    text_box.setPlaceholderText(f'{x}')
                    self.__set_custom_context_menu(text_box)
                    self._symbols[0][x] = (label, text_box)

                elif index == 1:
                    label = QLabel(f'{x}:', self)

                    option1 = QRadioButton(f'{x}')
                    option1.setCursor(Qt.CursorShape.PointingHandCursor)
                    option2 = QRadioButton(symbols.constant_preview[x] + '...')
                    option2.setCursor(Qt.CursorShape.PointingHandCursor)
                    option1.setChecked(True)

                    # displays the default answer if a radio button was selected
                    option1.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)  # used to see if a new value was selected
                    option2.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)

                    radio_group = QButtonGroup(self)
                    radio_group.addButton(option1)
                    radio_group.addButton(option2)

                    style = f'''
                            QRadioButton::indicator {{
                                border-radius: 6px;
                                border: 2px solid rgb{self._settings_user.color_box_border};
                                background-color: rgb{self._settings_user.color_box_background};
                            }}
                            QRadioButton::indicator:hover {{
                                background-color: rgb{self._settings_user.color_box_hover};
                            }}
                            QRadioButton::indicator:checked {{
                                background-color: rgb{self._settings_user.color_box_selected};
                            }}
                            '''
                    option1.setStyleSheet(style)
                    option2.setStyleSheet(style)

                    self._symbols[1][x] = (label, option1, option2)

        formatted = {}  # used to preserve functions
        keys = list(self._symbols[0].keys())
        for y in keys:
            formatted[y] = function_convert(self._symbols[0][y][1].text())  # lets functions be inside of variables
            for x in formatted[y]:
                # checks if the character is in one of the accepted lists
                if x in symbols.accepted_variables:
                    index_2 = 0
                    temp.add(x)
                elif x in symbols.accepted_constants:
                    index_2 = 1
                    temp.add(x)
                else:
                    continue

                # adds the character's label and line edit to the correct dictionary in symbols
                if x not in self._symbols[index_2].keys():

                    if index_2 == 0:
                        label = QLabel(f'{x} =', self)

                        text_box = QLineEdit(self)
                        text_box.setPlaceholderText(f'{x}')
                        self.__set_custom_context_menu(text_box)
                        self._symbols[0][x] = (label, text_box)

                    elif index_2 == 1:
                        label = QLabel(f'{x}:', self)

                        option1 = QRadioButton(f'{x}')
                        option1.setCursor(Qt.CursorShape.PointingHandCursor)
                        option2 = QRadioButton(symbols.constant_preview[x] + '...')
                        option2.setCursor(Qt.CursorShape.PointingHandCursor)
                        option1.setChecked(True)

                        # displays the default answer if a radio button was selected
                        option1.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)  # used to see if a new value was selected
                        option2.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)

                        radio_group = QButtonGroup(self)
                        radio_group.addButton(option1)
                        radio_group.addButton(option2)

                        style = f'''
                                QRadioButton::indicator {{
                                    border-radius: 6px;
                                    border: 2px solid rgb{self._settings_user.color_box_border};
                                    background-color: rgb{self._settings_user.color_box_background};
                                }}
                                QRadioButton::indicator:hover {{
                                    background-color: rgb{self._settings_user.color_box_hover};
                                }}
                                QRadioButton::indicator:checked {{
                                    background-color: rgb{self._settings_user.color_box_selected};
                                }}
                                '''
                        option1.setStyleSheet(style)
                        option2.setStyleSheet(style)

                        self._symbols[1][x] = (label, option1, option2)

        # deletes all variables not in the text box
        for index in range(len(self._symbols)):
            keys_to_delete = [x for x in self._symbols[index] if x not in temp]
            for x in keys_to_delete:
                del self._symbols[index][x]

        self._fill_variables()  # adds all variables found in the variable box

        if not activated:
            self.__box_answer_set(self._settings_user.answer_default)  # clears the previous answer

    def _update_main(self) -> None:
        self.__button_settings.move(self.width() - self._settings_user.title_bar_settings_width - self._settings_user.title_bar_settings_separate - (3 * self._settings_user.title_bar_button_width), self._settings_user.title_bar_settings_spacing)
        self.__button_settings.resize(self._settings_user.title_bar_settings_width, self._settings_user.title_bar_height - (2 * self._settings_user.title_bar_settings_spacing))

    def __box_answer_set(self, text: str, displayed_text: str = None) -> None:
        """
        Sets the answer button to the display the given text.

        Used for displaying errors and the default answer.
        """

        if displayed_text is None:
            displayed_text = text

        self._box_answer.setIcon(QIcon())  # removes the image
        self._box_answer_format_label.setText('')  # removes the format icon
        self._box_answer.setText(displayed_text)  # sets the text of the button

        self.__button_format_visibility(False)  # removes the format button

        self.__answer = text
        self.__answer_temp = text

    def __set_custom_context_menu(self, widget):
        """
        Sets the context menu stylesheet.
        """

        def context_menu_event(event):
            menu = widget.createStandardContextMenu()
            menu.setStyleSheet(
                f'''
                QMenu {{
                    background-color: rgb{self._settings_user.color_box_background};
                    border: 1px solid rgb{self._settings_user.color_box_border};
                    border-radius: 0px;
                    color: white;
                    font-size: 13px;
                }}
                QMenu::item::selected {{
                    background-color: rgb{self._settings_user.color_box_hover};
                }}
                '''
            )
            menu.exec(event.globalPos())

        widget.contextMenuEvent = context_menu_event

    def __window_settings_open(self) -> None:
        position = self.pos().x() + 40, self.pos().y() + 30

        if self.window_settings is None:  # creates and opens the setting window
            self.window_settings = SettingsWindow(self._settings_user, position)
            self.window_settings.button_apply_signal.connect(self._apply_settings_all)  # lets the apply button connect to the MainWindow class
            self.window_settings.show()

        else:  # the settings window already exists, it is showed and repositioned
            self.window_settings.show()  # shows the window if the user closed it
            new_position = position + self._settings_user.window_start_size_settings
            self.window_settings.setGeometry(*new_position)

            self.window_settings._window_normal()  # takes the window out of its special states
            self.window_settings.raise_()  # focuses the window to the front

    def _apply_settings_main(self) -> None:
        """
        Applies user settings from SettingsWindow to MainWindow.
        """

        is_displaying_answer = self._box_answer.text() == ''  # tells if an answer is being displayed or not

        misc_functions.test_colors(self._settings_user)  # changes all colors to random values for testing
        self.__update_colors_main(is_displaying_answer)  # updates all colors for MainWindow

        if is_displaying_answer:
            self._get_answer(self.__flip_type_toggle)

    def __update_colors_main(self, is_displaying_answer) -> None:
        """
        Updates the stylesheets of everything in MainWindow.

        Currently, this function is not fully implemented. Some widgets / buttons need to be automatically updated.
        """

        self.repaint()  # updates the colors for the title bar and background
        self._text_update(True)  # updates the colors in the variables tab

        self._update_colors_control()  # updates the colors of stuff in the title bar
        self.__button_format_visibility(is_displaying_answer)  # updates the color for the answer button

        self.__button_settings.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border-radius: 3px
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_title_bar_button_press}
            }}
            '''
        )

        self._box_answer.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            '''
        )

        self._box_answer_format_label.setStyleSheet(
            f'''
            QLabel {{
                font-size: {self._settings_user.answer_format_size}px;
                color: rgb{self._settings_user.color_text}
            }}
            '''
        )

        self._box_text.setStyleSheet(
            f'''
            QPlainTextEdit {{
                border-top: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-left: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-right: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                background-color: rgb{self._settings_user.color_box_background};
                border-top-left-radius: {self._settings_user.box_border_radius}px;
                border-top-right-radius: {self._settings_user.box_border_radius}px;
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self._settings_user.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self._settings_user.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )

        self._bar_blank.setStyleSheet(
            f'''
            QWidget {{
                border-bottom: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-right: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-bottom-right-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
            }}
            '''
        )

        self._bar_format.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-top-right-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            '''
        )

    def __variable_formatting(self, symbols: tuple[dict, dict, dict]) -> dict:

        self.__is_constant_value_used = False  # resets if a constant value was used

        temp1 = {}
        # adds all keys with their text to a new dict
        for index in range(len(symbols)):
            keys = list(symbols[index].keys())
            for key in keys:

                if index == 0:
                    temp1[key] = function_convert(symbols[index][key][1].text())

                    if temp1[key] == '':  # if the user did not define a variable, then it is equal to itself
                        temp1[key] = key

                elif index == 1:
                    if symbols[index][key][2].isChecked():
                        self.__is_constant_value_used = True  # keeps track if a constant value was used

        # performs chained variable substitution: a=b and b=5 -> a=5
        for x in temp1:

            if temp1[x] == x or not contains_substring(temp1[x], list(self._symbols[0].keys()) + list(self._symbols[1].keys())):
                continue

            temp2 = temp1.copy()
            for y in temp2:
                for z in temp2:

                    if temp2[z] == z or not contains_substring(temp2[z], list(self._symbols[0].keys()) + list(self._symbols[1].keys())):
                        continue

                    temp1[z] = temp1[z].replace(y, f'({temp2[y]})')

        # detects if a variable is circularly defined
        for x in temp1:
            if x in temp1[x] and f'({x})' != temp1[x] and x != temp1[x]:
                print('Error: A variable is circularly defined.')
                # add logic here to return an answer of 'Error'

                break

        return temp1

    def __generate_value_used_bool(self) -> dict[str, bool]:
        """
        Returns a dictionary of True or False values depending on if the constant's value was used
        """

        constant_symbol_used = {}
        for key in list(self._symbols[1].keys()):
            if self._symbols[1][key][1].isChecked():  # checks if a constant value was used
                constant_symbol_used[key] = True
            else:
                constant_symbol_used[key] = False

        return constant_symbol_used

    def __button_format_visibility(self, is_visible: bool) -> None:
        """
        Hides or shows the format button. Allows for correct visuals.

        :param is_visible: If the format button is going to be visible or not.
        """

        if is_visible:
            self._bar_format.show()
            self._bar_answer.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    border-bottom-left-radius: {self._settings_user.box_border_radius}px;
                    background-color: rgb{self._settings_user.color_box_background};
                    color: rgb{self._settings_user.color_text};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    background-color: rgb{self._settings_user.color_box_hover};
                    padding-top: -{self._settings_user.button_text_hover_raise}px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self._settings_user.color_box_selected};
                }}
                '''
            )

        else:
            self._bar_format.hide()
            self._bar_answer.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    border-bottom-left-radius: {self._settings_user.box_border_radius}px;
                    border-top-right-radius: {self._settings_user.box_border_radius}px;
                    background-color: rgb{self._settings_user.color_box_background};
                    color: rgb{self._settings_user.color_text};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    background-color: rgb{self._settings_user.color_box_hover};
                    padding-top: -{self._settings_user.button_text_hover_raise}px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self._settings_user.color_box_selected};
                }}
                '''
            )

    def __copy(self) -> None:
        """
        Lets the user copy the answer by clicking the answer box.
        """

        string = str(self.__answer_temp).replace('*', '')  # removes all multiplication symbols
        pyperclip.copy(string)  # copies answer to clipboard

    def closeEvent(self, event):
        """
        Closes all windows if the main window is closed.
        """

        if self.window_settings is not None:
            self.window_settings.close()
        event.accept()


class MultiBox(MainWindow):
    def __init__(self):
        super().__init__()
        self._setup()

    def _setup(self) -> None:

        # Scroll Area Setup -------------------------------------------------------------------------------------

        self.__selector_names = ['Variables', 'Notation']  # include at least 2 names (these will most likely be images in the future, for example: a simple image of a graph for the graph tab)
        self.__area_amount = len(self.__selector_names)  # amount of scroll areas, at least 2 are needed for correct formatting

        # creates the scroll areas
        self.__areas = []
        for i in range(self.__area_amount):
            area = QWidget(self)

            layout = QVBoxLayout(area)
            layout.setContentsMargins(self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin)

            area.setStyleSheet(
                f'''
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                background-color: rgb{self._settings_user.color_box_background};
                border-bottom-left-radius: {self._settings_user.box_border_radius}px;
                border-bottom-right-radius: {self._settings_user.box_border_radius}px;
                color: rgb{self._settings_user.color_text};
                font-size: 15px;
                '''
            )

            area.hide()
            self.__areas.append([area, layout, []])

        self.__areas[0][0].show()  # defaults to the variables tab

        # Selectors ---------------------------------------------------------------------------------------------

        self.__button_selected = 0  # the default selected button is the variables tab

        self.__button_selectors = []
        group = QButtonGroup(self)  # adds a button group to keep track of which selector is selected
        for i in range(self.__area_amount):
            button = QPushButton(self.__selector_names[i], self)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(self.__button_selector_logic)

            button.setCheckable(True)  # allows the button to be selected instead of only pressed
            group.addButton(button)
            if i == 0:  # selects the first selector by default
                button.setChecked(True)

            self.__button_selector_style(button, i)  # sets the button style
            self.__button_selectors.append(button)  # adds the button to a list

        self.__areas[0][0].show()  # shows the default tab

        # All Tabs ----------------------------------------------------------------------------------------------

        # sets a default label for each page
        for i, title in enumerate(self.__selector_names):

            if i == 1:  # skips the symbols tab since it is never empty
                continue

            label = QLabel(title)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                f'''
                * {{
                    border: none;
                    color: rgb{self._settings_user.color_text_secondary};
                    font-size: 15px;
                }}
                '''
            )
            self.__areas[i][1].addStretch()
            self.__areas[i][1].addWidget(label)
            self.__areas[i][1].addStretch()

        self.__fill_notation()  # initializes the symbols tab

        # Variable Tab ------------------------------------------------------------------------------------------

        # scroll area container alignment
        self.__areas[0][1].setAlignment(Qt.AlignmentFlag.AlignTop)

        # sections of the variable page
        self.__titles = ['Variables', 'Constants', 'Arbitrary Constants']

    def _apply_settings_multi(self) -> None:
        self.__update_colors_multi()

    def __update_colors_multi(self) -> None:

        # updates colors for the widgets in all the tabs
        for i, areas in enumerate(self.__areas):
            area = areas[0]

            area.setStyleSheet(
                f'''
                QWidget {{
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    background-color: rgb{self._settings_user.color_box_background};
                    border-bottom-left-radius: {self._settings_user.box_border_radius}px;
                    border-bottom-right-radius: {self._settings_user.box_border_radius}px;
                    color: rgb{self._settings_user.color_text};
                    font-size: 15px;
                }}
                '''
            )

        # updates colors for the scroll areas in the notation tab
        for scroll_area in self.__areas[1][2]:
            scroll_area.setStyleSheet(
                f'''
                * {{
                    border: none;
                }}
                QScrollArea {{
                    background-color: rgb{self._settings_user.color_box_background};
                    color: rgb{self._settings_user.color_text};
                    font-size: 15px;
                }}
                QScrollBar:vertical {{
                    border-radius: 4px;
                    background-color: rgb{self._settings_user.color_scrollbar_background};
                    width: 12px;
                    margin: 4px 4px 4px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: rgb{self._settings_user.color_box_border};
                    border-radius: 4px;
                    min-height: 20px;
                }}
                QScrollBar::add-line:vertical {{
                    width: 0px;
                }}
                QScrollBar::sub-line:vertical {{
                    width: 0px;
                }}
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                    background: none;
                }}
                '''
            )

        # updates the label colors in the notation tab
        for label in self.__save_label:
            label.setStyleSheet(
                f'''
                QLabel {{
                    font-weight: bold;
                    font-size: 14px;
                    color: rgb{self._settings_user.color_text};
                    border: none;
                }}
                '''
            )

        # updates the line colors in the notation tab
        for line in self.__save_line:
            line.setStyleSheet(
                f'''
                QFrame {{
                    border: 1px solid rgb{self._settings_user.color_line_primary};
                    background-color: rgb{self._settings_user.color_line_primary};
                    border-radius: 1px
                }}
                '''
            )

        # updates the button colors in the notation tab
        for button in self.__save_button:
            button.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    border-radius: {self._settings_user.box_border_radius}px;
                }}
                QPushButton:hover {{
                    background-color: rgb{self._settings_user.color_box_hover};
                    padding-top: -{self._settings_user.button_text_hover_raise}px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self._settings_user.color_box_selected};
                }}
                '''
            )

        # updates the colors for the constant's radio buttons
        for i, section in enumerate(self._symbols):
            if i == 1:
                for key in list(section.keys()):
                    element = section[key]

                    for j, button in enumerate(element):
                        if j > 0:
                            button.setStyleSheet(
                                f'''
                                QRadioButton::indicator {{
                                    border-radius: 6px;
                                    border: 2px solid rgb{self._settings_user.color_box_border};
                                    background-color: rgb{self._settings_user.color_box_background};
                                }}
                                QRadioButton::indicator:hover {{
                                    background-color: rgb{self._settings_user.color_box_hover};
                                }}
                                QRadioButton::indicator:checked {{
                                    background-color: rgb{self._settings_user.color_box_selected};
                                }}
                                '''
                            )

        # updates the color for the selector buttons
        for i, button in enumerate(self.__button_selectors):
            self.__button_selector_style(button, i)

    def _fill_variables(self) -> None:
        """
        Displays widgets to the variable tab.

        Adds: labels and text boxes for each variable, lines to separate each variable, and a stretch to push all widgets to the top.
        """

        if self._user_select != self._box_text:
            scroll_area = self._user_select.parent().parent().parent()

            scroll_bar = scroll_area.verticalScrollBar()
            previous_scroll_amount = scroll_bar.value()

        self.__clear_variables()  # deletes everything in the variable page

        count = 0
        self.__areas[0][2] = []
        for index in range(len(self._symbols)):
            self.__areas[0][2].append(QScrollArea())  # initializes the scroll areas
            count += len(self._symbols[index].keys())

        if count == 0:  # if there are no variables, the default text is generated
            label = QLabel('Variables')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                f'''
                * {{
                    border: none;
                    color: rgb{self._settings_user.color_text_secondary};
                    font-size: 15px;
                }}
                '''
            )
            self.__areas[0][1].addStretch()
            self.__areas[0][1].addWidget(label)
            self.__areas[0][1].addStretch()

        else:  # if there are no variables, this does not run
            for i, title in enumerate(self.__titles):
                if i == 2:  # arbitrary constants are not implemented yet
                    continue

                if len(self._symbols[i]) == 0:  # skips individual sections if they are empty
                    continue

                if i > 0:  # adds spacing before each label
                    self.__areas[0][1].addSpacing(5)

                # label for each scroll area
                label = QLabel(title)
                label.setStyleSheet(f'font-weight: bold; font-size: 14px; color: rgb{self._settings_user.color_text}; border: none;')
                self.__areas[0][1].addWidget(label)

                # scroll area setup
                self.__areas[0][2][i].setWidgetResizable(True)
                self.__areas[0][2][i].setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                self.__areas[0][2][i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum))

                # inside the scroll areas
                content_widget = QWidget()
                layout = QVBoxLayout()
                content_widget.setLayout(layout)
                layout.setAlignment(Qt.AlignmentFlag.AlignTop)

                for key in sorted(self._symbols[i].keys()):
                    h_layout = None
                    if i == 0:
                        label, edit = self._symbols[0][key]

                        # Use QHBoxLayout for each pair of label and line edit
                        h_layout = QHBoxLayout()
                        h_layout.addWidget(label)
                        h_layout.addWidget(edit, 1)  # The 1 here allows the QLineEdit to expand

                        edit.textChanged.connect(self._text_update_lambda)

                    if i == 1:
                        label, option1, option2 = self._symbols[1][key]

                        h_layout = QHBoxLayout()
                        h_layout.addWidget(label)

                        h_layout.addWidget(option1)
                        if key != 'i':  # 'i' doesn't need a second selector option
                            h_layout.addWidget(option2)
                        h_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

                    layout.addLayout(h_layout)

                    line = QFrame()
                    line.setFrameShape(QFrame.Shape.HLine)
                    line.setFrameShadow(QFrame.Shadow.Sunken)
                    line.setStyleSheet(f'background-color: rgb{self._settings_user.color_line_secondary}; border-radius: 1px')

                    layout.addWidget(line)

                    # Set minimum height based on number of labels and their heights
                    content_widget.setMinimumHeight(len(self._symbols[i]) * (30 + 4))  # 30 is for the line and label, 4 is for the margin

                # inner content widget
                self.__areas[0][2][i].setWidget(content_widget)

                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet(
                    f'''
                    QFrame {{
                        border: 1px solid rgb{self._settings_user.color_line_primary};
                        background-color: rgb{self._settings_user.color_line_primary};
                        border-radius: 1px
                    }}
                    '''
                )
                self.__areas[0][1].addWidget(line)

                self.__areas[0][2][i].setStyleSheet(
                    f'''
                    * {{
                        border: none;
                    }}
                    QScrollArea {{
                        background-color: rgb{self._settings_user.color_box_background};
                        color: rgb{self._settings_user.color_text};
                        font-size: 15px;
                    }}
                    QScrollBar:vertical {{
                        border-radius: 4px;
                        background-color: rgb{self._settings_user.color_scrollbar_background};
                        width: 12px;
                        margin: 4px 4px 4px 0px;
                    }}
                    QScrollBar::handle:vertical {{
                        background-color: rgb{self._settings_user.color_box_border};
                        border-radius: 4px;
                        min-height: 20px;
                    }}
                    QScrollBar::add-line:vertical {{
                        width: 0px;
                    }}
                    QScrollBar::sub-line:vertical {{
                        width: 0px;
                    }}
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                        background: none;
                    }}
                    '''
                )

                self.__areas[0][1].addWidget(self.__areas[0][2][i])

        # focuses the user to the current textbox they are typing in
        if self._user_select != self._box_text:

            scroll_area = self._user_select.parent().parent().parent()

            # finds the amount of variables inserted before the selected line edit
            key = misc_functions.get_line_edit_key(self._symbols[0], self._user_select)
            symbols_prev_keys = self._symbols_prev_keys
            symbols_curr_keys = sorted(self._symbols[0].keys())
            amount_inserted_before = misc_functions.get_position_change(symbols_prev_keys, symbols_curr_keys, key)

            QTimer.singleShot(0, lambda: self.__set_scrollbar(scroll_area.verticalScrollBar(), previous_scroll_amount, amount_inserted_before))  # QTimer is used due to the max_scroll not being correctly calculated

            self._user_select.setFocus()

    def __fill_notation(self) -> None:
        """
        Creates all buttons of hard to get symbols within the symbols tab.

        Allows for the user to easily copy symbols to use in calculations.
        """

        label_titles = ['Symbols', 'Functions']

        self.__grid_layout = []
        self.__button_symbols = []
        self.__previous_column_count = []

        # saves specific elements for changing the stylesheets
        self.__save_line = []
        self.__save_label = []
        self.__save_button = []

        for i in range(2):

            # adds a title for each section
            label = QLabel(label_titles[i])
            self.__save_label.append(label)  # saves for future stylesheet changes
            label.setStyleSheet(f'font-weight: bold; font-size: 14px; color: rgb{self._settings_user.color_text}; border: none;')
            self.__areas[1][1].addWidget(label)

            # adds a line under the title
            line = QFrame()
            self.__save_line.append(line)  # saves for future stylesheet changes
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            line.setStyleSheet(
                f'''
                QFrame {{
                    border: 1px solid rgb{self._settings_user.color_line_primary};
                    background-color: rgb{self._settings_user.color_line_primary};
                    border-radius: 1px
                }}
                '''
            )
            self.__areas[1][1].addWidget(line)

            # adds a scroll area
            self.__areas[1][2].append(QScrollArea())
            self.__areas[1][2][i].setWidgetResizable(True)
            self.__areas[1][2][i].setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            self.__areas[1][2][i].setStyleSheet(
                f'''
                * {{
                    border: none;
                }}
                QScrollArea {{
                    background-color: rgb{self._settings_user.color_box_background};
                    color: rgb{self._settings_user.color_text};
                    font-size: 15px;
                }}
                QScrollBar:vertical {{
                    border-radius: 4px;
                    background-color: rgb{self._settings_user.color_scrollbar_background};
                    width: 12px;
                    margin: 4px 4px 4px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: rgb{self._settings_user.color_box_border};
                    border-radius: 4px;
                    min-height: 20px;
                }}
                QScrollBar::add-line:vertical {{
                    width: 0px;
                }}
                QScrollBar::sub-line:vertical {{
                    width: 0px;
                }}
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                    background: none;
                }}
                '''
            )

            # uses a QFrame to hold the grid layout
            grid_widget = QFrame()
            grid_widget.setFrameShape(QFrame.Shape.NoFrame)

            # uses a QGridLayout to get the desired behavior
            self.__grid_layout.append(QGridLayout())
            grid_widget.setLayout(self.__grid_layout[i])

            # creates a wrapper widget for the scroll area
            wrapper_widget = QWidget()
            wrapper_layout = QVBoxLayout(wrapper_widget)
            wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            wrapper_layout.addWidget(grid_widget)
            self.__areas[1][2][i].setWidget(wrapper_widget)

            # adds buttons to the grid layout
            self.__button_symbols.append([])
            for x, symbol in enumerate(symbols.copy_notation[i]):
                button = QPushButton(symbol)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.__save_button.append(button)  # saves for future stylesheet changes
                button.clicked.connect(self.__copy_button_label)
                button.setStyleSheet(
                    f'''
                    QPushButton {{
                        border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                        border-radius: {self._settings_user.box_border_radius}px;
                    }}
                    QPushButton:hover {{
                        background-color: rgb{self._settings_user.color_box_hover};
                        padding-top: -{self._settings_user.button_text_hover_raise}px;
                    }}
                    QPushButton:pressed {{
                        background-color: rgb{self._settings_user.color_box_selected};
                    }}
                    '''
                )

                button.setFixedHeight(self._settings_user.symbols_button_height)
                self.__button_symbols[i].append(button)
                self.__grid_layout[i].addWidget(button, x // 4, x % 4)

            self.__areas[1][1].addWidget(self.__areas[1][2][i])  # adds the scroll area to the layout

            self.__previous_column_count.append(-1)  # initializes the column count

    def _update_multi(self) -> None:
        """
        Updates the positions of all widgets in the multi class.
        """

        # selectors
        # although this works perfectly, a lot of the math in this section is not optimized
        selector_size = (1/len(self.__button_selectors)) * (self.width() * (1 - self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + self._settings_user.box_border - (self._settings_user.box_border/len(self.__button_selectors))  # width of the selector buttons
        for i, button in enumerate(self.__button_selectors):

            # corrects for rounding errors which makes the borders between the buttons change size
            correction = 0
            if i != len(self.__button_selectors) - 1:
                correction = (int(((selector_size - self._settings_user.box_border) * (i - 1)) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int(selector_size) - self._settings_user.box_border) - int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5))

                if correction == 0 and (int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int(selector_size) - self._settings_user.box_border) - int(((selector_size - self._settings_user.box_border) * (i + 1)) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) == -1:
                    correction -= 1

            # makes sure the last selector and the box below line up
            elif int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int(selector_size) != (self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)):
                correction -= 1

            # move the buttons to their correct place, while keeping the borders the same size
            button.move(int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height)
            button.resize(int(selector_size) - correction, self._settings_user.select_height)

        # multi box
        for tup in self.__areas:
            tup[0].move((self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height + self._settings_user.select_height - self._settings_user.box_border)
            tup[0].resize(int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)), self.height() - (self._settings_user.box_padding * 2) - self._settings_user.title_bar_height - self._settings_user.select_height + self._settings_user.box_border)

        # symbols tab
        if self.__button_selected == 1:
            for i in range(2):
                width = self.__areas[1][2][i].viewport().width()
                column_count = max(1, width // self._settings_user.symbols_button_width[i])  # takes into account the gap between the buttons

                # only rearranges if the column count changes
                if column_count != self.__previous_column_count[i]:
                    self.__previous_column_count[i] = column_count

                    # re-arranges the buttons
                    for x, button in enumerate(self.__button_symbols[i]):
                        self.__grid_layout[i].addWidget(button, x // column_count, x % column_count)

    def __button_selector_logic(self) -> None:
        """
        Applies styles to the selector buttons and keeps track of which button was selected.
        """

        for i, scroll in enumerate(self.__areas):
            button = self.__button_selectors[i]

            if i == 1:
                QTimer.singleShot(0, self._update_multi)  # the symbols section is not initialized correctly without this

            if self.sender() == button:
                scroll[0].show()
                self.__button_selected = i

            else:
                scroll[0].hide()

    def __button_selector_style(self, button: QPushButton, i: int):
        if i == 0:  # left selector has a curved left corner
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self._settings_user.color_text};
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    background-color: rgb{self._settings_user.color_box_background};
                    border-top-left-radius: {self._settings_user.box_border_radius}px;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -{self._settings_user.button_text_hover_raise}px;
                    background-color: rgb{self._settings_user.color_box_hover};
                }}
                QPushButton:checked {{
                    background-color: rgb{self._settings_user.color_box_selected};
                }}
                '''
            )

        elif i == self.__area_amount - 1:  # middle selectors have no curved corners
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self._settings_user.color_text};
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    background-color: rgb{self._settings_user.color_box_background};
                    border-top-right-radius: {self._settings_user.box_border_radius}px;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -{self._settings_user.button_text_hover_raise}px;
                    background-color: rgb{self._settings_user.color_box_hover};
                }}
                QPushButton:checked {{
                    background-color: rgb{self._settings_user.color_box_selected};
                }}
                '''
            )

        else:  # right selector has a curved right corner
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self._settings_user.color_text};
                    border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                    background-color: rgb{self._settings_user.color_box_background};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -{self._settings_user.button_text_hover_raise}px;
                    background-color: rgb{self._settings_user.color_box_hover};
                }}
                QPushButton:checked {{
                    background-color: rgb{self._settings_user.color_box_selected};
                }}
                '''
            )

    def __set_scrollbar(self, scroll_bar, previous_scroll_amount, new_items):
        max_value = scroll_bar.maximum()
        if max_value != 0:
            new = previous_scroll_amount + (new_items * 34)
            scroll_bar.setValue(min(max_value, new))

    def __clear_variables(self) -> None:
        """
        Removes all widgets from the variable tab, disconnecting signals and clearing nested layouts.
        """

        # disconnects all LineEdits from their function
        for index in range(len(self._symbols)):
            keys = list(self._symbols[index].keys())
            for key in keys:
                try:
                    self._symbols[index][key][1].textChanged.disconnect(self._text_update_lambda)
                except:
                    pass

        # deletes all elements in the layout
        layout = self.__areas[0][1]
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self.__clear_inner_layout(item.layout())
                item.layout().deleteLater()

    def __clear_inner_layout(self, layout):
        """
        Recursively removes all items from a given nested layout.
        """

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.__clear_inner_layout(item.layout())
                item.layout().deleteLater()

    def __copy_button_label(self) -> None:
        button = self.sender()
        text = button.text()

        if text not in symbols.copy_notation[0]:  # adds parentheses to functions
            text += '()'

        pyperclip.copy(text)


class RunWindow(MultiBox, MainWindow):
    def __init__(self):  # initialize all children here
        MainWindow.__init__(self)
        MultiBox._setup(self)

    def resizeEvent(self, event):
        self.__update()
        self._update_main()
        self._update_control()
        self._update_multi()

    @pyqtSlot()
    def _apply_settings_all(self) -> None:
        """
        Applies changed settings to all classes.
        """

        self._apply_settings_main()
        self._apply_settings_multi()

    def __update(self) -> None:
        """
        Updates the positions of all widgets that need their positions updated.

        May also be used to update other stuff in the future.
        """

        box_answer_height = int(self._settings_user.box_answer_height_scale * (self.height() - self._settings_user.title_bar_height - (3 * self._settings_user.box_padding)))

        box_text_y1 = self._settings_user.box_padding + self._settings_user.title_bar_height
        box_text_height = self.height() - box_answer_height - (self._settings_user.box_padding * 3) - self._settings_user.title_bar_height - self._settings_user.bar_button_height
        box_text_x1 = self._settings_user.box_padding
        box_text_width = int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5))

        # text box
        self._box_text.move(box_text_x1, box_text_y1)
        self._box_text.resize(box_text_width, box_text_height)  # 1.5 is used so the gap to the right of the box isn't too big

        self._bar_answer.move(self._settings_user.box_padding, box_text_y1 + box_text_height - self._settings_user.box_border)
        self._bar_answer.resize(self._settings_user.bar_button_width, self._settings_user.bar_button_height)

        self._bar_format.move(self._settings_user.box_padding + self._settings_user.bar_button_width - self._settings_user.box_border, box_text_y1 + box_text_height - self._settings_user.box_border)
        self._bar_format.resize(self._settings_user.bar_button_width, self._settings_user.bar_button_height)

        self._bar_blank.move(self._settings_user.box_padding + self._settings_user.bar_button_width - self._settings_user.box_border, box_text_y1 + box_text_height - self._settings_user.box_border)
        self._bar_blank.resize(box_text_x1 + box_text_width - (self._settings_user.box_padding + self._settings_user.bar_button_width - self._settings_user.box_border), self._settings_user.bar_button_height)

        # answer box
        self._box_answer.move(self._settings_user.box_padding, self.height() - self._settings_user.box_padding - box_answer_height)
        self._box_answer.resize(int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), box_answer_height)

        # answer box icon
        adjust = 8
        # moves the image a bit more away from the format symbol
        icon_new_width = int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5) - (self._settings_user.box_answer_padding * 4) - (adjust * 2))
        if self._icon_aspect_ratio_inverse is not None:
            if self._icon_aspect_ratio_inverse * icon_new_width < box_answer_height - (self._settings_user.box_answer_padding * 2):
                self._box_answer.setIconSize(QSize(icon_new_width, self.height() - self._settings_user.box_padding - box_answer_height - (self._settings_user.box_answer_padding * 2)))
            else:
                icon_aspect_ratio = self._icon_aspect_ratio_inverse ** -1
                icon_new_width = int(icon_aspect_ratio * box_answer_height - (self._settings_user.box_answer_padding * 2))
                self._box_answer.setIconSize(QSize(icon_new_width, box_answer_height - (self._settings_user.box_answer_padding * 2)))

        # answer format label
        self._box_answer_format_label.move(self._settings_user.box_padding + self._settings_user.box_answer_padding, self.height() - self._settings_user.box_padding - box_answer_height)


class TestButtons(RunWindow):  # buttons, and functions for testing purposes
    def __init__(self):
        super().__init__()
        self.__setup_test()

    def __setup_test(self) -> None:

        self.__button_hook = []  # holds all testing buttons

        '''
        # size button
        self.__button_hook.append(QPushButton('Size', self))
        self.__button_hook[-1].clicked.connect(self.__get_info)
        '''

        # update button
        self.__button_hook.append(QPushButton('Update', self))
        self.__button_hook[-1].clicked.connect(self.__get_update)

        # answer button
        self.__button_hook.append(QPushButton(self._settings_user.answer_default, self))
        self.__button_hook[-1].clicked.connect(lambda: self._get_answer())

        # flip button
        self.__button_hook.append(QPushButton('Flip', self))
        self.__button_hook[-1].clicked.connect(self._flip_type)

        # test button
        self.__button_test_toggle = False
        self.__button_hook.append(QPushButton('Test', self))
        self.__button_hook[-1].clicked.connect(self.__test)

        for i, hook in enumerate(self.__button_hook):  # sets the button hook parameters
            hook.setGeometry(self._settings_user.test_horizontal_offset + (i * (self._settings_user.test_between_spacing + self._settings_user.test_button_width)), self._settings_user.test_padding, self._settings_user.test_button_width - (2 * self._settings_user.test_padding), self._settings_user.title_bar_height - (2 * self._settings_user.test_padding))
            hook.setStyleSheet(f'background-color: None; color: rgb{self._settings_user.color_title_bar_text}; border: 1px solid rgb{self._settings_user.color_title_bar_text}; border-radius: 4px;')
            hook.setCursor(Qt.CursorShape.PointingHandCursor)

    def __test(self) -> None:
        """
        Used for testing anything in the window.
        """

        self.__button_test_toggle = not self.__button_test_toggle

        '''
        if self.__button_test_toggle:
            self.scroll_area.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.scroll_area.setCursor(Qt.CursorShape.ArrowCursor)
        '''

        print(self._symbols)

    def __get_info(self) -> None:
        """
        Prints the current width and height of the window with the use of a button.
        """

        print(f'Width: {self.width()}, Height: {self.height()}')

    def __get_update(self) -> None:
        """
        For manually updating the window with a button.
        """

        self.resizeEvent(None)
        print('Manually Updated')


def main():

    app = QApplication(sys.argv)

    # sets the icon for the app
    app.setWindowIcon(QIcon(file_path('taskbar_icon_16px.png', 'icons')))

    # sets the default font
    font_family = fontcontrol.font_load(fontcontrol.font_files[0])
    if font_family:
        font = QFont(font_family, fontcontrol.font_size)
        app.setFont(font)
    else:
        print("Error: Font didn't load, default system font will be used instead.")

    # default settings
    settings = Settings()

    # could not change inactive highlight color with style sheet a style sheet; a style sheet overrides the inactive highlight color
    palette = app.palette()

    color_text = settings.color_text
    highlight_active = settings.color_text_highlight_active
    highlight_inactive = settings.color_text_highlight_inactive

    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor(*color_text))  # inactive highlight text color
    palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor(*highlight_active))  # active highlight color
    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor(*highlight_inactive))  # inactive highlight color
    app.setPalette(palette)

    # starts the window
    window = RunWindow()  # set the window equal to RunWindow() to run without the test buttons, set it to TestButtons() to run it with them
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
