import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QLineEdit, QVBoxLayout, QPlainTextEdit, QScrollArea, QHBoxLayout, QFrame, QLayout, QSizePolicy, QRadioButton, QButtonGroup, QSpacerItem, QGridLayout
from PyQt6.QtGui import QColor, QPainter, QIcon, QFont, QPalette, QMouseEvent, QKeySequence, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize
import sympy as sy
import pyperclip
import fontcontrol
from files import file_path
from str_format import contains_substring
from PIL import Image
import system_settings
import misc_functions
from functions import Solve
import str_format
import symbols


class Settings:
    def __init__(self):
        self.__load_defaults()

    def __load_defaults(self):
        """
        Converts / initializes all settings to their default values.
        """

        # Window ------------------------------------------------------------------------------------------------

        self._window_start_size_main = (
            100,  # initial x position
            100,  # initial y position
            800,  # initial x size
            600   # initial y size
        )

        self._window_settings_scale = .8  # number that the settings window's dimensions will be scaled by
        self._window_start_size_settings = (
            int(self._window_start_size_main[2] * self._window_settings_scale),  # initial x size
            int(self._window_start_size_main[3] * self._window_settings_scale)   # initial y size
        )

        self._widget_resize_size = 5  # thickness of the resizing widgets
        self._window_size_min_main = 650, 450  # min size of the main window
        self._window_size_min_settings = int(self._window_size_min_main[0] * self._window_settings_scale), int(self._window_size_min_main[1] * self._window_settings_scale)  # min size of the settings window

        # title bar
        self._title_bar_height = 22  # height of the title bar
        self._title_bar_button_width = int(1.5 * self._title_bar_height)  # width of the title bar buttons
        self._title_bar_settings_icon_scale = .8  # the size of the icon relative to the button size
        self._title_bar_settings_spacing = int(self._title_bar_height / 11)  # spacing between the button and the top / bottom of the title bar
        self._title_bar_settings_width = self._title_bar_height - (2 * self._title_bar_settings_spacing)  # width of the settings button
        self._title_bar_settings_separate = 20  # spacing between the settings button, and the other buttons

        self._window_title_main = 'Calculator'
        self._window_title_settings = 'Settings'
        self._window_title_position = (
            int(5 + (self._title_bar_height / 2) - (22 / 2)),  # x position
            int(3 + (self._title_bar_height / 2) - (22 / 2))  # y position
        )

        # Testing Buttons ---------------------------------------------------------------------------------------

        self._test_padding = 2  # starts after this one
        self._test_between_spacing = 10
        self._test_horizontal_offset = 90
        self._test_button_width = 50

        # Boxes -------------------------------------------------------------------------------------------------

        # general
        self._box_width_left = 1/2  # fraction of screen width
        self._box_padding = 20  # amount of spacing between the boxes
        self._box_border = 4  # the border thickness for all widgets
        self._box_border_radius = self._box_border * 2  # the curvature of the border corners

        # text box
        self._bar_button_width = 80  # width of the bar buttons under the text box
        self._bar_button_height = 40  # height of the bar buttons under the text box

        # answer box
        self._answer_default = 'Answer'
        self._answer_format_size = 20  # the size of the symbol that shows the current selected answer format

        self._box_answer_height_scale = 2/5  # fraction of screen height
        self._box_answer_padding = 12  # distance from the image to the border of the answer box
        self._latex_image_dpi = 800

        # multi box
        self._content_margin = 10  # distance between the scroll content, and the border
        self._select_height = 50  # height of the selector buttons
        self._symbols_button_width = 50, 120  # width of the copy buttons within the symbols tab, a tuple is used for the width of different sections
        self._symbols_button_height = 50  # height of the copy buttons, all buttons have the same height

        # Colors ------------------------------------------------------------------------------------------------
        # all int values in this section can be from 0 to 255

        # background
        self._color_background = 49, 51, 56
        self._color_background_transparent_amount = 150  # the transparency value of the background: lower means more transparent
        self._color_background_blurred = True  # blurs the background if it is transparent,

        # text
        self._color_text = 255, 255, 255
        self._color_text_highlight_active = 70, 115, 156
        self._color_text_highlight_inactive = 176, 176, 176
        self._color_text_secondary = 35, 36, 41

        # title bar
        self._color_title_bar = 30, 31, 34
        self._color_title_bar_text = 148, 155, 164
        self._color_title_bar_button_hover = 45, 46, 51
        self._color_title_bat_button_exit = 242, 63, 66

        # boxes
        self._color_box_background = 85, 88, 97
        self._color_box_background_selected = 51, 75, 97
        self._color_box_border = 35, 36, 40
        self._color_box_highlight = 81, 100, 117

        # other
        self._color_line_primary = 41, 42, 47
        self._color_line_secondary = 49, 51, 56
        self._color_scrollbar_background = 63, 65, 72
        self._color_latex = self._color_text

        # -------------------------------------------------------------------------------------------------------

    def get_color_text(self):
        return self._color_text

    def get_color_text_highlight_active(self):
        return self._color_text_highlight_active

    def get_color_text_highlight_inactive(self):
        return self._color_text_highlight_inactive


