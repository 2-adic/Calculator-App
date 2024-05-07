import platform
import ctypes
from PyQt6.QtCore import Qt


class OperatingSystem:
    def __init__(self):
        self.system_name = platform.system()

        if self.system_name == 'Windows':  # Windows

            # configures Windows to show the taskbar icon
            myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

            print('Operating system is Windows')

        elif self.system_name == 'Darwin':  # macOS
            print('Operating system is macOS')

        elif self.system_name == 'Linux':  # Linux
            print('Operating system is Linux')

        else:
            print('Operating system not recognized')

    def is_maximize_shortcut(self, event):

        if self.system_name == 'Windows':  # Windows
            return event.key() == Qt.Key.Key_F11

        elif self.system_name == 'Darwin':  # macOS
            return event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier) and event.key() == Qt.Key.Key_F

        elif self.system_name == 'Linux':  # Linux
            return False  # functionality not added yet

        else:
            return False  # operating system not recognized


