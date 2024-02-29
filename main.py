import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QLineEdit, QVBoxLayout, QPlainTextEdit, QScrollArea, QHBoxLayout, QFrame
from PyQt5.QtGui import QColor, QPainter, QIcon, QFont
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSlot, QTimer
import sympy as sy
from pyperclip import copy
from sortedcontainers import SortedDict

# needs shadowing for the sides of the window
# add a settings section
'''
* option to toggle commas; 1,000,000 <-> 1000000
* option to toggle between radians and degrees
'''
# numbers that are given as a decimal are turned into a long expansion of zeros
'''
Ex: 1.1 -> 1.10000000000000000000
Fix:
* turn all decimals given in the text box, into fractions before the answer is calculated
    * to do this scan the text and when a number is found,
    
'''
# fractions that are turned into a decimal and then turned back into a fraction aren't the same
'''
Fix:
* save the original fraction and display it when the user flips the answer back to a fraction
'''
# change all text highlight color to the same color by making it the default
# also make the text highlight color change colors when you click off the area
# add functionality so when the user puts the window to the side of their screen, they can full-screen it

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window ------------------------------------------------------------------------------------------------
        self.setGeometry(100, 100, 800, 600)  # initial window size / position
        self.setWindowTitle("Calculator")  # window title
        self.setWindowFlags(Qt.FramelessWindowHint)  # removes default title bar

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
        self.button_close.setIcon(QIcon('C:\\Users\\mglin\\PycharmProjects\\Apps\\Window\\Math App\\external\\button_close_icon.png'))
        self.button_close.setStyleSheet(
            "QPushButton { background-color: transparent; color: rgb(181, 186, 193); border: none; font-size: 11px;}"
            "QPushButton:hover { background-color: rgb(242, 63, 66); border: none; }"
        )
        self.button_close.clicked.connect(self.button_close_logic)

        # maximize button
        self.button_maximize = QPushButton('', self)
        self.button_maximize.setIcon(QIcon('C:\\Users\\mglin\\PycharmProjects\\Apps\\Window\\Math App\\external\\button_maximize_icon.png'))
        self.button_maximize.setStyleSheet(
            "QPushButton { background-color: transparent; color: rgb(181, 186, 193); border: none; font-weight: bold; font-size: 11px;}"
            "QPushButton:hover { background-color: rgb(45, 46, 51); border: none; }"
        )
        self.button_maximize.clicked.connect(self.button_maximize_logic)

        # minimize button
        self.button_minimize = QPushButton('', self)
        self.button_minimize.setIcon(QIcon('C:\\Users\\mglin\\PycharmProjects\\Apps\\Window\\Math App\\external\\button_minimize_icon.png'))
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
        self.button_update.setCursor(Qt.PointingHandCursor)
        self.test_counter += 1
        '''

        # answer button
        self.button_answer = QPushButton('Answer', self)
        self.button_answer.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
        self.button_answer.setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_answer.clicked.connect(self.get_answer)
        self.button_answer.setCursor(Qt.PointingHandCursor)
        self.test_counter += 1

        # flip button
        self.button_flip = QPushButton('Flip', self)
        self.button_flip.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
        self.button_flip.setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_flip.clicked.connect(self.flip_type)
        self.button_flip.setCursor(Qt.PointingHandCursor)
        self.test_counter += 1

        '''
        # test button
        self.button_test = QPushButton('Test', self)
        self.button_test.setGeometry(self.test_horizontal_offset + (self.test_counter * self.test_between_spacing), self.test_padding, self.test_button_width - (2 * self.test_padding), self.title_bar_height - (2 * self.test_padding))
        self.button_test.setStyleSheet('background-color: None; color: rgb(148, 155, 164); border: 1px solid rgb(148, 155, 164); border-radius: 4px;')
        self.button_test.clicked.connect(self.test)
        self.button_test.setCursor(Qt.PointingHandCursor)
        self.test_counter += 1
        '''
        # -------------------------------------------------------------------------------------------------------

        # Resizing Widgets --------------------------------------------------------------------------------------
        self.window_resize = False  # initial state of resizing
        self.window_resize_direction = None  # initial direction of resizing
        self.widget_resize_toggle = True

        # top
        self.widget_resize_top = QWidget(self)
        self.widget_resize_top.setCursor(Qt.SizeVerCursor)

        # bottom
        self.widget_resize_bottom = QWidget(self)
        self.widget_resize_bottom.setCursor(Qt.SizeVerCursor)

        # left
        self.widget_resize_left = QWidget(self)
        self.widget_resize_left.setCursor(Qt.SizeHorCursor)

        # right
        self.widget_resize_right = QWidget(self)
        self.widget_resize_right.setCursor(Qt.SizeHorCursor)

        # top left
        self.widget_resize_top_left = QWidget(self)
        self.widget_resize_top_left.setCursor(Qt.SizeFDiagCursor)

        # top right
        self.widget_resize_top_right = QWidget(self)
        self.widget_resize_top_right.setCursor(Qt.SizeBDiagCursor)

        # bottom left
        self.widget_resize_bottom_left = QWidget(self)
        self.widget_resize_bottom_left.setCursor(Qt.SizeBDiagCursor)

        # bottom right
        self.widget_resize_bottom_right = QWidget(self)
        self.widget_resize_bottom_right.setCursor(Qt.SizeFDiagCursor)
        # -------------------------------------------------------------------------------------------------------

        # answer box
        self.answer = 'N/A'

        self.box_answer_height = 80
        self.box_answer = QPushButton('Answer', self)
        self.box_answer.setStyleSheet('border: 3px solid rgb(35, 36, 40); background-color: rgb(85, 88, 97); border-radius: 6px; color: white; font-size: 15px;')
        self.box_answer.clicked.connect(self.copy)

        # text box
        self.box_padding = 20

        self.variables_accepted = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.variables = SortedDict()  # stores variables in a sorted dictionary, so it shows in alphabetical order

        # Create a QLineEdit with initial position (150, 50)
        self.box_text = QPlainTextEdit(self)
        self.box_text.textChanged.connect(self.text_update)

        palette = self.box_text.palette()
        palette.setColor(palette.Highlight, QColor(70, 115, 156))  # Set highlight color to red
        self.box_text.setPalette(palette)

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

        # scroll area
        self.scroll_layout = QVBoxLayout()
        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        '''
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
         '''
        # if many variables are deleted at once, some of them stay in the definitions area
        # DELETE ONCE YOU FIND OUT THE SPACING CAUSE RN THEY ARE TOO SPACED OUT WHEN THERE ARE A FEW OF THEM -----
        # keep the main window, cause there is an error without it
        # also delete the try: except:
        '''
        self.textbox = []

        for i in range(3):  # Add some labels for demonstration

            layout = QHBoxLayout()

            label = QLabel(f'x =', self)

            self.textbox.append(QLineEdit(self))
            self.textbox[i].setPlaceholderText('Enter value')

            layout.addWidget(label)
            layout.addWidget(self.textbox[i])

            self.scroll_layout.addLayout(layout)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet(f"background-color: #313338; border-radius: 1px")

            self.scroll_layout.addWidget(line)

        self.scroll_layout.addStretch()
        '''
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

    def test(self):

        for x in self.variables:
            print(self.variables[x][1].text())


    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # title bar
        painter.fillRect(0, 0, self.width(), self.title_bar_height, QColor(30, 31, 34))

        # center window
        painter.fillRect(0, self.title_bar_height, self.width(), self.height() - self.title_bar_height,
                         QColor(49, 51, 56))

    def get_info(self):
        print(f'Width: {self.width()}, Height: {self.height()}')

    def get_update(self):
        # this function only exits to print 'Manually Updated', instead of the button just using window_update()
        self.window_update()
        print('Manually Updated')

    def get_answer(self):
        # turns the textbox to a string
        text = self.box_text.toPlainText()

        # scans the text for any variables
        for x in text:
            if x in self.variables:
                test_variable = self.variables[x][1].text()

                if test_variable != '':
                    text = text.replace(f'{x}', f'({test_variable})')

        # tests if the user something wrong and outputs 'error' if so
        try:
            self.answer = sy.sympify(text)
            print(f'Answer: {text} = {self.answer}')
        except Exception as e:
            self.answer = 'Error'
            print(f'Error: {e}')

        self.box_answer.setText(f'{str(self.answer)}')

    def flip_type(self):

        if type(self.answer) == sy.core.numbers.Float:
            self.answer = sy.Rational(self.answer)
        elif type(self.answer) == sy.core.numbers.Rational:
            self.answer = sy.Float(self.answer)

        self.box_answer.setText(f'{str(self.answer)}')

    def copy(self):
        self.box_answer.setStyleSheet(
            'border: 3px solid rgb(35, 36, 40); background-color: rgb(81, 100, 117); border-radius: 6px; color: white; font-size: 15px;')
        QTimer.singleShot(150, lambda: self.box_answer.setStyleSheet(
            'border: 3px solid rgb(35, 36, 40); background-color: rgb(85, 88, 97); border-radius: 6px; color: white; font-size: 15px;'))

        # crashes to this when it is set to an actual number
        copy(str(self.answer))

    def text_update(self):
        text = self.box_text.toPlainText()

        temp = set()  # used later for deleting variables in self.variables which are not in the text box

        # adds all variables to a dictionary
        for x in text:
            if x in self.variables_accepted:
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

        self.scroll_area_clear()

        self.scroll_area_fill()


    def scroll_area_fill(self):
        # this is for when you delete the main layout in the scroll_area_clear

        for x in self.variables:

            layout = QHBoxLayout()
            layout.addWidget(self.variables[x][0])
            layout.addWidget(self.variables[x][1])

            self.scroll_layout.addLayout(layout)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet(f"background-color: #313338; border-radius: 1px")

            self.scroll_layout.addWidget(line)

        self.scroll_layout.addStretch()

    def scroll_area_clear(self):
        for i in reversed(range(self.scroll_layout.count())):
            layout_item = self.scroll_layout.itemAt(i)

            if layout_item.widget():
                widget_to_remove = layout_item.widget()
                self.scroll_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)
            elif layout_item.layout():
                self.clear_inner_layout(layout_item.layout())
            elif layout_item.spacerItem():
                # If the item is a spacer, remove it from the layout
                self.scroll_layout.removeItem(layout_item)

    def clear_inner_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                # Check if the widget is QLabel or QLineEdit and should be kept
                if isinstance(widget, (QLabel, QLineEdit)) and widget in [w for v in self.variables.values() for w in
                                                                          v]:
                    layout.removeWidget(widget)
                    widget.setParent(None)
                else:
                    widget.deleteLater()
            elif item.layout():
                # Recursively clear nested layouts
                self.clear_inner_layout(item.layout())

    def button_close_logic(self):
        # logic before closing goes here (checks if work is saved, etc.)

        exit()  # instantly exits the program

    def button_maximize_logic(self):
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

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.window_moving = False
            self.window_resize = False

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.offset = event.pos()

            # Moving Window
            self.window_moving = False
            if self.widget_move.rect().contains(self.widget_move.mapFrom(self, self.offset)):
                self.window_moving = True
                self.offset = event.globalPos() - self.pos()
                return

            # if self.widget_resize_size < event.y() < self.title_bar_height and self.widget_resize_size < event.x() < self.width() - self.widget_resize_size:
            #     self.window_moving = True
            #     self.offset = event.globalPos() - self.pos()
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

    def mouseMoveEvent(self, event):
        # Moving Window
        if self.window_moving:

            # exits the maximized setting
            if self.isMaximized():

                offset_x = min(int(self.normalGeometry().width() * (self.offset.x() / self.width())), self.normalGeometry().width() - (3 * self.button_width))
                self.offset = QPoint(offset_x, self.offset.y())

                self.button_maximize_logic()

                mouse_position = event.globalPos() - self.offset

            else:
                mouse_position = event.globalPos() - self.offset

            self.move(mouse_position)


        # Resizing Widgets
        elif self.window_resize:

            # top (needs work)
            if self.window_resize_direction == 0:
                temp_event_y = event.y()

                window_resize_move_y = self.height() - temp_event_y
                if window_resize_move_y >= self.window_size_min_y:
                    self.move(self.x(), self.y() + temp_event_y)
                    self.resize(self.width(), window_resize_move_y)
                    self.window_update()

            # bottom
            elif self.window_resize_direction == 1:
                window_resize_move_y = event.y()
                if window_resize_move_y >= self.window_size_min_y:
                    self.resize(self.width(), window_resize_move_y)
                    self.window_update()

            # left (needs work)
            elif self.window_resize_direction == 2:
                temp_event_x = event.x()

                window_resize_move_x = self.width() - temp_event_x
                if window_resize_move_x >= self.window_size_min_x:
                    self.move(self.x() + temp_event_x, self.y())
                    self.resize(window_resize_move_x, self.height())
                    self.window_update()

            # right
            elif self.window_resize_direction == 3:
                window_resize_move_x = event.x()
                if window_resize_move_x >= self.window_size_min_x:
                    self.resize(window_resize_move_x, self.height())
                    self.window_update()

            # top left (needs major work)
            elif self.window_resize_direction == 4:
                temp_event_x = event.x()
                temp_event_y = event.y()
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
                temp_event_y = event.y()
                temp_height = self.height()

                window_resize_move_x = event.x()
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
                temp_event_x = event.x()
                temp_width = self.width()

                window_resize_move_x = temp_width - temp_event_x
                window_resize_move_y = event.y()
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

                window_resize_move_x = max(self.window_size_min_x, event.x())
                window_resize_move_y = max(self.window_size_min_y, event.y())
                self.resize(window_resize_move_x, window_resize_move_y)

                self.window_update()

    def window_update(self):
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
        self.widget_resize_bottom_right.move(self.width() - self.widget_resize_size, self.height() - self.widget_resize_size)
        self.widget_resize_bottom_right.resize(self.widget_resize_size, self.widget_resize_size)

        # text box
        self.box_text.move(self.box_padding, self.box_padding + self.title_bar_height)
        self.box_text.resize(int((self.width() * (2/5)) - (self.box_padding * 1.5)), self.height() - self.box_answer_height - (self.box_padding * 3) - self.title_bar_height)  # 1.5 is used so the gap to the right of the box isn't too big

        # answer box
        self.box_answer.move(self.box_padding, self.height() - self.box_padding - 80)
        self.box_answer.resize(int((self.width() * (2/5)) - (self.box_padding * 1.5)), self.box_answer_height)

        # definition box
        self.scroll_area.move((self.box_padding * 2) + int((self.width() * (2 / 5)) - (self.box_padding * 1.5)), self.box_padding + self.title_bar_height)
        self.scroll_area.resize(int((self.width() * (3 / 5)) - (self.box_padding * 1.5)), self.height() - (self.box_padding * 2) - self.title_bar_height)


def main():
    app = QApplication(sys.argv)

    font = QFont('Consolas', 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
