from copy import deepcopy
import pyperclip
from PyQt6 import QtCore, QtGui, QtWidgets

from core.style import Settings, Style
import core.symbols as symbols
from core.system_settings import OperatingSystem
from ui.common.CaretLineEdit import CaretLineEdit
from ui.common.HorizontalButtonGroup import HorizontalButtonGroup
from ui.common.VerticalPageSelector import VerticalPageSelector
from ui.components.PageNotation import PageNotation
from ui.components.PageTerms import PageTerms
from ui.components.SectionGridButtons import SectionGridButtons
from ui.views.ControlWindow import ControlWindow

from core.functions import Solve


class TestWindow(ControlWindow):  # buttons, and functions for testing purposes
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        ControlWindow.__init__(self, settings, style, op)
        self.__setup()

        self.__init_page_selector()

    def __init_page_selector(self) -> None:

        # page selector

        self.__page_selector = VerticalPageSelector(self)
        n = 2
        for i in range(n):
            button = QtWidgets.QPushButton()
            button.setMinimumHeight(self._settings_user.select_height)
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.setCheckable(True)  # allows the button to be selected

            if i == 0:
                button.setText("Variables")
                button.setChecked(True)  # checks the first button by default

                widget = PageTerms(edit=self.__line_edit)
                self.__PageTerms = widget

            elif i == 1:
                button.setText("Notation")

                widget = PageNotation()

                self.__PageNotationSections: list[QtWidgets.QWidget] = widget.getSections()

                for j, section in enumerate(self.__PageNotationSections):
                    if isinstance(section, SectionGridButtons):

                        section.layout().setContentsMargins(0, 0, 0, 0)
                        section.connect(self.__copy_button_label)

                        section.setButtonHeight(self._settings_user.symbols_button_height)

                        if j == 0:

                            section.scrollArea().setMinimumHeight(self._op.get_notation_symbols_min_height())  # stops the top scroll area from becoming too collapsed

                            section.setButtonWidth(self._settings_user.symbols_button_width[0])

                        elif j == 1:
                            section.setButtonWidth(self._settings_user.symbols_button_width[1])

            elif i == 2:
                button.setText("Test")

                widget = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout(widget)
                label = QtWidgets.QLabel(f"Variables Page")
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            widget.layout().setContentsMargins(self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin)

            self.__page_selector.addPage(button, widget)

        self.__page_selector.layout().setSpacing(0)

    def __copy_button_label(self) -> None:
        button = self.sender()
        text = button.text()

        if text not in symbols.copy_notation[0]:  # adds parentheses to functions
            text += "()"

        pyperclip.copy(text)

    def update_settings(self) -> None:
        """
        Refreshes the windows to apply the new settings.
        """

        self.__update_colors()

    def connect_button_update(self, function) -> None:
        """
        Used to connect the update button to a function outside the class.
        """

        self.__buttons[0].clicked.connect(function)

    def __setup(self) -> None:

        self._set_title("Testing")

        size_start = self._settings_user.window_start_size_main[0] + self._settings_user.window_start_size_main[2] + 50, self._settings_user.window_start_size_main[1] + 70, 455, 169
        self._set_geometry(300, 200, self._settings_user.window_start_size_main[2], self._settings_user.window_start_size_main[3])
        self._set_size_min(*self._settings_user.window_size_min_main)

        # Layout ------------------------------------------------------------------------------------------------

        self.__box_buttons = QtWidgets.QWidget(self)
        
        # create a vertical layout for the button box to hold line edit and buttons
        self.__main_layout = QtWidgets.QVBoxLayout(self.__box_buttons)
        self.__main_layout.setContentsMargins(10, 10, 10, 5)  # more space around line edit
        self.__main_layout.setSpacing(10)  # more space between line edit and buttons
        
        # create the line edit first
        self.__line_edit = CaretLineEdit(self.__box_buttons, setText="", defaultText="Enter your input here...", tag="input")
        
        # create a widget to hold the horizontal button layout
        self.__button_container = QtWidgets.QWidget()
        self.__button_layout = HorizontalButtonGroup(self.__button_container)

        # Buttons -----------------------------------------------------------------------------------------------

        self.__buttons = []  # holds all testing buttons

        # answer button
        self.__buttons.append(QtWidgets.QPushButton("Answer"))
        self.__buttons[-1].clicked.connect(self.__answer)
        self.__button_layout.addWidget(self.__buttons[-1])

        # print button
        self.__buttons.append(QtWidgets.QPushButton("Print"))
        self.__buttons[-1].clicked.connect(self.__print_info)
        self.__button_layout.addWidget(self.__buttons[-1])

        # test button
        self.__buttons.append(QtWidgets.QPushButton("Test"))
        self.__buttons[-1].clicked.connect(self.__test)
        self.__button_layout.addWidget(self.__buttons[-1])

        self._style.init_test_buttons(self.__buttons)  # initializes all buttons
        
        # add line edit and button container to the main layout
        self.__main_layout.addWidget(self.__line_edit)
        self.__main_layout.addWidget(self.__button_container)

    def __update_colors(self) -> None:
        """
        Updates the stylesheets of everything in TestWindow.
        """

        self.repaint()  # updates the colors for the title bar and background
        self._update_colors_control()

        self._style.set_test_box_buttons(self.__box_buttons)

        # remove border and background from button container only (not affecting buttons)
        self.__button_container.setStyleSheet("""
            QWidget#buttonContainer {
                border: none;
                background-color: transparent;
            }
        """)
        self.__button_container.setObjectName("buttonContainer")

        # re-apply button styling to ensure buttons have their borders
        for button in self.__buttons:
            button.setStyleSheet(
            f"""
            QPushButton {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
                color: rgb{self._settings_user.color_text};
            }}
            QPushButton:hover {{
                background-color: rgb{self._settings_user.color_box_hover};
                padding-top: -{self._settings_user.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self._settings_user.color_box_selected};
            }}
            """
            )

        # line edit styling - apply CaretLineEdit styles
        self.__line_edit.caretColor = QtGui.QColor(*self._settings_user.color_line_secondary)
        self.__line_edit.caretSize = self._settings_user.caret_size
        
        # add border styling to the line edit
        self.__line_edit.setStyleSheet(f"""
            CaretLineEdit {{
                border: {self._settings_user.box_border}px solid rgb{self._settings_user.color_box_border};
                border-radius: {self._settings_user.box_border_radius}px;
                background-color: rgb{self._settings_user.color_box_background};
                color: rgb{self._settings_user.color_text};
                padding: 5px;
                selection-background-color: rgb{self._settings_user.color_text_highlight_active};
                selection-color: rgb{self._settings_user.color_text};
            }}
            CaretLineEdit:focus {{
                border: {self._settings_user.box_border + 1}px solid rgb{self._settings_user.color_line_secondary};
            }}
        """)

        # page selector
        for i, widget in enumerate(self.__page_selector.pages()):
            self._style.set_page_selector(widget)

        # selector buttons
        n = len(self.__page_selector.buttons())
        for i, button in enumerate(self.__page_selector.buttons()):
            self._style.set_selector(button, i, n)

        # page notation
        for i, section in enumerate(self.__PageNotationSections):
            if isinstance(section, SectionGridButtons):
                self._style.set_page_notation(section, section.scrollArea(), section.label(), section.line(), section.buttons())

        # page variables
        self._style.set_variables_page(self.__PageTerms)

    def __update_self(self) -> None:
        """
        Updates the position of everything in TestWindow.
        """

        self.__box_buttons.move(self._settings_user.box_padding, self._settings_user.title_bar_height + self._settings_user.box_padding)
        # limit the width to half the window width minus padding
        max_width = (self.width() // 2) - self._settings_user.box_padding
        button_box_width = min(max_width, self.width() - (self._settings_user.box_padding * 2))
        self.__box_buttons.resize(button_box_width, self.height() - self._settings_user.title_bar_height - (self._settings_user.box_padding * 2))

        # page selector
        self.__page_selector.resize(int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)), self.height() - (self._settings_user.title_bar_height + (self._settings_user.box_padding * 2)))
        self.__page_selector.move((self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height)

    def __test(self) -> None:
        """
        Used for testing anything in the window.
        """

        print("Hello World")

    def __get_info(self) -> None:
        """
        Prints the current width and height of the window with the use of a button.
        """

        print(f"Width: {self.width()}, Height: {self.height()}")

    def __answer(self):
        
        text = self.__line_edit.text()

        try:
            solution = Solve(text, self.__PageTerms.terms(), self._settings_user.answer_display, self._settings_user.answer_copy, self._settings_user.use_commas, self._settings_user.color_latex, self._settings_user.latex_image_dpi)
            solution.print()
            print(solution.get_variables())
            print(solution.get_constants())
        except Exception as error:
            print(f"Error: {error}")

    def __print_info(self) -> None:
        print(self.__PageTerms.terms())

    def resizeEvent(self, event):
        self._update_control()
        self.__update_self()