class ControlWindow(QWidget, Settings):
    def __init__(self):

        QWidget.__init__(self)

        self._settings_user = Settings()  # used to keep track of any settings the user changes within the window
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
        self.__button_close.setIcon(QIcon(file_path('button_close_icon.png', 'icons')))
        self.__button_close.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user._color_title_bat_button_exit};
                border: none;
            }}
            '''
        )
        self.__button_close.clicked.connect(self.__button_logic_close)

        # maximize button
        self.__button_maximize = QPushButton('', self)
        self.__button_maximize.setIcon(QIcon(file_path('button_maximize_icon.png', 'icons')))
        self.__button_maximize.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user._color_title_bar_button_hover};
                border: none;
            }}
            '''
        )
        self.__button_maximize.clicked.connect(self.__button_logic_maximize)

        # minimize button
        self.__button_minimize = QPushButton('', self)
        self.__button_minimize.setIcon(QIcon(file_path('button_minimize_icon.png', 'icons')))
        self.__button_minimize.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user._color_title_bar_button_hover};
                border: none;
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
        self.__title_label.setStyleSheet(f'color: rgb{self._settings_user._color_title_bar_text}; font-weight: bold; font-size: 11px;')
        self.__title_label.move(self._settings_user._window_title_position[0], self._settings_user._window_title_position[1])

    def _set_geometry(self, size: tuple[int, int, int, int]):
        """
        Sets the initial size of the window.

        :param size: initial x position, initial y position, initial x size, initial y size.
        """
        self.setGeometry(*size)  # initial window size / position

    def _set_size_min(self, size: tuple[int, int]):
        self.setMinimumSize(*size)  # sets the minimum size of the window (used for macOS since the OS automatically controls the resizing)

        self.size_min = size

    def _update_control(self) -> None:
        """
        Updates the positions of all widgets in the control class.
        """

        # move widget
        self.__widget_move.move(self._settings_user._widget_resize_size, self._settings_user._widget_resize_size)
        self.__widget_move.resize(self.width() - self._settings_user._widget_resize_size - (3 * self._settings_user._title_bar_height), self._settings_user._title_bar_height - self._settings_user._widget_resize_size)

        # close button
        self.__button_close.move(self.width() - self._settings_user._title_bar_button_width, 0)
        self.__button_close.resize(self._settings_user._title_bar_button_width, self._settings_user._title_bar_height)

        # maximize button
        self.__button_maximize.move(self.width() - (2 * self._settings_user._title_bar_button_width), 0)
        self.__button_maximize.resize(self._settings_user._title_bar_button_width, self._settings_user._title_bar_height)

        # minimize button
        self.__button_minimize.move(self.width() - (3 * self._settings_user._title_bar_button_width), 0)
        self.__button_minimize.resize(self._settings_user._title_bar_button_width, self._settings_user._title_bar_height)

        # Resize Widgets, Order: right, top right, top, top left, left, bottom left, bottom, bottom right
        self.__widget_resize[0].move(self.width() - self._settings_user._widget_resize_size, self._settings_user._widget_resize_size)
        self.__widget_resize[0].resize(self._settings_user._widget_resize_size, self.height() - (2 * self._settings_user._widget_resize_size))
        self.__widget_resize[1].move(self.width() - self._settings_user._widget_resize_size, 0)
        self.__widget_resize[1].resize(self._settings_user._widget_resize_size, self._settings_user._widget_resize_size)
        self.__widget_resize[2].move(self._settings_user._widget_resize_size, 0)
        self.__widget_resize[2].resize(self.width() - (2 * self._settings_user._widget_resize_size), self._settings_user._widget_resize_size)
        self.__widget_resize[3].move(0, 0)
        self.__widget_resize[3].resize(self._settings_user._widget_resize_size, self._settings_user._widget_resize_size)
        self.__widget_resize[4].move(0, self._settings_user._widget_resize_size)
        self.__widget_resize[4].resize(self._settings_user._widget_resize_size, self.height() - (2 * self._settings_user._widget_resize_size))
        self.__widget_resize[5].move(0, self.height() - self._settings_user._widget_resize_size)
        self.__widget_resize[5].resize(self._settings_user._widget_resize_size, self._settings_user._widget_resize_size)
        self.__widget_resize[6].move(self._settings_user._widget_resize_size, self.height() - self._settings_user._widget_resize_size)
        self.__widget_resize[6].resize(self.width() - (2 * self._settings_user._widget_resize_size), self._settings_user._widget_resize_size)
        self.__widget_resize[7].move(self.width() - self._settings_user._widget_resize_size, self.height() - self._settings_user._widget_resize_size)
        self.__widget_resize[7].resize(self._settings_user._widget_resize_size, self._settings_user._widget_resize_size)

    def __window_resize_enable(self):
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

    def __logic_full_screen(self):
        """
        Fullscreens the window.
        """

        if self.isFullScreen():
            # return to state before maximized
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
        painter.fillRect(0, 0, self.width(), self._settings_user._title_bar_height, QColor(*self._settings_user._color_title_bar))

        # center window
        color_background_transparent_amount = max(1, self._settings_user._color_background_transparent_amount)  # if set to 0, the background isn't there, and lets the user click things behind the window (this is prevented by making the minimum value 1)
        painter.fillRect(0, self._settings_user._title_bar_height, self.width(), self.height() - self._settings_user._title_bar_height, QColor(*self._settings_user._color_background, color_background_transparent_amount))

    def showEvent(self, event):
        super().showEvent(event)

        if self._settings_user._color_background_blurred:
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

                offset_x = min(int(self.normalGeometry().width() * (self.__offset.x() / self.width())), self.normalGeometry().width() - (3 * self._settings_user._title_bar_button_width))
                self.__offset = QPoint(offset_x, self.__offset.y())

                self.__button_logic_maximize()

                mouse_position = event.globalPosition().toPoint() - self.__offset

            elif self.isFullScreen():

                offset_x = min(int(self.normalGeometry().width() * (self.__offset.x() / self.width())), self.normalGeometry().width() - (3 * self._settings_user._title_bar_button_width))
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
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self._set_title(self._settings_user._window_title_settings)
        self._set_geometry(position + self._settings_user._window_start_size_settings)
        self._set_size_min(self._settings_user._window_size_min_settings)

    def resizeEvent(self, event):
        self._update_control()


