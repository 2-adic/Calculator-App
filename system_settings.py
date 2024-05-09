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

    def enable_blur(self, window):
        if self.system_name == 'Windows':

            hwnd = window.windowHandle().winId().__int__()  # Obtain the HWND

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
