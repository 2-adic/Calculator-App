from PyQt6 import QtGui, QtWidgets
import sys

from core.files import path
import core.font_control as font_control
from core.style import Settings, Style
from core.system_settings import OperatingSystem
from ui.views.MainWindow import MainWindow
from ui.views.SettingsWindow import SettingsWindow
from ui.views.TestWindow import TestWindow


class RunWindow:
    def __init__(self, is_test_included: bool = False):
        self.__is_test_included = is_test_included  # excludes the test window by default
        self.__init_app()

    def start(self) -> None:
        sys.exit(self.__app.exec())

    def __init_app(self) -> None:
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__app.setQuitOnLastWindowClosed(True)
        self.__init_icons()
        self.__init_font()
        self.__init_windows()

    def __init_icons(self) -> None:
        # sets the icon for the app
        self.__app.setWindowIcon(QtGui.QIcon(path("assets/icons/taskbar_icon_16px.png")))

    def __init_font(self) -> None:
        """
        Initializes the default font.
        """

        # attempts to find font, default system font used if none was found
        try:
            font_control.font_set(self.__app, font_control.font_default, font_control.font_size_default)
        except Exception as e:
            print(f"{e}")
            
    def __init_windows(self) -> None:
        """
        Initializes the windows and their settings.
        """

        # initializes classes that are shared between the windows
        settings = Settings()
        style = Style(settings)
        op = OperatingSystem()

        # initializes the windows
        self.__window_settings = SettingsWindow(settings, style, op)
        self.__window_main = MainWindow(settings, style, op)
        if self.__is_test_included:
            self.__window_test = TestWindow(settings, style, op)

        # initializes connections / settings
        self.__init_buttons()
        self.__update_settings()

        # displays the windows
        self.__window_main.show()
        if self.__is_test_included:
            self.__window_test.show()

    def __init_buttons(self) -> None:
        """
        Initializes buttons that are used to control multiple windows.
        """

        self.__window_main.connect_button_settings(self.__open_settings)
        self.__window_settings.connect_button_apply(self.__update_settings)
        if self.__is_test_included:
            self.__window_test.connect_button_update(self.__update_settings)

    def __open_settings(self) -> None:
        """
        Opens the settings window in front of the main window.
        """

        position = self.__window_main.pos().x() + 40, self.__window_main.pos().y() + 30
        self.__window_settings.open_window(position)

    def __update_settings(self) -> None:
        """
        Updates the settings for all windows.
        """

        self.__window_settings.update_settings()
        self.__window_main.update_settings()
        if self.__is_test_included:
            self.__window_test.update_settings()
