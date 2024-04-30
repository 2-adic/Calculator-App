import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QLineEdit, QVBoxLayout, QPlainTextEdit, QScrollArea, QHBoxLayout, QFrame, QLayout
from PyQt6.QtGui import QColor, QPainter, QIcon, QFont, QPalette, QMouseEvent
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize
import sympy as sy
import pyperclip
from sortedcontainers import SortedDict
import fontcontrol
import files
from str_format import contains_substring
from PIL import Image
from latex import convert_render_latex
import ctypes
import platform


'''
General:
    - "Cannot find reference 'connect' in 'pyqtSignal | pyqtSignal | function'" is a benign warning

Bugs: 
    - When deleting multiple variables at once, some variables in the multi area are still showing up

    - Implicit multiplication before a decimal is not working
        - Ex:
            - x.1 -> x(1/10): should be x*(1/10)
        - Not sure if this functionality is wanted anymore
        - x.1 seems as an incorrect way to write this out, check how other calculators handle this case
            

    - When using tab to go to the next variable, it sometimes skips to the textbox
        - How it should work (in each step the user presses tab), it should loop as shown: text box -> variable 1 -> variable 2 -> variable -> n -> text box
        - give the user a way to still type a tab in the text box (maybe mac: option + tab, Windows: 'not sure yet' + tab)

    - App crashes when user inputs ".." and clicks the answer button

    - If the user in a variable box while their mouse is on top of a variable text box, the mouse flashes between two different cursor shapes
    
    - LaTeX answer image still clips outside of the answer box in specific circumstances
        - Bug does not happen on Windows, only on MacOS (not sure why)
        - Ex: x + 7

Future Features:
    - Need shadowing for the sides of the window (for Windows)

    - Add a settings section
        - Option to toggle commas; 1,000,000 <-> 1000000
        - Option to toggle between radians and degrees

    - Add window's snap functionality
        - Find a way to do it

    - App Icon for taskbar (also one for when you hover on the window where it shows on the top left)

    - Animation for minimizing functionality (for Windows)

    - Plus minus (±)
        - Ex, x = 2:
            - When in exact form: 5x ± 1 -> (5*2) ± 1 -> 10 ± 1
            - When in approximate form:  5x ± 1 -> 5x + 1 -> (5*2) + 1 -> 10 + 1 -> 11  (Displays both answers somehow)
                                            -> 5x - 1 -> (5*2) - 1 -> 10 - 1 -> 9

    - Represent functions like cos() with italics
        - Might solve this problem another way without the use of color (not sure yet)
        - Make the "cos" highlight if the program detects it may be a function
            - If the user does an input (click + control, not sure), cos turns into italics and is considered a function instead of c*o*s
        - May want a font where the italics are the same width as the normal characters

    - If a variable is typed in the text box of another variable, add the new variable to the variable box

    - Add a scroll bar to the answer text box to see very large answers

    - Need to test if circularly defined variables are being detected every time
        - Need to give error for all cases where this occurs (not giving an error at all atm)

    - Add pin feature for variables so they don't get removed while its active

    - Integral functionality
        - ∫_d_
    
    - Find a way to change the font of the LaTeX image
    
    - Maybe increase the size of the format symbol
    
    - Maybe add a background to the scroll bar in the scroll area
'''


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

        # Answer box
        self.answer_default = 'Answer'
        self.answer_format_size = 20  # the size of the symbol that shows the current selected answer format

        self.box_answer_height_percent = 2/5  # percentage of screen height
        self.box_answer_padding = 12  # distance from the image to the border of the answer box
        self.latex_image_dpi = 800

        # Multi box
        self.content_margin = 30  # distance between the scroll content, and the border

        # -------------------------------------------------------------------------------------------------------


