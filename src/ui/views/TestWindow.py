from PyQt6 import QtGui, QtWidgets

from core.style import Settings, Style
from core.system_settings import OperatingSystem
from ui.common.CaretLineEdit import CaretLineEdit
from ui.common.HorizontalButtonGroup import HorizontalButtonGroup
from ui.views.ControlWindow import ControlWindow
from ui.views.Sidebar import Sidebar

from core.functions import Solve


class TestWindow(ControlWindow):  # buttons, and functions for testing purposes
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        ControlWindow.__init__(self, settings, style, op)
        self.__setup()

        self.__sidebar = Sidebar(self._settings_user, self._style, self._op, self.__line_edit, self)

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

        self.__sidebar.update_colors()

    def __update_self(self) -> None:
        """
        Updates the position of everything in TestWindow.
        """

        self.__box_buttons.move(self._settings_user.box_padding, self._settings_user.title_bar_height + self._settings_user.box_padding)
        # limit the width to half the window width minus padding
        max_width = (self.width() // 2) - self._settings_user.box_padding
        button_box_width = min(max_width, self.width() - (self._settings_user.box_padding * 2))
        self.__box_buttons.resize(button_box_width, self.height() - self._settings_user.title_bar_height - (self._settings_user.box_padding * 2))

        # sidebar
        self.__sidebar.resize(int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)), self.height() - (self._settings_user.title_bar_height + (self._settings_user.box_padding * 2)))
        self.__sidebar.move((self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height)

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
            solution = Solve(text, self.__sidebar.terms(), self._settings_user.answer_display, self._settings_user.answer_copy, self._settings_user.use_commas, self._settings_user.color_latex, self._settings_user.latex_image_dpi)
            solution.print()
            print(solution.get_variables())
            print(solution.get_constants())
        except Exception as error:
            print(f"Error: {error}")

    def __print_info(self) -> None:
        print(self.__sidebar.terms())

    def resizeEvent(self, event):
        self._update_control()
        self.__update_self()
