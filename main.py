import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QLineEdit, QVBoxLayout, QPlainTextEdit, QScrollArea, QHBoxLayout, QFrame, QLayout, QSizePolicy, QRadioButton, QButtonGroup, QSpacerItem
from PyQt6.QtGui import QColor, QPainter, QIcon, QFont, QPalette, QMouseEvent, QKeySequence
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize
import sympy as sy
import pyperclip
import fontcontrol
from files import file_path
from str_format import contains_substring
from PIL import Image
import system_settings
import misc_functions
import constants
from functions import Solve
import str_format


class SettingsWindow:
    def __init__(self):

        # Window ------------------------------------------------------------------------------------------------

        self.window_title = 'Calculator'
        self.window_title_position = (
            5,  # x position
            -5  # y position
        )
        self.window_start = (
            100,  # initial x position
            100,  # initial y position
            800,  # initial x size
            600   # initial y size
        )

        self.widget_resize_size = 5
        self.title_bar_height = 22  # Height of the title bar
        self.title_bar_button_width = 1.5  # as a percentage of the title bar height
        self.window_size_min_x = 650  # minimum width of the window
        self.window_size_min_y = 450  # minimum height of the window

        # Testing Buttons ---------------------------------------------------------------------------------------

        self.test_padding = 2
        self.test_between_spacing = 10
        self.test_horizontal_offset = 90
        self.test_button_width = 50

        # Boxes -------------------------------------------------------------------------------------------------

        # General
        self.box_width_left = 1/2  # percentage of screen width
        self.box_padding = 20  # amount of spacing between the boxes
        self.box_border = 4  # the border thickness for all widgets
        self.box_border_radius = self.box_border * 2  # the curvature of the border corners

        # Answer box
        self.answer_default = 'Answer'
        self.answer_format_size = 20  # the size of the symbol that shows the current selected answer format

        self.box_answer_height_percent = 2/5  # percentage of screen height
        self.box_answer_padding = 12  # distance from the image to the border of the answer box
        self.latex_image_dpi = 800

        # Multi box
        self.content_margin = 10  # distance between the scroll content, and the border
        self.select_height = 50  # height of the selector buttons

        # Colors ------------------------------------------------------------------------------------------------
        # all int values in this section can be from 0 to 255

        # background
        self.color_background = 49, 51, 56
        self.color_background_transparent_amount = 150  # the transparency value of the background: lower means more transparent
        self.color_background_blurred = True  # blurs the background if it is transparent,

        # text
        self.color_text = 255, 255, 255
        self.color_text_highlight_active = 70, 115, 156
        self.color_text_highlight_inactive = 176, 176, 176
        self.color_text_secondary = 35, 36, 41

        # title bar
        self.color_title_bar = 30, 31, 34
        self.color_title_bar_text = 148, 155, 164
        self.color_title_bar_button_hover = 45, 46, 51
        self.color_title_bat_button_exit = 242, 63, 66

        # boxes
        self.color_box_background = 85, 88, 97
        self.color_box_border = 35, 36, 40
        self.color_box_highlight = 81, 100, 117

        # other
        self.color_line = 49, 51, 56
        self.color_scrollbar_background = 63, 65, 72
        self.color_latex = self.color_text

        # -------------------------------------------------------------------------------------------------------