class ControlWindow(QMainWindow, SettingsWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        SettingsWindow.__init__(self)

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
        self.title_label.setStyleSheet('color: rgb(148, 155, 164); font-weight: bold; font-size: 11px;')
        self.title_label.move(self.window_title_position[0], self.window_title_position[1])

        # close button
        self.button_close = QPushButton('', self)
        self.button_close.setIcon(QIcon(files.file_path('button_close_icon.png', 'icons')))
        self.button_close.setStyleSheet(
            "QPushButton { background-color: transparent; color: rgb(181, 186, 193); border: none; font-size: 11px;}"
            "QPushButton:hover { background-color: rgb(242, 63, 66); border: none; }"
        )
        self.button_close.clicked.connect(self.button_close_logic)

        # maximize button
        self.button_maximize = QPushButton('', self)
        self.button_maximize.setIcon(QIcon(files.file_path('button_maximize_icon.png', 'icons')))
        self.button_maximize.setStyleSheet(
            "QPushButton { background-color: transparent; color: rgb(181, 186, 193); border: none; font-weight: bold; font-size: 11px;}"
            "QPushButton:hover { background-color: rgb(45, 46, 51); border: none; }"
        )
        self.button_maximize.clicked.connect(self.button_maximize_logic)

        # minimize button
        self.button_minimize = QPushButton('', self)
        self.button_minimize.setIcon(QIcon(files.file_path('button_minimize_icon.png', 'icons')))
        self.button_minimize.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }"
            "QPushButton:hover { background-color: rgb(45, 46, 51); border: none; }"
            "QPushButton::icon { margin-bottom: -5px; }"
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

    def paintEvent(self, event) -> None:
        """
        Gives the background and titlebar their colors.
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # title bar
        painter.fillRect(0, 0, self.width(), self.title_bar_height, QColor(30, 31, 34))

        # center window
        painter.fillRect(0, self.title_bar_height, self.width(), self.height() - self.title_bar_height, QColor(49, 51, 56))

    def window_resize_enable(self):
        """
        Re-enables resizing after the timer expires.
        """

        self.window_resize_allowed = True

    def button_close_logic(self) -> None:
        """
        Checks if work was saved, then closes the window. Uses the exit button.
        """

        # logic for saving will go here

        # eventually may want to keep the program running after the window exits
        exit()  # instantly exits the program

    def button_maximize_logic(self) -> None:
        """
        Maximizes the screem using the maximize button.
        """

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

                self.button_maximize_logic()

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
        self.flip_type_toggle = False
        self.image = None
        self.icon_aspect_ratio_inverse = None

        self.box_answer = QPushButton(self.answer_default, self)
        self.box_answer.setStyleSheet('border: 3px solid rgb(35, 36, 40); background-color: rgb(85, 88, 97); border-radius: 6px; color: white; font-size: 15px;')
        self.box_answer.clicked.connect(self.copy)

        self.answer_image_path = files.file_path('latex_answer.png', None)  # gets the path of the latex image

        # answer format label
        self.box_answer_format_label = QLabel('', self)
        self.box_answer_format_label.setStyleSheet(f'font-size: {self.answer_format_size}px; color: white')

        # text box
        self.user_select = None

        self.user_mouse_set = False
        self.variables = SortedDict()  # stores variables in a sorted dictionary, so it shows in alphabetical order

        self.accepted_variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.accepted_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.accepted_other = ['(']

        self.box_text = QPlainTextEdit(self)
        self.box_text.textChanged.connect(self.text_update)
        self.box_text.setStyleSheet(
            '''
            QPlainTextEdit {
                border: 3px solid rgb(35, 36, 40);
                background-color: rgb(85, 88, 97);
                border-radius: 6px;
                color: white;
                font-size: 15px;
            }
            QScrollBar:vertical {
                border-radius: 4px;
                background-color: #3f4148;
                width: 12px;
                margin: 4px 4px 4px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #232428;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                width: 0px;
            }
            QScrollBar::sub-line:vertical {
                width: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
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
            if string[x] in self.accepted_variables or string[x] in self.accepted_numbers or string[x] == ')' or string[x] == '.':
                if string[x + 1] in self.accepted_variables or string[x + 1] == '(':
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

    def answer_formatting_after(self, answer: sy) -> str:
        """
        Reformats the string after the answer is calculated.

        Makes it easier for the user to read the answer.
        """

        string = str(answer)

        string = string.replace('**', '^')
        return string

    def variable_formatting(self, variables: SortedDict) -> dict:
        temp1 = variables.copy()

        for x in temp1:
            temp1[x] = temp1[x][1].text()

            if temp1[x] == '':
                temp1[x] = x

        # starts here
        for x in temp1:

            if temp1[x] == x or not contains_substring(temp1[x], list(self.variables.keys())):
                continue

            temp2 = temp1.copy()
            for y in temp2:
                for z in temp2:

                    if temp2[z] == z or not contains_substring(temp2[z], list(self.variables.keys())):
                        continue

                    temp1[z] = temp1[z].replace(y, f'({temp2[y]})')

            print(temp1)

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

        # scans the text for any variables
        temp = self.variable_formatting(self.variables)

        for x in text:
            if x in temp:
                test_variable = temp[x]

                text = text.replace(f'{x}', f'({test_variable})')

        text = self.answer_formatting_before(text)  # reformats the string

        # tests if the user did something wrong and outputs 'error' if so
        try:
            self.answer = sy.sympify(text)

            # sometimes sy.sympify doesn't simplify completely, but removing spaces and looping fixes some problems
            while str(self.answer).replace(' ', '') != str(sy.sympify(str(self.answer).replace(' ', ''))).replace(' ', ''):
                self.answer = sy.sympify(str(self.answer).replace(' ', ''))

            print(f'Answer: {text} = {self.answer}')
        except Exception as e:
            self.answer = 'Error'
            print(f'Error: {e}')

        self.answer_temp = self.answer_formatting_after(self.answer)  # reformats the answer

        # use this for option that lets the user set the non latex image as the answer
        # self.box_answer.setText(self.answer_temp)  # displays the answer

        convert_render_latex(self.answer_temp, self.latex_image_dpi)

        self.box_answer.setText('')
        self.box_answer.setIcon(QIcon(self.answer_image_path))
        self.image = Image.open(self.answer_image_path)
        self.icon_aspect_ratio_inverse = self.image.size[1] / self.image.size[0]

        self.box_answer_format_label.setText('=')  # answer defaults in exact mode

        self.resizeEvent(None)  # updates to resize the new image

    def flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        if self.answer == self.answer_default:
            return

        self.flip_type_toggle = not self.flip_type_toggle  # keeps track of which format is being displayed

        # uses self.answer_temp to save the actual answer
        if self.flip_type_toggle:
            self.answer_temp = sy.N(self.answer)  # turns the answer into its decimal format
            self.box_answer_format_label.setText('≈')
        else:
            self.answer_temp = self.answer  # returns the original answer
            self.box_answer_format_label.setText('=')

        self.answer_temp = self.answer_formatting_after(self.answer_temp)  # reformats the answer

        convert_render_latex(self.answer_temp, self.latex_image_dpi)

        self.box_answer.setIcon(QIcon(self.answer_image_path))
        self.image = Image.open(self.answer_image_path)
        self.icon_aspect_ratio_inverse = self.image.size[1] / self.image.size[0]

        self.resizeEvent(None)

        # self.box_answer.setText(self.answer_temp)  # displays the answer

    def copy(self) -> None:
        """
        Lets the user copy the answer by clicking the answer box.
        """

        # adds flashing blue visual when button is clicked
        self.box_answer.setStyleSheet('border: 3px solid rgb(35, 36, 40); background-color: rgb(81, 100, 117); border-radius: 6px; color: white; font-size: 15px;')
        QTimer.singleShot(150, lambda: self.box_answer.setStyleSheet('border: 3px solid rgb(35, 36, 40); background-color: rgb(85, 88, 97); border-radius: 6px; color: white; font-size: 15px;'))

        pyperclip.copy(str(self.answer_temp))  # copies answer to clipboard

    def text_update(self) -> None:
        """
        Activates each time a user changes their input in the text box.

        Adds and removes variables in the variables box based on the new user input.
        Removes the answer from the answer box.
        """

        self.user_select = self.sender()  # saves which text box the user was typing in

        text = self.box_text.toPlainText()

        temp = set()  # used later for deleting variables in self.variables which are not in the text box

        # adds all variables from the text box to a dictionary
        for x in text:
            if x in self.accepted_variables:
                temp.add(x)
                if x not in self.variables:
                    label = QLabel(f'{x} =', self)

                    text_box = QLineEdit(self)
                    text_box.setPlaceholderText(f'{x}')

                    self.variables[x] = (label, text_box)

        for y in self.variables:
            for x in self.variables[y][1].text():
                if x in self.accepted_variables:
                    temp.add(x)
                    if x not in self.variables:
                        label = QLabel(f'{x} =', self)

                        text_box = QLineEdit(self)
                        text_box.setPlaceholderText(f'{x}')

                        self.variables[x] = (label, text_box)

        # deletes all variables not in the text box
        for x in self.variables:
            if x not in temp:
                del self.variables[x]

        '''
        # fix - cursor_flash: may delete
        for x in self.variables:
            if self.variables[x][1].underMouse():
                self.scroll_area.setCursor(Qt.CursorShape.IBeamCursor)
        self.user_mouse_set = True
        '''

        self.scroll_area_clear()  # deletes the all variables in the variable box
        self.scroll_area_fill()  # adds all variables found in the variable box

        # clears the answer box to prevent user from thinking the answer is for what was just typed in the text box
        self.answer = self.answer_default  # sets answer to default answer so if the user flips the format, the default answer still displays
        self.box_answer.setIcon(QIcon())

        self.box_answer.setText(f'{str(self.answer)}')  # displays the answer

        self.box_answer_format_label.setText('')


class MultiWindow(MainWindow):
    def __init__(self):
        super().__init__()

        self.setup_multi()

    def setup_multi(self):
        # scroll area
        self.scroll_layout = QVBoxLayout()
        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)

        # --------------------------------------------------------------------------------------------------------

        self.scroll_area.setStyleSheet(
            '''
            QScrollArea {
                border: 3px solid #232428;
                background-color: #555861;
                border-radius: 6px;
                color: white;
                font-size: 15px;
            }
            QScrollBar:vertical {
                border-radius: 4px;
                background-color: #3f4148;
                width: 12px;
                margin: 4px 4px 4px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #232428;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                width: 0px;
            }
            QScrollBar::sub-line:vertical {
                width: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            '''
        )

        self.scroll_content.setStyleSheet(
            'border: transparent;'
            'background-color: transparent;'
            'color: white;'
            'font-size: 15px;'
        )

        self.scroll_layout.setContentsMargins(self.content_margin, self.content_margin, self.content_margin, self.content_margin)
        self.scroll_area.setWidget(self.scroll_content)

    def scroll_area_fill(self) -> None:
        """
        Displays widgets to the variable box.

        Adds: labels and text boxes for each variable, lines to separate each variable, and a stretch to push all widgets to the top.
        """

        for x in self.variables:
            layout = QHBoxLayout()
            layout.addWidget(self.variables[x][0])

            self.variables[x][1].textChanged.connect(self.text_update)
            layout.addWidget(self.variables[x][1])

            self.scroll_layout.addLayout(layout)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            line.setStyleSheet(f"background-color: #313338; border-radius: 1px")

            self.scroll_layout.addWidget(line)

        self.scroll_layout.addStretch()

        if self.user_select != self.box_text:
            self.user_select.setFocus()

    def scroll_area_clear(self) -> None:
        """
        Removes all widgets from the variable box.
        """
        for i in reversed(range(self.scroll_layout.count())):
            layout_item = self.scroll_layout.itemAt(i)

            if layout_item.widget():
                widget_to_remove = layout_item.widget()
                # Check if the widget is a QLineEdit and disconnect the textChanged signal
                if isinstance(widget_to_remove, QLineEdit):
                    try:
                        widget_to_remove.textChanged.disconnect(self.text_update)
                    except TypeError:
                        # No connections to disconnect
                        pass
                self.scroll_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)
            elif layout_item.layout():
                self.clear_inner_layout(layout_item.layout())
            elif layout_item.spacerItem():
                # If the item is a spacer, remove it from the layout
                self.scroll_layout.removeItem(layout_item)

    def clear_inner_layout(self, layout: QLayout) -> None:
        """
        Removes layouts.

        May only work for layouts in the format: (QLabel, QLineEdit). Need to test later.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                # Check if the widget is a QLineEdit and should be kept
                if isinstance(widget, QLineEdit):
                    try:
                        widget.textChanged.disconnect(self.text_update)
                    except TypeError:
                        # No connections to disconnect
                        pass
                    # Remove the QLineEdit widget from its parent layout
                    layout.removeWidget(widget)
                    widget.setParent(None)
                elif isinstance(widget, QLabel):
                    # Handle QLabel widgets if necessary
                    layout.removeWidget(widget)
                    widget.setParent(None)
                else:
                    widget.deleteLater()
            elif item.layout():
                # Recursively clear nested layouts
                self.clear_inner_layout(item.layout())


