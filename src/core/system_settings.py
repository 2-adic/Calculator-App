from PyQt6.QtCore import Qt, QObject, QTimer
from PyQt6.QtGui import QKeyEvent
import platform
import ctypes
from PIL import Image
import io
import subprocess
import os


def get_system_info() -> tuple[str, str]:
    """
    Finds the OS name that the user is using.
    """

    name = platform.system()
    version = None

    # gets the version of Windows
    if name == "Windows":
        version = platform.version()
        build_number = int(version.split('.')[2])

        if build_number >= 10240:
            version = "10"

        elif build_number >= 22000:
            version = "11"

    return name, version


system_name, system_version = get_system_info()  # gets the system name and version


def get_data_path(file_name: str | None):
    """
    Used to get the path to files which need permissions to use.
    """

    app_name = "Calculator App"

    if system_name == "Windows":
        app_data_folder = os.path.join(os.environ["APPDATA"], app_name)
        if not os.path.exists(app_data_folder):
            os.makedirs(app_data_folder)

    elif system_name == "Darwin":
        home = os.path.expanduser('~')
        app_data_folder = os.path.join(home, "Library", "Application Support", app_name)
        if not os.path.exists(app_data_folder):
            os.makedirs(app_data_folder)

    else:
        print("Folder not set.")
        return None

    return os.path.join(app_data_folder, file_name)


class OperatingSystem:
    def __init__(self):

        self.__set_system_info()
        self.__print_system_name()
        self.__show_taskbar_icon()

    def get_system_name(self) -> str:
        """
        Returns the OS name that the user is using.
        """

        return self.__system_name

    def get_scroll_bar_variable_height(self) -> int:
        """
        Returns the scroll bar height created per variable in the variables tab. This depends on the OS the user is on.
        """

        if self.__system_name == "Windows":
            height = 37

        elif self.__system_name == "Darwin":
            height = 49

        else:
            height = 40

        return height

    def get_notation_symbols_min_height(self) -> int:
        """
        Returns the minimum height of the symbols scroll area in the notations tab.
        """

        if self.__system_name == "Windows":
            height = 86

        elif self.__system_name == "Darwin":
            height = 98

        else:
            height = 86

        return height

    def get_window_border_radius(self) -> int:
        """
        Returns how curved the windows should be depending on the OS.
        """

        if self.__system_name == "Windows" and self.__system_version == "11":
            radius = 10

        elif self.__system_name == "Darwin":
            radius = 10

        else:
            radius = 0

        return radius

    def copy_image(self, file_path):
        """
        Copies a png image to the clipboard.
        """

        if self.__system_name == "Windows":

            import win32clipboard as clp

            image = Image.open(file_path)

            # converts the image to a png
            output_png = io.BytesIO()
            image.save(output_png, format="PNG")
            png_data = output_png.getvalue()

            # convert the image to DIB
            output_dib = io.BytesIO()
            image.convert("RGB").save(output_dib, format="BMP")
            dib_data = output_dib.getvalue()[14:]  # skips the first 14 bytes which removes the header

            # copies the png to the clipboard
            clp.OpenClipboard()
            clp.EmptyClipboard()
            clp.SetClipboardData(clp.RegisterClipboardFormat("PNG"), png_data)  # sets the PNG format
            clp.SetClipboardData(clp.CF_DIB, dib_data)  # sets the DIB format
            clp.CloseClipboard()

        elif self.__system_name == "Darwin":
            image = Image.open(file_path)
            output_path = "/tmp/temp_image.png"
            image.save(output_path)

            # uses AppleScript to copy the image to the clipboard as a file reference
            script = f"set the clipboard to (read (POSIX file \"{output_path}\") as «class PNGf»)"
            subprocess.run(["osascript", "-e", script])

    def is_maximize_shortcut(self, event):

        if self.__system_name == "Windows":  # Windows
            return event.key() == Qt.Key.Key_F11

        # macOS's full screen shortcut is detected through the MacOSEventFilter class

        elif self.__system_name == "Linux":  # Linux
            return False  # functionality not added yet

        else:
            return False  # operating system not recognized

    def enable_blur(self, window):
        if self.__system_name == "Windows":

            hwnd = window.windowHandle().winId().__int__()  # obtains the HWND

            class ACCENT_POLICY(ctypes.Structure):
                _fields_ = [("AccentState", ctypes.c_int),
                            ("AccentFlags", ctypes.c_int),
                            ("GradientColor", ctypes.c_uint),
                            ("AnimationId", ctypes.c_uint)]

            class WINDOW_COMPOSITION_ATTRIBUTE_DATA(ctypes.Structure):
                _fields_ = [("Attribute", ctypes.c_int),
                            ("Data", ctypes.POINTER(ACCENT_POLICY)),
                            ("SizeOfData", ctypes.c_size_t)]

            accent = ACCENT_POLICY()
            accent.AccentState = 3  # ACCENT_ENABLE_BLURBEHIND=3
            accent.AccentFlags = 2  # draw all borders=2
            accent.GradientColor = 0  # transparent gradient color
            accent.AnimationId = 0  # no animation

            data = WINDOW_COMPOSITION_ATTRIBUTE_DATA()
            data.Attribute = 19  # WCA_ACCENT_POLICY
            data.Data = ctypes.pointer(accent)
            data.SizeOfData = ctypes.sizeof(accent)
            ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

    def __set_system_info(self):
        """
        Finds the OS name that the user is using.
        """

        self.__system_name = system_name
        self.__system_version = system_version

    def __print_system_name(self):
        """
        Prints the name of the OS. Used for testing purposes.
        """

        name = self.__system_name
        version = self.__system_version

        if name == "Darwin":
            name = "macOS"

        # adds the version if there is one
        if version is None:
            str_end = ''
        else:
            str_end = f" {version}"

        print(f"Operating system is {name}{str_end}")

    def __show_taskbar_icon(self):
        """
        Shows the app icon in the taskbar.
        """

        name = self.__system_name

        if name == "Windows":

            # configures Windows to show the taskbar icon
            myappid = u"mycompany.myproduct.subproduct.version"  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def set_fullscreen_function(self, window, function):
        if self.__system_name == "Darwin":
            self.filter = MacOSEventFilter()
            self.filter.set_function_fullscreen(function)
            window.installEventFilter(self.filter)

class MacOSEventFilter(QObject):

    def __init__(self):
        super().__init__()
        self.__trigger_fullscreen = True
        self.__function_fullscreen = lambda: None  # function does nothing until its defined

    def set_function_fullscreen(self, function) -> None:
        self.__function_fullscreen = function

    def __trigger_reset_fullscreen(self) -> None:
        self.__trigger_fullscreen = True

    def eventFilter(self, obj, event):

        # detects if a macOS user presses "control + command + f" to fullscreen the window
        if isinstance(event, QKeyEvent) and event.key() == 70 and event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier):
            if self.__trigger_fullscreen:  # uses a trigger as a cooldown before this can be activated again
                self.__trigger_fullscreen = False
                QTimer.singleShot(645, self.__trigger_reset_fullscreen)
                self.__function_fullscreen()

            return True  # event is handled

        return super().eventFilter(obj, event)  # propagates other events normally