class MainWindow(ControlWindow):
    def __init__(self):
        super().__init__()
        self._set_title(self._settings_user._window_title_main)
        self._set_geometry(self._settings_user._window_start_size_main)
        self._set_size_min(self._settings_user._window_size_min_main)

        # settings button
        self.__button_settings = QPushButton('', self)
        self.__button_settings.clicked.connect(self.__window_settings_open)
        self.__button_settings.setIcon(QIcon(file_path('gear_icon.png', 'icons')))
        size = int(self._settings_user._title_bar_settings_icon_scale * (self._settings_user._title_bar_height - (2 * self._settings_user._title_bar_settings_spacing)))
        self.__button_settings.setIcon(QIcon(QPixmap(file_path('gear_icon.png', 'icons')).scaled(size, size)))
        self.__button_settings.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border-radius: 3px
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user._color_title_bar_button_hover};
                border: none;
                border-radius: 3px
            }}
            '''
        )

        # answer box
        self.__answer = None  # user shouldn't be able to access this string yet
        self.__answer_temp = self._settings_user._answer_default
        self.__solution = None
        self.__flip_type_toggle = False
        self._icon_aspect_ratio_inverse = None

        self._box_answer = QPushButton(self._settings_user._answer_default, self)
        self._box_answer.clicked.connect(self.__copy)
        self._box_answer.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-radius: {self._settings_user._box_border_radius}px;
                background-color: rgb{self._settings_user._color_box_background};
                color: rgb{self._settings_user._color_text};
                font-size: 15px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user._color_box_highlight};
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
                font-size: {self._settings_user._answer_format_size}px;
                color: rgb{self._settings_user._color_text}
            }}
            '''
        )

        # text box
        self._user_select = None
        self._box_text = QPlainTextEdit(self)
        self._box_text.textChanged.connect(self._text_update)
        self._box_text.setStyleSheet(
            f'''
            QPlainTextEdit {{
                border-top: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-left: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-right: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                background-color: rgb{self._settings_user._color_box_background};
                border-top-left-radius: {self._settings_user._box_border_radius}px;
                border-top-right-radius: {self._settings_user._box_border_radius}px;
                color: rgb{self._settings_user._color_text};
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self._settings_user._color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self._settings_user._color_box_border};
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
                border-bottom: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-right: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-bottom-right-radius: {self._settings_user._box_border_radius}px;
                background-color: rgb{self._settings_user._color_box_background};
            }}
            '''
        )

        self._bar_answer = QPushButton('Answer', self)  # the button that lets the user compute the answer
        self._bar_answer.clicked.connect(self._get_answer)
        self._bar_answer.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-bottom-left-radius: {self._settings_user._box_border_radius}px;
                background-color: rgb{self._settings_user._color_box_background};
                color: rgb{self._settings_user._color_text};
                font-size: 15px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user._color_box_highlight};
            }}
            '''
        )

        self._bar_format = QPushButton('Format', self)  # the button that changes the format of the answer
        self._bar_format.clicked.connect(self._flip_type)
        self.__button_format_visibility(False)
        self._bar_format.setStyleSheet(
            f'''
            QPushButton {{
                border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                border-top-right-radius: {self._settings_user._box_border_radius}px;
                background-color: rgb{self._settings_user._color_box_background};
                color: rgb{self._settings_user._color_text};
                font-size: 15px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user._color_box_highlight};
            }}
            '''
        )

        # storage
        self._symbols = ({}, {}, {})
        self._symbols_prev_keys = []

        self.__is_constant_value_used = False

        # settings Window
        self.window_settings = None

    def _get_answer(self) -> None:
        """
        Calculates the answer from the user input.

        Displays the answer in the answer box.
        """

        self.__flip_type_toggle = False  # resets the format type
        self.__button_format_visibility(True)  # shows the format button

        text = self._box_text.toPlainText()  # gets the string from the text box
        text = str_format.function_convert(text)  # ensures functions won't be messed up

        # scans the text for any variables
        temp = self.__variable_formatting(self._symbols)

        if self.__is_constant_value_used:  # hides the format button is a
            self.__button_format_visibility(False)

        for x in text:
            if x in temp:
                text = text.replace(f'{x}', f'({temp[x]})')

        text = self.__answer_formatting_before(text)  # reformats the string

        self.__solution = Solve(text, self.__generate_value_used_bool(), self._settings_user._color_latex, self._settings_user._latex_image_dpi)
        self.__solution.print()  # shows the before and after expression (for testing purposes)
        self.__answer = self.__solution.get_exact()

        self._flip_type()

    def _flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        if self.__answer == self._settings_user._answer_default:
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

        # self._box_answer.setText(self.__answer_temp)  # displays the answer

    def _update_main(self):
        self.__button_settings.move(self.width() - self._settings_user._title_bar_settings_width - self._settings_user._title_bar_settings_separate - (3 * self._settings_user._title_bar_button_width), self._settings_user._title_bar_settings_spacing)
        self.__button_settings.resize(self._settings_user._title_bar_settings_width, self._settings_user._title_bar_height - (2 * self._settings_user._title_bar_settings_spacing))

    def __window_settings_open(self):
        position = self.pos().x() + 40, self.pos().y() + 30

        self.window_settings = SettingsWindow(position)
        self.window_settings.show()

    def __answer_formatting_before(self, string: str) -> str:
        """
        Reformats the string before the answer is calculated.

        Gives the user more freedom to type expressions different ways.

        :param string: The user input.
        """

        # removes white spaces
        string = string.replace(' ', '')
        string = string.replace('\n', '')
        string = string.replace('\t', '')

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
                if num == '.':  # user error; displays 'error' in answer box
                    print('Not yet fixed, do later')

                elif num != '' and '.' in num:  # num is not blank, and is a decimal
                    # replaces the first instance of each number
                    string = string.replace(num, f'({sy.Rational(num)})', 1)

                num = ''  # resets num

        return string

    def __variable_formatting(self, symbols: tuple[dict, dict, dict]) -> dict:

        self.__is_constant_value_used = False  # resets if a constant value was used

        temp1 = {}
        # adds all keys with their text to a new dict
        for index in range(len(symbols)):
            keys = list(symbols[index].keys())
            for key in keys:

                if index == 0:
                    temp1[key] = str_format.function_convert(symbols[index][key][1].text())

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

        :param is_visible: If the buttons is going to be visible or not.
        """

        if is_visible:
            self._bar_format.show()
            self._bar_answer.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                    border-bottom-left-radius: {self._settings_user._box_border_radius}px;
                    background-color: rgb{self._settings_user._color_box_background};
                    color: rgb{self._settings_user._color_text};
                    font-size: 15px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self._settings_user._color_box_highlight};
                }}
                '''
            )

        else:
            self._bar_format.hide()
            self._bar_answer.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                    border-bottom-left-radius: {self._settings_user._box_border_radius}px;
                    border-top-right-radius: {self._settings_user._box_border_radius}px;
                    background-color: rgb{self._settings_user._color_box_background};
                    color: rgb{self._settings_user._color_text};
                    font-size: 15px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self._settings_user._color_box_highlight};
                }}
                '''
            )

    def __copy(self) -> None:
        """
        Lets the user copy the answer by clicking the answer box.
        """

        pyperclip.copy(str(self.__answer_temp))  # copies answer to clipboard

    def _text_update(self) -> None:
        """
        Activates each time a user changes their input in the text box.

        Adds and removes variables in the variables box based on the new user input.
        Removes the answer from the answer box.
        """

        self.__button_format_visibility(False)  # hides the format button

        self._user_select = self.sender()  # saves which text box the user was typing in

        text = self._box_text.toPlainText()
        text = str_format.function_convert(text)

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
                    self._symbols[0][x] = (label, text_box)

                elif index == 1:
                    label = QLabel(f'{x}:', self)

                    option1 = QRadioButton(f'{x}')
                    option2 = QRadioButton(symbols.constant_preview[x] + '...')
                    option1.setChecked(True)

                    radio_group = QButtonGroup(self)
                    radio_group.addButton(option1)
                    radio_group.addButton(option2)

                    style = f'''
                            QRadioButton::indicator {{
                                border-radius: 6px;
                                border: 2px solid rgb{self._settings_user._color_box_border};
                                background-color: rgb{self._settings_user._color_box_background};
                            }}
                            QRadioButton::indicator:checked {{
                                background-color: rgb{self._settings_user._color_box_highlight};
                            }}
                            '''
                    option1.setStyleSheet(style)
                    option2.setStyleSheet(style)

                    self._symbols[1][x] = (label, option1, option2)

        formatted = {}  # used to preserve functions
        keys = list(self._symbols[0].keys())
        for y in keys:
            formatted[y] = str_format.function_convert(self._symbols[0][y][1].text())  # lets functions be inside of variables
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
                        self._symbols[0][x] = (label, text_box)

                    elif index_2 == 1:
                        label = QLabel(f'{x}:', self)

                        option1 = QRadioButton(f'{x}')
                        option2 = QRadioButton(symbols.constant_preview[x] + '...')
                        option1.setChecked(True)

                        radio_group = QButtonGroup(self)
                        radio_group.addButton(option1)
                        radio_group.addButton(option2)

                        style = f'''
                                QRadioButton::indicator {{
                                    border-radius: 6px;
                                    border: 2px solid rgb{self._settings_user._color_box_border};
                                    background-color: rgb{self._settings_user._color_box_background};
                                }}
                                QRadioButton::indicator:checked {{
                                    background-color: rgb{self._settings_user._color_box_highlight};
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

        # clears the answer box to prevent user from thinking the answer is for what was just typed in the text box
        self.__answer = self._settings_user._answer_default  # sets answer to default answer so if the user flips the format, the default answer still displays
        self._box_answer.setIcon(QIcon())

        self._box_answer.setText(f'{self.__answer}')  # displays the answer

        self._box_answer_format_label.setText('')

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

    def _setup(self):

        # Scroll Area Setup -------------------------------------------------------------------------------------

        self.__selector_names = ['Variables', 'Notation']  # include at least 2 names (these will most likely be images in the future, for example: a simple image of a graph for the graph tab)
        self.__area_amount = len(self.__selector_names)  # amount of scroll areas, at least 2 are needed for correct formatting

        # creates the scroll areas
        self.__areas = []
        for i in range(self.__area_amount):
            area = QWidget(self)

            layout = QVBoxLayout(area)
            layout.setContentsMargins(self._settings_user._content_margin, self._settings_user._content_margin, self._settings_user._content_margin, self._settings_user._content_margin)

            area.setStyleSheet(
                f'''
                border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                background-color: rgb{self._settings_user._color_box_background};
                border-bottom-left-radius: {self._settings_user._box_border_radius}px;
                border-bottom-right-radius: {self._settings_user._box_border_radius}px;
                color: rgb{self._settings_user._color_text};
                font-size: 15px;
                '''
            )

            area.hide()
            self.__areas.append([area, layout, []])

        self.__areas[0][0].show()  # defaults to the variables tab

        # Selectors ---------------------------------------------------------------------------------------------

        self.__button_selectors = []
        for i in range(self.__area_amount):
            button = QPushButton(self.__selector_names[i], self)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(self.__button_logic_selector)
            self.__button_selector_style(button, i)  # sets the button style
            self.__button_selectors.append(button)  # adds the button to a list

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
                    color: rgb{self._settings_user._color_text_secondary};
                    font-size: 15px;
                }}
                '''
            )
            self.__areas[i][1].addStretch()
            self.__areas[i][1].addWidget(label)
            self.__areas[i][1].addStretch()

        self.__fill_symbols()  # initializes the symbols tab

        # Variable Tab ------------------------------------------------------------------------------------------

        # scroll area container alignment
        self.__areas[0][1].setAlignment(Qt.AlignmentFlag.AlignTop)

        # sections of the variable page
        self.__titles = ['Variables', 'Constants', 'Arbitrary Constants']

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
                    color: rgb{self._settings_user._color_text_secondary};
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
                label.setStyleSheet(f'font-weight: bold; font-size: 14px; color: rgb{self._settings_user._color_text}; border: none;')
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

                        edit.textChanged.connect(self._text_update)

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
                    line.setStyleSheet(f'background-color: rgb{self._settings_user._color_line_secondary}; border-radius: 1px')

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
                        border: 1px solid rgb{self._settings_user._color_line_primary};
                        background-color: rgb{self._settings_user._color_line_primary};
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
                        background-color: rgb{self._settings_user._color_box_background};
                        color: rgb{self._settings_user._color_text};
                        font-size: 15px;
                    }}
                    QScrollBar:vertical {{
                        border-radius: 4px;
                        background-color: rgb{self._settings_user._color_scrollbar_background};
                        width: 12px;
                        margin: 4px 4px 4px 0px;
                    }}
                    QScrollBar::handle:vertical {{
                        background-color: rgb{self._settings_user._color_box_border};
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

    def __fill_symbols(self):
        """
        Creates all buttons of hard to get symbols within the symbols tab.

        Allows for the user to easily copy symbols to use in calculations.
        """

        label_titles = ['Symbols', 'Functions']

        self.__grid_layout = []
        self.__button_symbols = []
        self.__previous_column_count = []

        for i in range(2):

            # adds a title for each section
            label = QLabel(label_titles[i])
            label.setStyleSheet(f'font-weight: bold; font-size: 14px; color: rgb{self._settings_user._color_text}; border: none;')
            self.__areas[1][1].addWidget(label)

            # adds a line under the title
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            line.setStyleSheet(
                f'''
                QFrame {{
                    border: 1px solid rgb{self._settings_user._color_line_primary};
                    background-color: rgb{self._settings_user._color_line_primary};
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
                    background-color: rgb{self._settings_user._color_box_background};
                    color: rgb{self._settings_user._color_text};
                    font-size: 15px;
                }}
                QScrollBar:vertical {{
                    border-radius: 4px;
                    background-color: rgb{self._settings_user._color_scrollbar_background};
                    width: 12px;
                    margin: 4px 4px 4px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: rgb{self._settings_user._color_box_border};
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
                button.clicked.connect(self.__copy_button_label)
                button.setStyleSheet(
                    f'''
                    QPushButton {{
                        border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                        border-radius: {self._settings_user._box_border_radius}px;
                    }}
                    QPushButton:pressed {{
                        background-color: rgb{self._settings_user._color_box_highlight};
                    }}
                    '''
                )

                button.setFixedHeight(self._settings_user._symbols_button_height)
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
        selector_size = (1/len(self.__button_selectors)) * (self.width() * (1 - self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)) + self._settings_user._box_border - (self._settings_user._box_border/len(self.__button_selectors))  # width of the selector buttons
        for i, button in enumerate(self.__button_selectors):

            # corrects for rounding errors which makes the borders between the buttons change size
            correction = 0
            if i != len(self.__button_selectors) - 1:
                correction = (int(((selector_size - self._settings_user._box_border) * (i - 1)) + (self._settings_user._box_padding * 2) + (self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)) + int(selector_size) - self._settings_user._box_border) - int(((selector_size - self._settings_user._box_border) * i) + (self._settings_user._box_padding * 2) + (self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5))

                if correction == 0 and (int(((selector_size - self._settings_user._box_border) * i) + (self._settings_user._box_padding * 2) + (self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)) + int(selector_size) - self._settings_user._box_border) - int(((selector_size - self._settings_user._box_border) * (i + 1)) + (self._settings_user._box_padding * 2) + (self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)) == -1:
                    correction -= 1

            # makes sure the last selector and the box below line up
            elif int(((selector_size - self._settings_user._box_border) * i) + (self._settings_user._box_padding * 2) + (self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)) + int(selector_size) != (self._settings_user._box_padding * 2) + int((self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)) + int((self.width() * (1 - self._settings_user._box_width_left)) - (self._settings_user._box_padding * 1.5)):
                correction -= 1

            # move the buttons to their correct place, while keeping the borders the same size
            button.move(int(((selector_size - self._settings_user._box_border) * i) + (self._settings_user._box_padding * 2) + (self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)), self._settings_user._box_padding + self._settings_user._title_bar_height)
            button.resize(int(selector_size) - correction, self._settings_user._select_height)

        # multi box
        for tup in self.__areas:
            tup[0].move((self._settings_user._box_padding * 2) + int((self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)), self._settings_user._box_padding + self._settings_user._title_bar_height + self._settings_user._select_height - self._settings_user._box_border)
            tup[0].resize(int((self.width() * (1 - self._settings_user._box_width_left)) - (self._settings_user._box_padding * 1.5)), self.height() - (self._settings_user._box_padding * 2) - self._settings_user._title_bar_height - self._settings_user._select_height + self._settings_user._box_border)

        # symbols tab
        for i in range(2):
            width = self.__areas[1][2][i].viewport().width()
            column_count = max(1, width // self._settings_user._symbols_button_width[i])  # takes into account the gap between the buttons

            # only rearranges if the column count changes
            if column_count != self.__previous_column_count[i]:
                self.__previous_column_count[i] = column_count

                # re-arranges the buttons
                for x, button in enumerate(self.__button_symbols[i]):
                    self.__grid_layout[i].addWidget(button, x // column_count, x % column_count)

    def __button_logic_selector(self):

        for i, scroll in enumerate(self.__areas):
            button = self.__button_selectors[i]

            if i == 1:
                QTimer.singleShot(0, self._update_multi)  # the symbols section is not initialize correctly without this

            if self.sender() == button:
                self.__button_selector_style(button, i, True)
                scroll[0].show()
            else:
                self.__button_selector_style(button, i, False)  # changes all buttons to their default color
                scroll[0].hide()

    def __button_selector_style(self, button: QPushButton, i: int, selected: bool = False):

        if selected:
            background_color = self._settings_user._color_box_background_selected
            hover_color = self._settings_user._color_box_background_selected
        else:
            background_color = self._settings_user._color_box_background
            hover_color = self._settings_user._color_box_highlight

        if i == 0:  # left selector has a curved left corner
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self._settings_user._color_text};
                    border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                    background-color: rgb{background_color};
                    border-top-left-radius: {self._settings_user._box_border_radius}px;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -5px;
                    background-color: rgb{hover_color};
                }}
                '''
            )

        elif i == self.__area_amount - 1:  # middle selectors have no curved corners
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self._settings_user._color_text};
                    border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                    background-color: rgb{background_color};
                    border-top-right-radius: {self._settings_user._box_border_radius}px;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -5px;
                    background-color: rgb{hover_color};
                }}
                '''
            )

        else:  # right selector has a curved right corner
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self._settings_user._color_text};
                    border: {self._settings_user._box_border}px solid rgb{self._settings_user._color_box_border};
                    background-color: rgb{background_color};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -5px;
                    background-color: rgb{hover_color};
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
                    self._symbols[index][key][1].textChanged.disconnect(self._text_update)
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

    def __copy_button_label(self):
        button = self.sender()
        text = button.text()

        if text not in symbols.copy_notation[0]:  # adds brackets to functions
            text += '[]'

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

    def __update(self) -> None:
        """
        Updates the positions of all widgets that need their positions updated.

        May also be used to update other stuff in the future.
        """

        box_answer_height = int(self._settings_user._box_answer_height_scale * (self.height() - self._settings_user._title_bar_height - (3 * self._settings_user._box_padding)))

        box_text_y1 = self._settings_user._box_padding + self._settings_user._title_bar_height
        box_text_height = self.height() - box_answer_height - (self._settings_user._box_padding * 3) - self._settings_user._title_bar_height - self._settings_user._bar_button_height
        box_text_x1 = self._settings_user._box_padding
        box_text_width = int((self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5))

        # text box
        self._box_text.move(box_text_x1, box_text_y1)
        self._box_text.resize(box_text_width, box_text_height)  # 1.5 is used so the gap to the right of the box isn't too big

        self._bar_answer.move(self._settings_user._box_padding, box_text_y1 + box_text_height - self._settings_user._box_border)
        self._bar_answer.resize(self._settings_user._bar_button_width, self._settings_user._bar_button_height)

        self._bar_format.move(self._settings_user._box_padding + self._settings_user._bar_button_width - self._settings_user._box_border, box_text_y1 + box_text_height - self._settings_user._box_border)
        self._bar_format.resize(self._settings_user._bar_button_width, self._settings_user._bar_button_height)

        self._bar_blank.move(self._settings_user._box_padding + self._settings_user._bar_button_width - self._settings_user._box_border, box_text_y1 + box_text_height - self._settings_user._box_border)
        self._bar_blank.resize(box_text_x1 + box_text_width - (self._settings_user._box_padding + self._settings_user._bar_button_width - self._settings_user._box_border), self._settings_user._bar_button_height)

        # answer box
        self._box_answer.move(self._settings_user._box_padding, self.height() - self._settings_user._box_padding - box_answer_height)
        self._box_answer.resize(int((self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5)), box_answer_height)

        # answer box icon
        adjust = 8
        # moves the image a bit more away from the format symbol
        icon_new_width = int((self.width() * self._settings_user._box_width_left) - (self._settings_user._box_padding * 1.5) - (self._settings_user._box_answer_padding * 4) - (adjust * 2))
        if self._icon_aspect_ratio_inverse is not None:
            if self._icon_aspect_ratio_inverse * icon_new_width < box_answer_height - (self._settings_user._box_answer_padding * 2):
                self._box_answer.setIconSize(QSize(icon_new_width, self.height() - self._settings_user._box_padding - box_answer_height - (self._settings_user._box_answer_padding * 2)))
            else:
                icon_aspect_ratio = self._icon_aspect_ratio_inverse ** -1
                icon_new_width = int(icon_aspect_ratio * box_answer_height - (self._settings_user._box_answer_padding * 2))
                self._box_answer.setIconSize(QSize(icon_new_width, box_answer_height - (self._settings_user._box_answer_padding * 2)))

        # answer format label
        self._box_answer_format_label.move(self._settings_user._box_padding + self._settings_user._box_answer_padding, self.height() - self._settings_user._box_padding - box_answer_height)