class TestWindow(MainWindow):  # buttons, and functions for testing purposes
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

        for i in range(len(self.button_hook)):  # sets the button hook parameters
            self.button_hook[i].setGeometry(self.test_horizontal_offset + (i * (self.test_between_spacing + self.test_button_width)), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
            self.button_hook[i].setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
            self.button_hook[i].setCursor(Qt.CursorShape.PointingHandCursor)

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

        print(self.variables)

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


class RunWindow(TestWindow, MultiWindow, MainWindow):  # include all children of the MainWindow class here
    def __init__(self):  # initialize all children here
        MainWindow.__init__(self)
        TestWindow.setup_test(self)
        MultiWindow.setup_multi(self)

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
        icon_new_width = int((self.width() * self.box_width_left) - (self.box_padding * 1.5) - (self.box_answer_padding * 4))
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

        # multi box
        self.scroll_area.move((self.box_padding * 2) + int((self.width() * self.box_width_left) - (self.box_padding * 1.5)), self.box_padding + self.title_bar_height)
        self.scroll_area.resize(int((self.width() * (1 - self.box_width_left)) - (self.box_padding * 1.5)), self.height() - (self.box_padding * 2) - self.title_bar_height)


def main():

    app = QApplication(sys.argv)

    system_name = platform.system()
    if system_name == 'Windows':
        # configures windows to show the taskbar icon
        myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        print("Operating system is Windows")

    if system_name == 'Darwin':
        print("Operating system is macOS")

    elif system_name == 'Linux':
        print("Operating system is Linux")

    # sets the icon for the app
    app.setWindowIcon(QIcon(files.file_path('taskbar_icon_16px.png', 'icons')))

    # sets the default font
    font_family = fontcontrol.font_load(fontcontrol.font_files[0])
    if font_family:
        font = QFont(font_family, fontcontrol.font_size)
        app.setFont(font)
    else:
        print("Error: Font didn't load, default system font will be used instead.")

    # default settings
    # could not change inactive highlight color with style sheet a style sheet; a style sheet overrides the inactive highlight color
    palette = app.palette()
    palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor('#46739c'))  # active highlight color
    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor('#ffffff'))  # active highlight text color
    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor('#b0b0b0'))  # inactive highlight color
    palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor('#ffffff'))  # inactive highlight text color
    app.setPalette(palette)

    # starts the window
    window = RunWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
