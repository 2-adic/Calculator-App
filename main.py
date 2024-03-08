import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QLineEdit, QVBoxLayout, \
    QPlainTextEdit, QScrollArea, QHBoxLayout, QFrame, QLayout
from PyQt6.QtGui import QColor, QPainter, QIcon, QFont, QPalette, QMouseEvent, QFontDatabase
from PyQt6.QtCore import Qt, QPoint, QTimer
import sympy as sy
import pyperclip
from sortedcontainers import SortedDict
import fontcontrol

'''
General:
    - "Cannot find reference 'connect' in 'pyqtSignal | pyqtSignal | function'" is a benign warning

Bugs: 
    - When answer format is flipped to decimal, it doesn't give an exact answer
        - Ex: 1.1 -> 11/10 -> *User clicks format flip button* -> 1.10000000000000
        - There might not be a solution for this bug
        - May not consider it a bug, since the decimal format is not meant to be exact in the first place
        
    - When deleting multiple variables at once, some variables in the definition area are still showing up
    
    - Implicit multiplication before a decimal is not working
        - Ex:
            x.1 -> x(1/10): should be x*(1/10)
            
    - When using tab to go to the next variable, it sometimes skips to the textbox
        - How it should work (in each step the user presses tab), it should loop as shown: text box -> variable 1 -> variable 2 -> variable -> n -> text box
        - give the user a way to still type a tab in the text box (maybe mac: option + tab, Windows: 'not sure yet' + tab)
        
    - Resizing doesn't work on macOS
        - Used to work before updating to PyQt6
        - Not sure why, needs testing
        - The window resizes, but the widgets don't resize
        
    - App crashes when user inputs ".." and clicks the answer button
    
    - Long answers clip outside of the answer box
    
    - If the user in a variable box while their mouse is on top of a variable text box,the mouse flashes between two shapes

Future Features:
    - Need shadowing for the sides of the window
    
    - Add a settings section
        - Option to toggle commas; 1,000,000 <-> 1000000
        - Option to toggle between radians and degrees
    
    - Add window's snap functionality
        - Updated to PyQt6 for this (the feature might be accessible in PyQt6)
    
    - App Icon for taskbar (also one for when you hover on the window where it shows on the top left)
    
    - Minimizing functionality for when the user clicks the app icon
    
    - Plus minus (±)
        - Ex, x = 2:
            - When in exact form: 5x ± 1 -> (5*2) ± 1 -> 10 ± 1
            - When in decimal form:  5x ± 1 -> 5x + 1 -> (5*2) + 1 -> 10 + 1 -> 11  (Displays both answers somehow)
                                            -> 5x - 1 -> (5*2) - 1 -> 10 - 1 -> 9
                                           
    - Approximation (≈) symbol in the top left of the answer box if the decimal value is longer than a certain amount of digits / find another way to see if the value displayed isn't the exact value\
        - A equals (=) symbol for when the format is exact
    
    - Represent functions like cos() with italics
        - Make the "cos" highlight if the program detects it may be a function
            - If the user does an input (click + control, not sure), cos turns into italics and is considered a function instead of c*o*s
        - May want a font where the italics are the same width as the normal characters
        
    - If a variable is typed in the text box of another variable, add the new variable to the variable box
    
    - Add a scroll bar to the answer text box to see very large answers
    
    - Need to test if circularly defined variables are being detected every time
        - Need to give error for all cases where this occurs (not giving an error at all atm)
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window ------------------------------------------------------------------------------------------------
        self.setGeometry(100, 100, 800, 600)  # initial window size / position
        self.setWindowTitle("Calculator")  # window title
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)  # removes default title bar

        self.widget_resize_size = 5
        self.title_bar_height = 22  # Height of the title bar
        self.window_size_min_x = 650  # minimum width of the window
        self.window_size_min_y = 450  # minimum height of the window
        # -------------------------------------------------------------------------------------------------------

        # Title Bar ---------------------------------------------------------------------------------------------
        self.window_moving = False  # initial state of the window moving
        self.offset = None  # initial state of the window offset
        self.button_width = int(1.3 * self.title_bar_height)

        # window move widget
        self.widget_move = QWidget(self)

        # displayed title
        self.title_label = QLabel('Calculator', self)
        self.title_label.setStyleSheet('color: rgb(148, 155, 164); font-weight: bold; font-size: 11px;')
        self.title_label.move(5, -5)

        # close button
        self.button_close = QPushButton('', self)
        self.button_close.setIcon(
            QIcon('C:\\Users\\mglin\\PycharmProjects\\Apps\\Window\\Math App\\external\\button_close_icon.png'))
        self.button_close.setStyleSheet(
            "QPushButton { background-color: transparent; color: rgb(181, 186, 193); border: none; font-size: 11px;}"
            "QPushButton:hover { background-color: rgb(242, 63, 66); border: none; }"
        )
        self.button_close.clicked.connect(self.button_close_logic)

        # maximize button
        self.button_maximize = QPushButton('', self)
        self.button_maximize.setIcon(
            QIcon('C:\\Users\\mglin\\PycharmProjects\\Apps\\Window\\Math App\\external\\button_maximize_icon.png'))
        self.button_maximize.setStyleSheet(
            "QPushButton { background-color: transparent; color: rgb(181, 186, 193); border: none; font-weight: bold; font-size: 11px;}"
            "QPushButton:hover { background-color: rgb(45, 46, 51); border: none; }"
        )
        self.button_maximize.clicked.connect(self.button_maximize_logic)

        # minimize button
        self.button_minimize = QPushButton('', self)
        self.button_minimize.setIcon(
            QIcon('C:\\Users\\mglin\\PycharmProjects\\Apps\\Window\\Math App\\external\\button_minimize_icon.png'))
        self.button_minimize.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }"
            "QPushButton:hover { background-color: rgb(45, 46, 51); border: none; }"
            "QPushButton::icon { margin-bottom: -5px; }"
        )
        self.button_minimize.clicked.connect(self.showMinimized)

        # test button parameters
        self.test_padding = 2
        self.test_between_spacing = 10
        self.test_horizontal_offset = 90
        self.test_button_width = 50

        # don't change
        self.test_between_spacing = self.test_between_spacing + self.test_button_width
        self.test_counter = 0

        '''
        # size button
        self.button_size = QPushButton('Size', self)
        self.button_size.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
        self.button_size.setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_size.clicked.connect(self.get_info)
        self.button_size.setCursor(Qt.PointingHandCursor)
        self.test_counter += 1
        '''

        '''
        # update button
        self.button_update = QPushButton('Update', self)
        self.button_update.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
        self.button_update.setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_update.clicked.connect(self.get_update)
        self.button_update.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_counter += 1
        '''

        # answer button
        self.answer_default = 'Answer'
        self.button_answer = QPushButton(self.answer_default, self)
        self.button_answer.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing),
                                       self.test_padding, self.test_button_width - (2 * self.test_padding),
                                       self.title_bar_height - (2 * self.test_padding))
        self.button_answer.setStyleSheet(
            'background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_answer.clicked.connect(self.get_answer)
        self.button_answer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_counter += 1

        # flip button
        self.button_flip = QPushButton('Flip', self)
        self.button_flip.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing),
                                     self.test_padding, self.test_button_width - (2 * self.test_padding),
                                     self.title_bar_height - (2 * self.test_padding))
        self.button_flip.setStyleSheet(
            'background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_flip.clicked.connect(self.flip_type)
        self.button_flip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_counter += 1

        # test button
        self.button_test_toggle = False
        self.button_test = QPushButton('Test', self)
        self.button_test.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
        self.button_test.setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_test.clicked.connect(self.test)
        self.button_test.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_counter += 1
        # -------------------------------------------------------------------------------------------------------

        # Resizing Widgets --------------------------------------------------------------------------------------
        self.window_resize = True  # initial state of resizing
        self.window_resize_direction = None  # initial direction of resizing
        self.widget_resize_toggle = True

        # top
        self.widget_resize_top = QWidget(self)
        self.widget_resize_top.setCursor(Qt.CursorShape.SizeVerCursor)

        # bottom
        self.widget_resize_bottom = QWidget(self)
        self.widget_resize_bottom.setCursor(Qt.CursorShape.SizeVerCursor)

        # left
        self.widget_resize_left = QWidget(self)
        self.widget_resize_left.setCursor(Qt.CursorShape.SizeHorCursor)

        # right
        self.widget_resize_right = QWidget(self)
        self.widget_resize_right.setCursor(Qt.CursorShape.SizeHorCursor)

        # top left
        self.widget_resize_top_left = QWidget(self)
        self.widget_resize_top_left.setCursor(Qt.CursorShape.SizeFDiagCursor)

        # top right
        self.widget_resize_top_right = QWidget(self)
        self.widget_resize_top_right.setCursor(Qt.CursorShape.SizeBDiagCursor)

        # bottom left
        self.widget_resize_bottom_left = QWidget(self)
        self.widget_resize_bottom_left.setCursor(Qt.CursorShape.SizeBDiagCursor)

        # bottom right
        self.widget_resize_bottom_right = QWidget(self)
        self.widget_resize_bottom_right.setCursor(Qt.CursorShape.SizeFDiagCursor)
        # -------------------------------------------------------------------------------------------------------

        # answer box
        self.answer = 'Error'  # user shouldn't be able to access this string yet
        self.answer_final = self.answer_default
        self.answer_temp = self.answer_final
        self.flip_type_toggle = False

        self.box_answer_height = 80
        self.box_answer = QPushButton(self.answer_default, self)
        self.box_answer.setStyleSheet(
            'border: 3px solid rgb(35, 36, 40); background-color: rgb(85, 88, 97); border-radius: 6px; color: white; font-size: 15px;')
        self.box_answer.clicked.connect(self.copy)

        # answer format label
        self.box_answer_format_label = QLabel('', self)
        self.box_answer_format_label.setStyleSheet('font-size: 18px; color: white')

        # text box
        self.user_select = None
        self.box_padding = 20

        self.user_mouse_set = False
        self.variables = SortedDict()  # stores variables in a sorted dictionary, so it shows in alphabetical order

        self.accepted_variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.accepted_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.accepted_other = ['(']

        # Create a QLineEdit with initial position (150, 50)
        self.box_text = QPlainTextEdit(self)
        self.box_text.textChanged.connect(self.text_update)

        # old: rgb(56, 58, 64),
        self.box_text.setStyleSheet(
            '''
            QPlainTextEdit {
                border: 3px solid rgb(35, 36, 40);
                background-color: rgb(85, 88, 97);
                border-radius: 6px;
                color: white;
                font-size: 15px;
            }
            '''
        )

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
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: red;
            }
            QScrollBar:vertical {
                border: none;
                background-color: rgba(0, 0, 0, 0);
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
            ''
            '   border: transparent;'
            '   background-color: transparent;'
            '   color: white;'
            '   font-size: 15px;'
            ''
        )

        self.test_margin = 50
        self.scroll_layout.setContentsMargins(self.test_margin, self.test_margin, self.test_margin, self.test_margin)
        self.scroll_area.setWidget(self.scroll_content)

        # initializes all widgets in their positions
        self.window_update()

    def test(self) -> None:
        """
        Used for testing anything using a button in the window.
        """

        self.button_test_toggle = not self.button_test_toggle

        if self.button_test_toggle:
            self.scroll_area.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.scroll_area.setCursor(Qt.CursorShape.ArrowCursor)

        print(self.variables)


    def paintEvent(self, event) -> None:
        """
        Gives the background and titlebar their colors.
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # title bar
        painter.fillRect(0, 0, self.width(), self.title_bar_height, QColor(30, 31, 34))

        # center window
        painter.fillRect(0, self.title_bar_height, self.width(), self.height() - self.title_bar_height,
                         QColor(49, 51, 56))

    def get_info(self) -> None:
        """
        Prints the current width and height of the window with the use of a button.
        """

        print(f'Width: {self.width()}, Height: {self.height()}')

    def get_update(self) -> None:
        """
        For manually updating the window with a button.
        """

        self.window_update()
        print('Manually Updated')

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
        for x in range(len(temp1)):
            temp2 = temp1.copy()
            for y in temp2:
                for z in temp2:
                    temp1[z] = temp1[z].replace(y, f'({temp2[y]})')

        for x in temp1:
            if x in temp1[x]:
                print('Error: A variable is circularly defined.')

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
        self.box_answer.setText(self.answer_temp)  # displays the answer

        self.box_answer_format_label.setText('=')  # answer defaults in exact mode

    def flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        self.flip_type_toggle = not self.flip_type_toggle  # keeps track of which format is being displayed

        # uses self.answer_temp to save the actual answer
        if self.flip_type_toggle:
            self.answer_temp = sy.N(self.answer)  # turns the answer into its decimal format
            self.box_answer_format_label.setText('≈')
        else:
            self.answer_temp = self.answer  # returns the original answer
            self.box_answer_format_label.setText('=')

        self.answer_temp = self.answer_formatting_after(self.answer_temp)  # reformats the answer
        self.box_answer.setText(self.answer_temp)  # displays the answer

    def copy(self) -> None:
        """
        Lets the user copy the answer by clicking the answer box.
        """

        # adds flashing blue visual when button is clicked
        self.box_answer.setStyleSheet(
            'border: 3px solid rgb(35, 36, 40); background-color: rgb(81, 100, 117); border-radius: 6px; color: white; font-size: 15px;')
        QTimer.singleShot(150, lambda: self.box_answer.setStyleSheet(
            'border: 3px solid rgb(35, 36, 40); background-color: rgb(85, 88, 97); border-radius: 6px; color: white; font-size: 15px;'))

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
        self.box_answer.setText(f'{str(self.answer)}')  # displays the answer

        self.box_answer_format_label.setText('')

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

            self.widget_resize_top.setEnabled(True)
            self.widget_resize_bottom.setEnabled(True)
            self.widget_resize_left.setEnabled(True)
            self.widget_resize_right.setEnabled(True)
            self.widget_resize_top_left.setEnabled(True)
            self.widget_resize_top_right.setEnabled(True)
            self.widget_resize_bottom_left.setEnabled(True)
            self.widget_resize_bottom_right.setEnabled(True)

        else:
            # maximize window
            self.showMaximized()

            self.widget_resize_toggle = False

            self.widget_resize_top.setEnabled(False)
            self.widget_resize_bottom.setEnabled(False)
            self.widget_resize_left.setEnabled(False)
            self.widget_resize_right.setEnabled(False)
            self.widget_resize_top_left.setEnabled(False)
            self.widget_resize_top_right.setEnabled(False)
            self.widget_resize_bottom_left.setEnabled(False)
            self.widget_resize_bottom_right.setEnabled(False)

        QTimer.singleShot(0, self.window_update)

    def mouseReleaseEvent(self,  event: QMouseEvent | None) -> None:
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

            # not sure why this is here, will review later
            # if self.widget_resize_size < event.y() < self.title_bar_height and self.widget_resize_size < event.x() < self.width() - self.widget_resize_size:
            #     self.window_moving = True
            #     self.offset = event.globalPosition().toPoint() - self.pos()
            #     return

            # Resizing Widgets
            self.window_resize = False
            if self.widget_resize_toggle:
                if self.widget_resize_top.rect().contains(self.widget_resize_top.mapFrom(self, self.offset)):
                    self.window_resize_direction = 0  # top
                    self.window_resize = True
                elif self.widget_resize_bottom.rect().contains(self.widget_resize_bottom.mapFrom(self, self.offset)):
                    self.window_resize_direction = 1  # bottom
                    self.window_resize = True
                elif self.widget_resize_left.rect().contains(self.widget_resize_left.mapFrom(self, self.offset)):
                    self.window_resize_direction = 2  # left
                    self.window_resize = True
                elif self.widget_resize_right.rect().contains(self.widget_resize_right.mapFrom(self, self.offset)):
                    self.window_resize_direction = 3  # right
                    self.window_resize = True
                elif self.widget_resize_top_left.rect().contains(
                        self.widget_resize_top_left.mapFrom(self, self.offset)):
                    self.window_resize_direction = 4  # top left
                    self.window_resize = True
                elif self.widget_resize_top_right.rect().contains(
                        self.widget_resize_top_right.mapFrom(self, self.offset)):
                    self.window_resize_direction = 5  # top right
                    self.window_resize = True
                elif self.widget_resize_bottom_left.rect().contains(
                        self.widget_resize_bottom_left.mapFrom(self, self.offset)):
                    self.window_resize_direction = 6  # bottom left
                    self.window_resize = True
                elif self.widget_resize_bottom_right.rect().contains(
                        self.widget_resize_bottom_right.mapFrom(self, self.offset)):
                    self.window_resize_direction = 7  # bottom right
                    self.window_resize = True

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

                offset_x = min(int(self.normalGeometry().width() * (self.offset.x() / self.width())),
                               self.normalGeometry().width() - (3 * self.button_width))
                self.offset = QPoint(offset_x, self.offset.y())

                self.button_maximize_logic()

                mouse_position = event.globalPosition().toPoint() - self.offset

            else:
                mouse_position = event.globalPosition().toPoint() - self.offset

            self.move(mouse_position)

        # Resizing Widgets
        elif self.window_resize:

            # top (needs work)
            if self.window_resize_direction == 0:
                temp_event_y = event.position().toPoint().y()

                window_resize_move_y = self.height() - temp_event_y
                if window_resize_move_y >= self.window_size_min_y:
                    self.move(self.x(), self.y() + temp_event_y)
                    self.resize(self.width(), window_resize_move_y)
                    self.window_update()

            # bottom
            elif self.window_resize_direction == 1:
                window_resize_move_y = event.position().toPoint().y()
                if window_resize_move_y >= self.window_size_min_y:
                    self.resize(self.width(), window_resize_move_y)
                    self.window_update()

            # left (needs work)
            elif self.window_resize_direction == 2:
                temp_event_x = event.position().toPoint().x()

                window_resize_move_x = self.width() - temp_event_x
                if window_resize_move_x >= self.window_size_min_x:
                    self.move(self.x() + temp_event_x, self.y())
                    self.resize(window_resize_move_x, self.height())
                    self.window_update()

            # right
            elif self.window_resize_direction == 3:
                window_resize_move_x = event.position().toPoint().x()
                if window_resize_move_x >= self.window_size_min_x:
                    self.resize(window_resize_move_x, self.height())
                    self.window_update()

            # top left (needs major work)
            elif self.window_resize_direction == 4:
                temp_event_x = event.position().toPoint().x()
                temp_event_y = event.position().toPoint().y()
                temp_self_x = self.x()
                temp_self_y = self.y()
                temp_height = self.height()
                temp_width = self.width()

                window_resize_move_x = temp_width - temp_event_x
                window_resize_move_y = temp_height - temp_event_y
                if window_resize_move_x >= self.window_size_min_x and window_resize_move_y >= self.window_size_min_y:
                    self.resize(window_resize_move_x, window_resize_move_y)
                    self.move(temp_self_x + temp_event_x, temp_self_y + temp_event_y)
                    self.window_update()
                elif window_resize_move_x >= self.window_size_min_x:
                    self.resize(window_resize_move_x, temp_height)
                    self.move(temp_self_x + temp_event_x, temp_self_y)
                    self.window_update()
                elif window_resize_move_y >= self.window_size_min_y:
                    self.resize(temp_width, window_resize_move_y)
                    self.move(temp_self_x, temp_self_y + temp_event_y)
                    self.window_update()

            # top right (needs work)
            elif self.window_resize_direction == 5:
                temp_event_y = event.position().toPoint().y()
                temp_height = self.height()

                window_resize_move_x = event.position().toPoint().x()
                window_resize_move_y = temp_height - temp_event_y
                if window_resize_move_x >= self.window_size_min_x and window_resize_move_y >= self.window_size_min_y:
                    self.move(self.x(), self.y() + temp_event_y)
                    self.resize(window_resize_move_x, window_resize_move_y)
                    self.window_update()
                elif window_resize_move_x >= self.window_size_min_x:
                    self.resize(window_resize_move_x, temp_height)
                    self.window_update()
                elif window_resize_move_y >= self.window_size_min_y:
                    self.move(self.x(), self.y() + temp_event_y)
                    self.resize(self.width(), window_resize_move_y)
                    self.window_update()

            # bottom left (needs work)
            elif self.window_resize_direction == 6:
                temp_event_x = event.position().toPoint().x()
                temp_width = self.width()

                window_resize_move_x = temp_width - temp_event_x
                window_resize_move_y = event.position().toPoint().y()
                if window_resize_move_x >= self.window_size_min_x and window_resize_move_y >= self.window_size_min_y:
                    self.move(self.x() + temp_event_x, self.y())
                    self.resize(window_resize_move_x, window_resize_move_y)
                    self.window_update()
                elif window_resize_move_x >= self.window_size_min_x:
                    self.move(self.x() + temp_event_x, self.y())
                    self.resize(window_resize_move_x, self.height())
                    self.window_update()
                elif window_resize_move_y >= self.window_size_min_y:
                    self.resize(self.width(), window_resize_move_y)
                    self.window_update()

            # bottom right
            elif self.window_resize_direction == 7:

                window_resize_move_x = max(self.window_size_min_x, event.position().toPoint().x())
                window_resize_move_y = max(self.window_size_min_y, event.position().toPoint().y())
                self.resize(window_resize_move_x, window_resize_move_y)

                self.window_update()

    def window_update(self) -> None:
        """
        Updates the positions of all widgets that need their positions updated.

        May also be used to update other stuff in the future.
        """

        # move widget
        self.widget_move.move(self.widget_resize_size, self.widget_resize_size)
        self.widget_move.resize(self.width() - self.widget_resize_size - (3 * self.title_bar_height),
                                self.title_bar_height - self.widget_resize_size)

        # close button
        self.button_close.move(self.width() - self.button_width, 0)
        self.button_close.resize(self.button_width, self.title_bar_height)

        # maximize button
        self.button_maximize.move(self.width() - (2 * self.button_width), 0)
        self.button_maximize.resize(self.button_width, self.title_bar_height)

        # minimize button
        self.button_minimize.move(self.width() - (3 * self.button_width), 0)
        self.button_minimize.resize(self.button_width, self.title_bar_height)

        # top
        self.widget_resize_top.move(self.widget_resize_size, 0)
        self.widget_resize_top.resize(self.width() - (2 * self.widget_resize_size), self.widget_resize_size)

        # bottom
        self.widget_resize_bottom.move(self.widget_resize_size, self.height() - self.widget_resize_size)
        self.widget_resize_bottom.resize(self.width() - (2 * self.widget_resize_size), self.widget_resize_size)

        # left
        self.widget_resize_left.move(0, self.widget_resize_size)
        self.widget_resize_left.resize(self.widget_resize_size, self.height() - (2 * self.widget_resize_size))

        # right
        self.widget_resize_right.move(self.width() - self.widget_resize_size, self.widget_resize_size)
        self.widget_resize_right.resize(self.widget_resize_size, self.height() - (2 * self.widget_resize_size))

        # top left
        self.widget_resize_top_left.move(0, 0)
        self.widget_resize_top_left.resize(self.widget_resize_size, self.widget_resize_size)

        # top right
        self.widget_resize_top_right.move(self.width() - self.widget_resize_size, 0)
        self.widget_resize_top_right.resize(self.widget_resize_size, self.widget_resize_size)

        # bottom left
        self.widget_resize_bottom_left.move(0, self.height() - self.widget_resize_size)
        self.widget_resize_bottom_left.resize(self.widget_resize_size, self.widget_resize_size)

        # bottom right
        self.widget_resize_bottom_right.move(self.width() - self.widget_resize_size,
                                             self.height() - self.widget_resize_size)
        self.widget_resize_bottom_right.resize(self.widget_resize_size, self.widget_resize_size)

        # text box
        self.box_text.move(self.box_padding, self.box_padding + self.title_bar_height)
        self.box_text.resize(int((self.width() * (2 / 5)) - (self.box_padding * 1.5)),
                             self.height() - self.box_answer_height - (
                                     self.box_padding * 3) - self.title_bar_height)  # 1.5 is used so the gap to the right of the box isn't too big

        # answer box
        self.box_answer.move(self.box_padding, self.height() - self.box_padding - 80)
        self.box_answer.resize(int((self.width() * (2 / 5)) - (self.box_padding * 1.5)), self.box_answer_height)

        # answer format label
        self.box_answer_format_label.move(self.box_padding + 12, self.height() - self.box_padding - 80)

        # definition box
        self.scroll_area.move((self.box_padding * 2) + int((self.width() * (2 / 5)) - (self.box_padding * 1.5)),
                              self.box_padding + self.title_bar_height)
        self.scroll_area.resize(int((self.width() * (3 / 5)) - (self.box_padding * 1.5)),
                                self.height() - (self.box_padding * 2) - self.title_bar_height)


def main():
    app = QApplication(sys.argv)

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