class TestButtons(RunWindow):  # buttons, and functions for testing purposes
    def __init__(self):
        super().__init__()
        self.__setup_test()

    def __setup_test(self):

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
        self.__button_hook.append(QPushButton(self._settings_user._answer_default, self))
        self.__button_hook[-1].clicked.connect(self._get_answer)

        # flip button
        self.__button_hook.append(QPushButton('Flip', self))
        self.__button_hook[-1].clicked.connect(self._flip_type)

        # test button
        self.__button_test_toggle = False
        self.__button_hook.append(QPushButton('Test', self))
        self.__button_hook[-1].clicked.connect(self.__test)

        for i, hook in enumerate(self.__button_hook):  # sets the button hook parameters
            hook.setGeometry(self._settings_user._test_horizontal_offset + (i * (self._settings_user._test_between_spacing + self._settings_user._test_button_width)), self._settings_user._test_padding, self._settings_user._test_button_width - (2 * self._settings_user._test_padding), self._settings_user._title_bar_height - (2 * self._settings_user._test_padding))
            hook.setStyleSheet(f'background-color: None; color: rgb{self._settings_user._color_title_bar_text}; border: 1px solid rgb{self._settings_user._color_title_bar_text}; border-radius: 4px;')
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

    color_text = settings.get_color_text()
    highlight_active = settings.get_color_text_highlight_active()
    highlight_inactive = settings.get_color_text_highlight_inactive()

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
