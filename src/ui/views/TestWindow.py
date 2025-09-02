from PyQt6 import QtWidgets

from core.style import Settings, Style
from core.system_settings import OperatingSystem
from ui.views.ControlWindow import ControlWindow


class TestWindow(ControlWindow):  # buttons, and functions for testing purposes
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        ControlWindow.__init__(self, settings, style, op)
        self.__setup()

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
        self._set_geometry(*size_start)
        self._set_size_min(350, 130)

        # Layout ------------------------------------------------------------------------------------------------

        self.__box_buttons = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(self.__box_buttons)

        # Buttons -----------------------------------------------------------------------------------------------

        self.__buttons = []  # holds all testing buttons

        # update button
        self.__buttons.append(QtWidgets.QPushButton("Update"))
        layout.addWidget(self.__buttons[-1])

        # size button
        self.__buttons.append(QtWidgets.QPushButton("Size"))
        self.__buttons[-1].clicked.connect(self.__get_info)
        layout.addWidget(self.__buttons[-1])

        # test button
        self.__button_test_toggle = False
        self.__buttons.append(QtWidgets.QPushButton("Test"))
        self.__buttons[-1].clicked.connect(self.__test)
        layout.addWidget(self.__buttons[-1])

        self._style.init_test_buttons(self.__buttons)  # initializes all buttons

    def __update_colors(self) -> None:
        """
        Updates the stylesheets of everything in TestWindow.
        """

        self.repaint()  # updates the colors for the title bar and background
        self._update_colors_control()

        self._style.set_test_box_buttons(self.__box_buttons)

    def __update_self(self) -> None:
        """
        Updates the position of everything in TestWindow.
        """

        self.__box_buttons.move(self._settings_user.box_padding, self._settings_user.title_bar_height + self._settings_user.box_padding)
        self.__box_buttons.resize(self.width() - (self._settings_user.box_padding * 2), self.height() - self._settings_user.title_bar_height - (self._settings_user.box_padding * 2))

    def __test(self) -> None:
        """
        Used for testing anything in the window.
        """

        print("Test Button")

    def __get_info(self) -> None:
        """
        Prints the current width and height of the window with the use of a button.
        """

        print(f"Width: {self.width()}, Height: {self.height()}")

    def resizeEvent(self, event):
        self._update_control()
        self.__update_self()