class ControlWindow(QMainWindow, SettingsWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        SettingsWindow.__init__(self)

        self.op = system_settings.OperatingSystem()  # initializes settings depending on the operating system

        # Window ------------------------------------------------------------------------------------------------

        self.setGeometry(self.window_start[0], self.window_start[1], self.window_start[2], self.window_start[3])  # initial window size / position
        self.setWindowTitle(self.window_title)  # window title
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)  # removes default title bar

        self.setMinimumSize(self.window_size_min_x, self.window_size_min_y)  # need to check if this works on Windows too

        # Title Bar ---------------------------------------------------------------------------------------------

        self.window_moving = False  # initial state of the window moving
        self.offset = None  # initial state of the window offset
        self.button_width = int(self.title_bar_button_width * self.title_bar_height)

        # window move widget
        self.widget_move = QWidget(self)

        # displayed title
        self.title_label = QLabel(self.window_title, self)
        self.title_label.setStyleSheet(f'color: rgb{self.color_title_bar_text}; font-weight: bold; font-size: 11px;')
        self.title_label.move(self.window_title_position[0], self.window_title_position[1])

        # close button
        self.button_close = QPushButton('', self)
        self.button_close.setIcon(QIcon(file_path('button_close_icon.png', 'icons')))
        self.button_close.setStyleSheet(
            'QPushButton { background-color: transparent;}'
            f'QPushButton:hover {{ background-color: rgb{self.color_title_bat_button_exit}; border: none; }}'
        )
        self.button_close.clicked.connect(self.button_logic_close)

        # maximize button
        self.button_maximize = QPushButton('', self)
        self.button_maximize.setIcon(QIcon(file_path('button_maximize_icon.png', 'icons')))
        self.button_maximize.setStyleSheet(
            'QPushButton { background-color: transparent;}'
            f'QPushButton:hover {{ background-color: rgb{self.color_title_bar_button_hover}; border: none; }}'
        )
        self.button_maximize.clicked.connect(self.button_logic_maximize)

        # minimize button
        self.button_minimize = QPushButton('', self)
        self.button_minimize.setIcon(QIcon(file_path('button_minimize_icon.png', 'icons')))
        self.button_minimize.setStyleSheet(
            'QPushButton { background-color: transparent;}'
            f'QPushButton:hover {{ background-color: rgb{self.color_title_bar_button_hover}; border: none; }}'
            'QPushButton::icon { margin-bottom: -5px; }'
        )
        self.button_minimize.clicked.connect(self.showMinimized)

        # Resizing Widgets --------------------------------------------------------------------------------------

        self.window_resize = True  # initial state of resizing
        self.window_resize_direction = None  # initial direction of resizing
        self.widget_resize_toggle = True  # toggles resizing functionality

        self.window_resize_allowed = True  # only allows resizing once the timer is over
        self.window_resize_timer = QTimer(self)  # timer for resizing
        self.window_resize_timer.setSingleShot(True)  # timer triggers once before its cooldown
        self.window_resize_timer.timeout.connect(self.window_resize_enable)  # enables the timer after its cooldown
        self.widget_resize = []

        for x in range(8):  # order: right, top right, top, top left, left, bottom left, bottom, bottom right
            self.widget_resize.append(QWidget(self))

        self.widget_resize[0].setCursor(Qt.CursorShape.SizeHorCursor)  # right
        self.widget_resize[4].setCursor(Qt.CursorShape.SizeHorCursor)  # left

        self.widget_resize[1].setCursor(Qt.CursorShape.SizeBDiagCursor)  # top right
        self.widget_resize[5].setCursor(Qt.CursorShape.SizeBDiagCursor)  # bottom left

        self.widget_resize[2].setCursor(Qt.CursorShape.SizeVerCursor)  # top
        self.widget_resize[6].setCursor(Qt.CursorShape.SizeVerCursor)  # bottom

        self.widget_resize[3].setCursor(Qt.CursorShape.SizeFDiagCursor)  # top left
        self.widget_resize[7].setCursor(Qt.CursorShape.SizeFDiagCursor)  # bottom right

        # -------------------------------------------------------------------------------------------------------

        # configures transparency
        if self.op.system_name == 'Windows':
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # -------------------------------------------------------------------------------------------------------

    def paintEvent(self, event) -> None:
        """
        Gives the background and titlebar their colors.
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # title bar
        painter.fillRect(0, 0, self.width(), self.title_bar_height, QColor(self.color_title_bar[0], self.color_title_bar[1], self.color_title_bar[2]))

        # center window
        self.color_background_transparent_amount = max(1, self.color_background_transparent_amount)  # if set to 0, the background isn't there, and lets the user click things behind the window (this is prevented by making the minimum value 1)
        painter.fillRect(0, self.title_bar_height, self.width(), self.height() - self.title_bar_height, QColor(self.color_background[0], self.color_background[1], self.color_background[2], self.color_background_transparent_amount))

    def showEvent(self, event):
        super().showEvent(event)

        if self.color_background_blurred:
            self.op.enable_blur(self)

    def window_resize_enable(self):
        """
        Re-enables resizing after the timer expires.
        """

        self.window_resize_allowed = True

    def button_logic_close(self) -> None:
        """
        Checks if work was saved, then closes the window. Uses the exit button.
        """

        # logic for saving will go here

        # eventually may want to keep the program running after the window exits
        exit()  # instantly exits the program

    def button_logic_maximize(self) -> None:
        """
        Maximizes the screem using the maximize button.
        """

        if self.op.system_name == 'Darwin':  # on macOS, the maximize button fullscreens the window
            self.logic_full_screen()
            return

        if self.isMaximized():
            # return to state before maximized
            self.showNormal()
            self.widget_resize_toggle = True

            for widget in self.widget_resize:  # enables all resizing widgets
                widget.setEnabled(True)

        else:
            # maximize window
            self.showMaximized()
            self.widget_resize_toggle = False

            for widget in self.widget_resize:  # disables all resizing widgets
                widget.setEnabled(False)

        self.resizeEvent(None)  # resizes the window

    def logic_full_screen(self):
        """
        Fullscreens the window.
        """

        if self.isFullScreen():
            # return to state before maximized
            self.showNormal()
            self.widget_resize_toggle = True

            for widget in self.widget_resize:  # enables all resizing widgets
                widget.setEnabled(True)

        else:
            # maximize window
            self.showFullScreen()
            self.widget_resize_toggle = False

            for widget in self.widget_resize:  # disables all resizing widgets
                widget.setEnabled(False)

        self.resizeEvent(None)  # resizes the window

    def keyPressEvent(self, event) -> None:

        # maximizes the window based on the operating system's shortcut
        if self.op.is_maximize_shortcut(event):
            self.logic_full_screen()

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
            self.window_moving = False
            self.window_resize = False

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """
        Detects if the user pressed left click to resize or move the window.

        :param event: Detects when a mouse button is pressed.
        """

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.offset = event.position().toPoint()

            # Moving Window
            self.window_moving = False
            if self.widget_move.rect().contains(self.widget_move.mapFrom(self, self.offset)):
                self.window_moving = True
                self.offset = event.globalPosition().toPoint() - self.pos()
                return

            # Resizing Widgets
            self.window_resize = False
            if self.widget_resize_toggle:

                for i in range(len(self.widget_resize)):  # checks if cursor is in any of the resizing widgets
                    if self.widget_resize[i].rect().contains(self.widget_resize[i].mapFrom(self, self.offset)):
                        self.window_resize_direction = i
                        self.window_resize = True
                        break

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        """
        Detects when the user moves their mouse.

        Use to detect if the user trying to move or resize the window.

        :param event: Detects when the mouse is left-clicked and moves.
        """

        '''
        # fix - cursor_flash: may delete
        print('true')
        if self.user_mouse_set:
            print('double true')
            self.scroll_area.setCursor(Qt.CursorShape.ArrowCursor)
            self.user_mouse_set = False
        '''

        # Moving Window
        if self.window_moving:

            # exits the maximized setting
            if self.isMaximized():

                offset_x = min(int(self.normalGeometry().width() * (self.offset.x() / self.width())), self.normalGeometry().width() - (3 * self.button_width))
                self.offset = QPoint(offset_x, self.offset.y())

                self.button_logic_maximize()

                mouse_position = event.globalPosition().toPoint() - self.offset

            elif self.isFullScreen():

                offset_x = min(int(self.normalGeometry().width() * (self.offset.x() / self.width())), self.normalGeometry().width() - (3 * self.button_width))
                self.offset = QPoint(offset_x, self.offset.y())

                self.logic_full_screen()

                mouse_position = event.globalPosition().toPoint() - self.offset

            else:
                mouse_position = event.globalPosition().toPoint() - self.offset

            self.move(mouse_position)

        # Resizing Widgets
        elif self.window_resize:

            # right
            if self.window_resize_direction == 0:
                new_width = event.position().toPoint().x()
                if new_width >= self.window_size_min_x:
                    self.resize(new_width, self.height())

            # bottom
            elif self.window_resize_direction == 6:
                new_height = event.position().toPoint().y()
                if new_height >= self.window_size_min_y:
                    self.resize(self.width(), new_height)

            # top right
            elif self.window_resize_direction == 1 and self.window_resize_allowed:

                self.window_resize_allowed = False  # prevents further resizing until the timer expires
                self.window_resize_timer.start(1)  # starts the timer

                new_width = event.position().toPoint().x()
                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_width >= self.window_size_min_x and new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, new_width, new_height)

                elif new_width >= self.window_size_min_x:
                    # resizes the window to the new size
                    self.resize(new_width, self.height())

                elif new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # bottom left
            elif self.window_resize_direction == 5 and self.window_resize_allowed:

                self.window_resize_allowed = False  # prevents further resizing until the timer expires
                self.window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x
                new_height = event.position().toPoint().y()

                if new_width >= self.window_size_min_x and new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, new_height)

                elif new_width >= self.window_size_min_x:
                    # resizes the window to the new size
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

                elif new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.resize(self.width(), new_height)

            # top
            elif self.window_resize_direction == 2 and self.window_resize_allowed:

                self.window_resize_allowed = False  # prevents further resizing until the timer expires
                self.window_resize_timer.start(1)  # starts the timer

                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # left
            if self.window_resize_direction == 4 and self.window_resize_allowed:  # Check if resizing is allowed

                self.window_resize_allowed = False  # prevents further resizing until the timer expires
                self.window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x

                if new_width >= self.window_size_min_x:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

            # top left
            elif self.window_resize_direction == 3 and self.window_resize_allowed:

                self.window_resize_allowed = False  # prevents further resizing until the timer expires
                self.window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x
                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_width >= self.window_size_min_x and new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y() + temp_event_y, new_width, new_height)

                elif new_width >= self.window_size_min_x:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

                elif new_height >= self.window_size_min_y:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # bottom right
            elif self.window_resize_direction == 7:

                new_width = max(self.window_size_min_x, event.position().toPoint().x())
                new_height = max(self.window_size_min_y, event.position().toPoint().y())
                self.resize(new_width, new_height)


class MainWindow(ControlWindow):
    def __init__(self):
        super().__init__()

        # answer box
        self.answer = 'Error'  # user shouldn't be able to access this string yet
        self.answer_final = self.answer_default
        self.answer_temp = self.answer_final
        self.solution = None
        self.flip_type_toggle = False
        self.image = None
        self.icon_aspect_ratio_inverse = None

        self.box_answer = QPushButton(self.answer_default, self)
        self.box_answer.setStyleSheet(f'border: {self.box_border}px solid rgb{self.color_box_border}; background-color: rgb{self.color_box_background}; border-radius: {self.box_border_radius}px; color: rgb{self.color_text}; font-size: 15px;')
        self.box_answer.clicked.connect(self.copy)

        self.answer_image_path_exact = file_path('latex_exact.png')  # gets the path of the latex image
        self.answer_image_path_approximate = file_path('latex_approximate.png')  # gets the path of the latex image

        # answer format label
        self.box_answer_format_label = QLabel('', self)
        self.box_answer_format_label.setFixedWidth(25)
        self.box_answer_format_label.setStyleSheet(
            f'''
                QLabel {{
                    font-size: {self.answer_format_size}px;
                    color: rgb{self.color_text}
                }}
            '''
        )

        # text box
        self.user_select = None

        self.user_mouse_set = False

        self.symbols = ({}, {}, {})
        self.symbols_prev_keys = []
        self.accepted_variables = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        self.is_constant_value_used = False
        self.accepted_constants = constants.get_constants(constants.constants)
        self.accepted_constant_values = constants.get_constant_values(constants.constants, 20)
        self.accepted_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.accepted_other = ['(']

        self.box_text = QPlainTextEdit(self)
        self.box_text.textChanged.connect(self.text_update)
        self.box_text.setStyleSheet(
            f'''
            QPlainTextEdit {{
                border: {self.box_border}px solid rgb{self.color_box_border};
                background-color: rgb{self.color_box_background};
                border-radius: {self.box_border_radius}px;
                color: rgb{self.color_text};
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self.color_box_border};
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

    def answer_formatting_before(self, string: str) -> str:
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
            if string[x] in self.accepted_variables or string[x] in self.accepted_numbers or string[x] == ')' or string[x] == ']' or string[x] == '.':
                if string[x + 1] in self.accepted_variables or string[x + 1] == '(' or string[x + 1] == '§':
                    # inserts in front of x
                    string = string[:x + 1] + '*' + string[x + 1:]
                    x -= 1
            x += 1

        # turns all decimals into rationals
        temp = string + ' '  # character added to end of string to recognize final number
        num = ''
        for x in temp:
            if x in self.accepted_numbers or x == '.':
                num += x
            else:
                if num == '.':  # user error; displays 'error' in answer box
                    print('Not yet fixed, do later')

                elif num != '' and '.' in num:  # num is not blank, and is a decimal
                    # replaces the first instance of each number
                    string = string.replace(num, f'({sy.Rational(num)})', 1)

                num = ''  # resets num

        return string

    def variable_formatting(self, symbols: tuple[dict, dict, dict]) -> dict:

        self.is_constant_value_used = False  # resets if a constant value was used

        temp1 = {}
        # adds all keys with their text to a new dict
        for index in range(len(symbols)):
            keys = list(symbols[index].keys())
            for key in keys:

                if index == 0:
                    temp1[key] = symbols[index][key][1].text()

                    if temp1[key] == '':  # if the user did not define a variable, then it is equal to itself
                        temp1[key] = key

                elif index == 1:
                    if symbols[index][key][1].isChecked():
                        if key == 'i':  # replaces 'i' with it's recognized symbols for sympy
                            temp1[key] = 'I'
                        else:
                            temp1[key] = key

                    elif symbols[index][key][2].isChecked():
                        temp1[key] = self.accepted_constant_values[key]
                        self.is_constant_value_used = True  # keeps track if a constant value was used

        # performs chained variable substitution: a=b and b=5 -> a=5
        for x in temp1:

            if temp1[x] == x or not contains_substring(temp1[x], list(self.symbols[0].keys()) + list(self.symbols[1].keys())):
                continue

            temp2 = temp1.copy()
            for y in temp2:
                for z in temp2:

                    if temp2[z] == z or not contains_substring(temp2[z], list(self.symbols[0].keys()) + list(self.symbols[1].keys())):
                        continue

                    temp1[z] = temp1[z].replace(y, f'({temp2[y]})')

        # detects if a variable is circularly defined
        for x in temp1:
            if x in temp1[x] and f'({x})' != temp1[x] and x != temp1[x]:
                print('Error: A variable is circularly defined.')
                # add logic here to return an answer of 'Error'

                break

        return temp1

    def get_answer(self) -> None:
        """
        Calculates the answer from the user input.

        Displays the answer in the answer box.
        """

        self.flip_type_toggle = False  # resets the format type

        text = self.box_text.toPlainText()  # gets the string from the text box
        text = str_format.function_convert(text)  # ensures functions won't be messed up

        # scans the text for any variables
        temp = self.variable_formatting(self.symbols)

        for x in text:
            if x in temp:
                text = text.replace(f'{x}', f'({temp[x]})')

        text = self.answer_formatting_before(text)  # reformats the string

        self.solution = Solve(text, self.color_latex, self.latex_image_dpi)
        self.answer = self.solution.get_exact()

        self.flip_type()

    def flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        if self.answer == self.answer_default:
            return

        self.box_answer.setText('')

        # uses self.answer_temp to save the actual answer
        if self.flip_type_toggle or self.is_constant_value_used:
            self.answer_temp = self.solution.get_approximate()  # turns the answer into its decimal format
            image_path = self.answer_image_path_approximate
            self.box_answer_format_label.setText('≈')
        else:
            self.answer_temp = self.answer  # returns the original answer
            image_path = self.answer_image_path_exact
            self.box_answer_format_label.setText('=')

        self.flip_type_toggle = not self.flip_type_toggle  # keeps track of which format is being displayed

        # use this for an option that lets the user set the non latex image as the answer
        # self.box_answer.setText(self.answer_temp)  # displays the answer

        self.box_answer.setIcon(QIcon(image_path))
        self.image = Image.open(image_path)
        self.icon_aspect_ratio_inverse = self.image.size[1] / self.image.size[0]

        self.resizeEvent(None)

        # self.box_answer.setText(self.answer_temp)  # displays the answer

    def copy(self) -> None:
        """
        Lets the user copy the answer by clicking the answer box.
        """

        # adds flashing blue visual when button is clicked
        self.box_answer.setStyleSheet(f'border: {self.box_border}px solid rgb{self.color_box_border}; background-color: rgb{self.color_box_highlight}; border-radius: {self.box_border_radius}px; color: rgb{self.color_text}; font-size: 15px;')
        QTimer.singleShot(150, lambda: self.box_answer.setStyleSheet(f'border: {self.box_border}px solid rgb{self.color_box_border}; background-color: rgb{self.color_box_background}; border-radius: {self.box_border_radius}px; color: rgb{self.color_text}; font-size: 15px;'))

        pyperclip.copy(str(self.answer_temp))  # copies answer to clipboard

    def text_update(self) -> None:
        """
        Activates each time a user changes their input in the text box.

        Adds and removes variables in the variables box based on the new user input.
        Removes the answer from the answer box.
        """

        self.user_select = self.sender()  # saves which text box the user was typing in

        text = self.box_text.toPlainText()
        text = str_format.function_convert(text)

        temp = set()  # used later for deleting variables in self.symbols which are not in the text box

        self.symbols_prev_keys = sorted(self.symbols[0].keys())

        # adds all variables from the text box to a dictionary
        for x in text:
            # checks if the character is in one of the accepted lists
            if x in self.accepted_variables:
                index = 0
                temp.add(x)
            elif x in self.accepted_constants:
                index = 1
                temp.add(x)
            else:
                continue

            # adds the character's label and line edit to the correct dictionary in symbols
            if x not in self.symbols[index]:
                if index == 0:
                    label = QLabel(f'{x} =', self)

                    text_box = QLineEdit(self)
                    text_box.setPlaceholderText(f'{x}')
                    self.symbols[0][x] = (label, text_box)

                elif index == 1:
                    label = QLabel(f'{x}:', self)

                    option1 = QRadioButton(f'{x}')
                    option2 = QRadioButton(self.accepted_constant_values[x][:4] + '...')
                    option1.setChecked(True)

                    radio_group = QButtonGroup(self)
                    radio_group.addButton(option1)
                    radio_group.addButton(option2)

                    style = f'''
                            QRadioButton::indicator {{
                                border-radius: 6px;
                                border: 2px solid rgb{self.color_box_border};
                                background-color: rgb{self.color_box_background};
                            }}
                            QRadioButton::indicator:checked {{
                                background-color: rgb{self.color_box_highlight};
                            }}
                            '''
                    option1.setStyleSheet(style)
                    option2.setStyleSheet(style)

                    self.symbols[1][x] = (label, option1, option2)

        keys = list(self.symbols[0].keys())
        for y in keys:
            for x in self.symbols[0][y][1].text():
                # checks if the character is in one of the accepted lists
                if x in self.accepted_variables:
                    index_2 = 0
                    temp.add(x)
                elif x in self.accepted_constants:
                    index_2 = 1
                    temp.add(x)
                else:
                    continue

                # adds the character's label and line edit to the correct dictionary in symbols
                if x not in self.symbols[index_2].keys():

                    if index_2 == 0:
                        label = QLabel(f'{x} =', self)

                        text_box = QLineEdit(self)
                        text_box.setPlaceholderText(f'{x}')
                        self.symbols[0][x] = (label, text_box)

                    elif index_2 == 1:
                        label = QLabel(f'{x}:', self)

                        option1 = QRadioButton(f'{x}')
                        option2 = QRadioButton(self.accepted_constant_values[x][:4] + '...')
                        option1.setChecked(True)

                        radio_group = QButtonGroup(self)
                        radio_group.addButton(option1)
                        radio_group.addButton(option2)

                        style = f'''
                                QRadioButton::indicator {{
                                    border-radius: 6px;
                                    border: 2px solid rgb{self.color_box_border};
                                    background-color: rgb{self.color_box_background};
                                }}
                                QRadioButton::indicator:checked {{
                                    background-color: rgb{self.color_box_highlight};
                                }}
                                '''
                        option1.setStyleSheet(style)
                        option2.setStyleSheet(style)

                        self.symbols[1][x] = (label, option1, option2)

        # deletes all variables not in the text box
        for index in range(len(self.symbols)):
            keys_to_delete = [x for x in self.symbols[index] if x not in temp]
            for x in keys_to_delete:
                del self.symbols[index][x]

        self.area_fill()  # adds all variables found in the variable box

        # clears the answer box to prevent user from thinking the answer is for what was just typed in the text box
        self.answer = self.answer_default  # sets answer to default answer so if the user flips the format, the default answer still displays
        self.box_answer.setIcon(QIcon())

        self.box_answer.setText(f'{str(self.answer)}')  # displays the answer

        self.box_answer_format_label.setText('')


class MultiBox(MainWindow):
    def __init__(self):
        super().__init__()

        self.setup_multi()

    def setup_multi(self):

        # Scroll Area Setup -------------------------------------------------------------------------------------

        self.selector_names = ['Variables', 'Graph', 'Functions']  # include at least 2 names (these will most likely be images in the future, for example: a simple image of a graph for the graph section)
        self.area_amount = len(self.selector_names)  # amount of scroll areas, at least 2 are needed for correct formatting
        self.variables_amount_current = [0, 0, 0]  # current amount of variables
        self.variable_position_curr = None
        self.current_scroll_prev = 0
        self.current_scroll = 0

        # creates the scroll areas
        self.areas = []
        for i in range(self.area_amount):
            area = QWidget(self)

            layout = QVBoxLayout(area)
            layout.setContentsMargins(self.content_margin, self.content_margin, self.content_margin, self.content_margin)

            area.setStyleSheet(
                f'''
                border: {self.box_border}px solid rgb{self.color_box_border};
                background-color: rgb{self.color_box_background};
                border-bottom-left-radius: {self.box_border_radius}px;
                border-bottom-right-radius: {self.box_border_radius}px;
                color: rgb{self.color_text};
                font-size: 15px;
                '''
            )

            area.hide()
            self.areas.append([area, layout, []])

        self.areas[0][0].show()

        # Selectors ---------------------------------------------------------------------------------------------

        self.button_selectors = []
        for x in range(self.area_amount):
            button = QPushButton(self.selector_names[x], self)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(self.button_logic_selector)

            if x == 0:  # left selector has a curved left corner
                button.setStyleSheet(
                    f'''
                    QPushButton {{
                        color: rgb{self.color_text};
                        border: {self.box_border}px solid rgb{self.color_box_border};
                        background-color: rgb{self.color_box_background};
                        border-top-left-radius: {self.box_border_radius}px;
                        font-size: 15px;
                    }}
                    QPushButton:hover {{
                        padding-top: -5px;
                        background-color: rgb{self.color_box_highlight};
                    }}
                    '''
                )

            elif x == self.area_amount - 1:  # middle selectors have no curved corners
                button.setStyleSheet(
                    f'''
                    QPushButton {{
                        color: rgb{self.color_text};
                        border: {self.box_border}px solid rgb{self.color_box_border};
                        background-color: rgb{self.color_box_background};
                        border-top-right-radius: {self.box_border_radius}px;
                        font-size: 15px;
                    }}
                    QPushButton:hover {{
                        padding-top: -5px;
                        background-color: rgb{self.color_box_highlight};
                    }}
                    '''
                )

            else:  # right selector has a curved right corner
                button.setStyleSheet(
                    f'''
                    QPushButton {{
                        color: rgb{self.color_text};
                        border: {self.box_border}px solid rgb{self.color_box_border};
                        background-color: rgb{self.color_box_background};
                        font-size: 15px;
                    }}
                    QPushButton:hover {{
                        padding-top: -5px;
                        background-color: rgb{self.color_box_highlight};
                    }}
                    '''
                )

            self.button_selectors.append(button)

        # Variable Section --------------------------------------------------------------------------------------

        # scroll area container alignment
        self.areas[0][1].setAlignment(Qt.AlignmentFlag.AlignTop)

        # sections of the variable page
        self.titles = ['Variables', 'Constants', 'Arbitrary Constants']

        # sets a default label for each page
        for i, title in enumerate(self.selector_names):
            label = QLabel(title)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                f'''
                * {{
                    border: none;
                    color: rgb{self.color_text_secondary};
                    font-size: 15px;
                }}
                '''
            )
            self.areas[i][1].addStretch()
            self.areas[i][1].addWidget(label)
            self.areas[i][1].addStretch()

    def button_logic_selector(self):

        for i, scroll in enumerate(self.areas):

            if self.sender() == self.button_selectors[i]:
                scroll[0].show()
            else:
                scroll[0].hide()

    def area_fill(self) -> None:
        """
        Displays widgets to the variable box.

        Adds: labels and text boxes for each variable, lines to separate each variable, and a stretch to push all widgets to the top.
        """

        self.user_scroll = 0
        if self.user_select != self.box_text:
            scroll_area = self.user_select.parent().parent().parent()

            scroll_bar = scroll_area.verticalScrollBar()
            max_scroll = scroll_bar.maximum()
            self.user_scroll = scroll_bar.value()

        # gets the previous and current amount of items in each scroll area
        self.variables_amount_previous = self.variables_amount_current.copy()
        for i in range(self.area_amount):  # gets the amount of variables in each section
            self.variables_amount_current[i] = len(self.symbols[i].keys())

        self.area_clear()  # deletes everything in the variable page

        count = 0
        self.areas[0][2] = []
        for index in range(len(self.symbols)):
            self.areas[0][2].append(QScrollArea())  # initializes the scroll areas
            count += len(self.symbols[index].keys())

        if count == 0:  # if there are no variables, the default text is generated
            label = QLabel('Variables')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                f'''
                    * {{
                        border: none;
                        color: rgb{self.color_text_secondary};
                        font-size: 15px;
                    }}
                '''
            )
            self.areas[0][1].addStretch()
            self.areas[0][1].addWidget(label)
            self.areas[0][1].addStretch()

        else:  # if there are no variables, this does not run
            for i, title in enumerate(self.titles):
                if i == 2:  # arbitrary constants are not implemented yet
                    continue

                if len(self.symbols[i]) == 0:
                    continue

                if i > 0:  # adds spacing before each label
                    self.areas[0][1].addSpacing(5)

                # label for each scroll area
                label = QLabel(title)
                label.setStyleSheet(f'font-weight: bold; font-size: 14px; color: rgb{self.color_text}; border: none;')
                self.areas[0][1].addWidget(label)

                # scroll area setup
                self.areas[0][2][i].setWidgetResizable(True)
                self.areas[0][2][i].setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                self.areas[0][2][i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum))

                # inside the scroll areas
                content_widget = QWidget()
                layout = QVBoxLayout()
                content_widget.setLayout(layout)
                layout.setAlignment(Qt.AlignmentFlag.AlignTop)

                for key in sorted(self.symbols[i].keys()):
                    if i == 0:
                        label, edit = self.symbols[0][key]

                        # Use QHBoxLayout for each pair of label and line edit
                        h_layout = QHBoxLayout()
                        h_layout.addWidget(label)
                        h_layout.addWidget(edit, 1)  # The 1 here allows the QLineEdit to expand

                        edit.textChanged.connect(self.text_update)

                    if i == 1:
                        label, option1, option2 = self.symbols[1][key]

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
                    line.setStyleSheet(f'background-color: rgb{self.color_line}; border-radius: 1px')

                    layout.addWidget(line)

                    # Set minimum height based on number of labels and their heights
                    content_widget.setMinimumHeight(len(self.symbols[i]) * (30 + 4))  # 30 is for the line and label, 4 is for the margin

                # inner content widget
                self.areas[0][2][i].setWidget(content_widget)

                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("background-color: #313338; border-radius: 1px")
                self.areas[0][1].addWidget(line)

                self.areas[0][2][i].setStyleSheet(
                    f'''
                    * {{
                        border: none;
                    }}
                    QScrollArea {{
                        background-color: rgb{self.color_box_background};
                        color: rgb{self.color_text};
                        font-size: 15px;
                    }}
                    QScrollBar:vertical {{
                        border-radius: 4px;
                        background-color: rgb{self.color_scrollbar_background};
                        width: 12px;
                        margin: 4px 4px 4px 0px;
                    }}
                    QScrollBar::handle:vertical {{
                        background-color: rgb{self.color_box_border};
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

                self.areas[0][1].addWidget(self.areas[0][2][i])

        # focuses the user to the current textbox they are typing in (currently doesn't work)
        if self.user_select != self.box_text:  # may only need this for the variable scroll area, since constants will not be equal to another variable (keeping it general for now)

            scroll_area = self.user_select.parent().parent().parent()

            # finds the amount of variables inserted before the selected line edit
            key = misc_functions.get_line_edit_key(self.symbols[0], self.user_select)
            symbols_prev_keys = self.symbols_prev_keys
            symbols_curr_keys = sorted(self.symbols[0].keys())
            self.amount_inserted_before = misc_functions.get_position_change(symbols_prev_keys, symbols_curr_keys, key)

            self.scroll_bar = scroll_area.verticalScrollBar()
            QTimer.singleShot(0, self.set_scrollbar)  # QTimer is used due to the max_scroll not being correctly calculated

            self.user_select.setFocus()

    def set_scrollbar(self):
        max_value = self.scroll_bar.maximum()
        if max_value != 0:
            new = self.user_scroll + (self.amount_inserted_before * 34)
            self.scroll_bar.setValue(min(max_value, new))

    def area_clear(self) -> None:
        """
        Removes all widgets from the variable box, disconnecting signals and clearing nested layouts.
        """

        # disconnects all LineEdits from their function
        for index in range(len(self.symbols)):
            keys = list(self.symbols[index].keys())
            for key in keys:
                try:
                    self.symbols[index][key][1].textChanged.disconnect(self.text_update)
                except:
                    pass

        # deletes all elements in the layout
        layout = self.areas[0][1]
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self.clear_inner_layout(item.layout())
                item.layout().deleteLater()

    def clear_inner_layout(self, layout):
        """
        Recursively removes all items from a given nested layout.
        """

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_inner_layout(item.layout())
                item.layout().deleteLater()


class RunWindow(MultiBox, MainWindow):  # include all children of the MainWindow class here
    def __init__(self):  # initialize all children here
        MainWindow.__init__(self)
        MultiBox.setup_multi(self)

    def resizeEvent(self, event):
        self.update()
        self.update_control()
        self.update_multi()

    def update(self) -> None:
        """
        Updates the positions of all widgets that need their positions updated.

        May also be used to update other stuff in the future.
        """

        box_answer_height = int(self.box_answer_height_percent * (self.height() - self.title_bar_height - (3 * self.box_padding)))

        # text box
        self.box_text.move(self.box_padding, self.box_padding + self.title_bar_height)
        self.box_text.resize(int((self.width() * self.box_width_left) - (self.box_padding * 1.5)), self.height() - box_answer_height - (self.box_padding * 3) - self.title_bar_height)  # 1.5 is used so the gap to the right of the box isn't too big

        # answer box
        self.box_answer.move(self.box_padding, self.height() - self.box_padding - box_answer_height)
        self.box_answer.resize(int((self.width() * self.box_width_left) - (self.box_padding * 1.5)), box_answer_height)

        # answer box icon
        adjust = 8
        # moves the image a bit more away from the format symbol
        icon_new_width = int((self.width() * self.box_width_left) - (self.box_padding * 1.5) - (self.box_answer_padding * 4) - (adjust * 2))
        if self.icon_aspect_ratio_inverse is not None:
            if self.icon_aspect_ratio_inverse * icon_new_width < box_answer_height - (self.box_answer_padding * 2):
                self.box_answer.setIconSize(QSize(icon_new_width, self.height() - self.box_padding - box_answer_height - (self.box_answer_padding * 2)))
            else:
                icon_aspect_ratio = self.icon_aspect_ratio_inverse ** -1
                icon_new_width = int(icon_aspect_ratio * box_answer_height - (self.box_answer_padding * 2))
                self.box_answer.setIconSize(QSize(icon_new_width, box_answer_height - (self.box_answer_padding * 2)))

        # answer format label
        self.box_answer_format_label.move(self.box_padding + self.box_answer_padding, self.height() - self.box_padding - box_answer_height)

    def update_control(self) -> None:
        """
        Updates the positions of all widgets in the control class.
        """

        # move widget
        self.widget_move.move(self.widget_resize_size, self.widget_resize_size)
        self.widget_move.resize(self.width() - self.widget_resize_size - (3 * self.title_bar_height), self.title_bar_height - self.widget_resize_size)

        # close button
        self.button_close.move(self.width() - self.button_width, 0)
        self.button_close.resize(self.button_width, self.title_bar_height)

        # maximize button
        self.button_maximize.move(self.width() - (2 * self.button_width), 0)
        self.button_maximize.resize(self.button_width, self.title_bar_height)

        # minimize button
        self.button_minimize.move(self.width() - (3 * self.button_width), 0)
        self.button_minimize.resize(self.button_width, self.title_bar_height)

        # Resize Widgets, Order: right, top right, top, top left, left, bottom left, bottom, bottom right
        self.widget_resize[0].move(self.width() - self.widget_resize_size, self.widget_resize_size)
        self.widget_resize[0].resize(self.widget_resize_size, self.height() - (2 * self.widget_resize_size))
        self.widget_resize[1].move(self.width() - self.widget_resize_size, 0)
        self.widget_resize[1].resize(self.widget_resize_size, self.widget_resize_size)
        self.widget_resize[2].move(self.widget_resize_size, 0)
        self.widget_resize[2].resize(self.width() - (2 * self.widget_resize_size), self.widget_resize_size)
        self.widget_resize[3].move(0, 0)
        self.widget_resize[3].resize(self.widget_resize_size, self.widget_resize_size)
        self.widget_resize[4].move(0, self.widget_resize_size)
        self.widget_resize[4].resize(self.widget_resize_size, self.height() - (2 * self.widget_resize_size))
        self.widget_resize[5].move(0, self.height() - self.widget_resize_size)
        self.widget_resize[5].resize(self.widget_resize_size, self.widget_resize_size)
        self.widget_resize[6].move(self.widget_resize_size, self.height() - self.widget_resize_size)
        self.widget_resize[6].resize(self.width() - (2 * self.widget_resize_size), self.widget_resize_size)
        self.widget_resize[7].move(self.width() - self.widget_resize_size, self.height() - self.widget_resize_size)
        self.widget_resize[7].resize(self.widget_resize_size, self.widget_resize_size)

    def update_multi(self) -> None:
        """
        Updates the positions of all widgets in the multi class.
        """

        # selectors
        # although this works perfectly, a lot of the math in this section is not optimized and may need to be in the future
        selector_size = (1/len(self.button_selectors)) * (self.width() * (1 - self.box_width_left) - (self.box_padding * 1.5)) + self.box_border - (self.box_border/len(self.button_selectors))  # width of the selector buttons
        check = 0
        for i, button in enumerate(self.button_selectors):

            # corrects for rounding which makes the borders between the buttons change size
            correction = 0
            if i != len(self.button_selectors) - 1:
                correction = (int(((selector_size - self.box_border) * (i - 1)) + (self.box_padding * 2) + (self.width() * self.box_width_left) - (self.box_padding * 1.5)) + int(selector_size) - self.box_border) - int(((selector_size - self.box_border) * i) + (self.box_padding * 2) + (self.width() * self.box_width_left) - (self.box_padding * 1.5))

                if correction == 0 and (int(((selector_size - self.box_border) * i) + (self.box_padding * 2) + (self.width() * self.box_width_left) - (self.box_padding * 1.5)) + int(selector_size) - self.box_border) - int(((selector_size - self.box_border) * (i + 1)) + (self.box_padding * 2) + (self.width() * self.box_width_left) - (self.box_padding * 1.5)) == -1:
                    correction -= 1

            # makes sure the last selector and the box below line up
            elif int(((selector_size - self.box_border) * i) + (self.box_padding * 2) + (self.width() * self.box_width_left) - (self.box_padding * 1.5)) + int(selector_size) != (self.box_padding * 2) + int((self.width() * self.box_width_left) - (self.box_padding * 1.5)) + int((self.width() * (1 - self.box_width_left)) - (self.box_padding * 1.5)):
                correction -= 1

            # move the buttons to their correct place, while keeping the borders the same size
            button.move(int(((selector_size - self.box_border) * i) + (self.box_padding * 2) + (self.width() * self.box_width_left) - (self.box_padding * 1.5)), self.box_padding + self.title_bar_height)
            button.resize(int(selector_size) - correction, self.select_height)

        # multi box
        for tup in self.areas:
            tup[0].move((self.box_padding * 2) + int((self.width() * self.box_width_left) - (self.box_padding * 1.5)), self.box_padding + self.title_bar_height + self.select_height - self.box_border)
            tup[0].resize(int((self.width() * (1 - self.box_width_left)) - (self.box_padding * 1.5)), self.height() - (self.box_padding * 2) - self.title_bar_height - self.select_height + self.box_border)


class TestButtons(RunWindow):  # buttons, and functions for testing purposes
    def __init__(self):
        super().__init__()
        self.setup_test()

    def setup_test(self):

        self.button_hook = []  # holds all testing buttons

        '''
        # size button
        self.button_hook.append(QPushButton('Size', self))
        self.button_hook[-1].clicked.connect(self.get_info)
        '''

        # update button
        self.button_hook.append(QPushButton('Update', self))
        self.button_hook[-1].clicked.connect(self.get_update)

        # answer button
        self.button_hook.append(QPushButton(self.answer_default, self))
        self.button_hook[-1].clicked.connect(self.get_answer)

        # flip button
        self.button_hook.append(QPushButton('Flip', self))
        self.button_hook[-1].clicked.connect(self.flip_type)

        # test button
        self.button_test_toggle = False
        self.button_hook.append(QPushButton('Test', self))
        self.button_hook[-1].clicked.connect(self.test)

        for i, hook in enumerate(self.button_hook):  # sets the button hook parameters
            hook.setGeometry(self.test_horizontal_offset + (i * (self.test_between_spacing + self.test_button_width)), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
            hook.setStyleSheet(f'background-color: None; color: rgb{self.color_title_bar_text}; border: 1px solid rgb{self.color_title_bar_text}; border-radius: 4px;')
            hook.setCursor(Qt.CursorShape.PointingHandCursor)

    def test(self) -> None:
        """
        Used for testing anything in the window.
        """

        self.button_test_toggle = not self.button_test_toggle

        '''
        if self.button_test_toggle:
            self.scroll_area.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.scroll_area.setCursor(Qt.CursorShape.ArrowCursor)
        '''

        print(self.symbols)

    def get_info(self) -> None:
        """
        Prints the current width and height of the window with the use of a button.
        """

        print(f'Width: {self.width()}, Height: {self.height()}')

    def get_update(self) -> None:
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
    settings = SettingsWindow()

    # could not change inactive highlight color with style sheet a style sheet; a style sheet overrides the inactive highlight color
    palette = app.palette()
    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor(settings.color_text[0], settings.color_text[1], settings.color_text[2]))  # inactive highlight text color
    palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor(settings.color_text_highlight_active[0], settings.color_text_highlight_active[1], settings.color_text_highlight_active[2]))  # active highlight color
    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor(settings.color_text_highlight_inactive[0], settings.color_text_highlight_inactive[1], settings.color_text_highlight_inactive[2]))  # inactive highlight color
    app.setPalette(palette)

    # starts the window
    window = TestButtons()  # set the window equal to RunWindow() to run without the test buttons, set it to TestButtons() to run it with them
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
