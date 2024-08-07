from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QProxyStyle, QStyle, QLineEdit, QApplication, QPlainTextEdit
from PyQt6.QtGui import QIcon, QColor, QPainter
from PyQt6.QtCore import Qt, QSize, QTimer, QRect, pyqtProperty


class WrapTextButton:
    def __init__(self, text, parent=None, gap: int = 8):

        self.__button = QPushButton()
        self.__button.setParent(parent)
        self.__button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.__label = QLabel(text, self.__button)
        self.__label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.__label.setWordWrap(True)
        self.__label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__label.setMouseTracking(False)

        self.__button.setLayout(QVBoxLayout())
        self.__button.layout().setContentsMargins(gap, gap, gap, gap)
        self.__button.layout().addWidget(self.__label)

    def get_button(self) -> QPushButton:
        """
        Returns the QPushButton.
        """

        return self.__button

    def get_label(self) -> QLabel:
        """
        Returns the QLabel.
        """

        return self.__label

    def text(self) -> str:
        """
        Returns the button's text as a string.
        """

        return self.__label.text()

    def setText(self, new_string: str) -> None:
        """
        Changes the text of the button.
        """

        self.__label.setText(new_string)

    def setIcon(self, icon: QIcon) -> None:
        """
        Sets the icon of the button to the given QIcon.
        """

        self.__button.setIcon(icon)

    def setIconSize(self, size: QSize):
        self.__button.setIconSize(size)

    def setCursor(self, cursor: Qt.CursorShape) -> None:
        """
        Sets the cursor which appears when hovering over the button.
        """

        self.__button.setCursor(cursor)

    def move(self, x: int, y: int) -> None:
        self.__button.move(x, y)

    def resize(self, w: int, h: int) -> None:
        self.__button.resize(w, h)


class CustomCaretLineEditStyle(QProxyStyle):
    def pixelMetric(self, pm, opt=None, widget=None):
        if (
            pm == QStyle.PixelMetric.PM_TextCursorWidth and opt
            and isinstance(opt.styleObject, CustomCaretLineEdit)
            and opt.styleObject.property('customCaret')
        ):
            return 0
        return super().pixelMetric(pm, opt, widget)


class CustomCaretLineEdit(QLineEdit):
    # default values
    __caret_size = -1
    __caret_color = QColor(255, 255, 255)  # the active color of the caret
    __background_color = QColor(0, 0, 0)  # background color to hide the caret

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyle(CustomCaretLineEditStyle())
        self.__blink_timer = QTimer(self, timeout=self.__toggle_caret_color, interval=QApplication.styleHints().cursorFlashTime() // 2)
        self.__current_color = self.__background_color

    @pyqtProperty(int)
    def caret_size(self):
        return self.__caret_size

    @caret_size.setter
    def caret_size(self, size):
        if size < 0:
            size = -1
        if self.__caret_size != size:
            self.__caret_size = size
            self.update()

    @pyqtProperty(QColor)
    def caret_color(self):
        return self.__caret_color

    @caret_color.setter
    def caret_color(self, color: QColor):
        self.__caret_color = color
        self.update(self.cursorRect())

    @pyqtProperty(QColor)
    def background_color(self):
        return self.__background_color

    @background_color.setter
    def background_color(self, color: QColor):
        self.__background_color = color
        self.__current_color = self.__background_color
        self.update(self.cursorRect())

    def __toggle_caret_color(self):
        # toggles between the caret color and the background color
        if self.__current_color == self.__background_color:
            self.__current_color = self.__caret_color  # set to visible color
        else:
            self.__current_color = self.__background_color  # set to background color to hide
        self.update(self.cursorRect())

    def focusInEvent(self, event):
        super().focusInEvent(event)

        self.__current_color = self.__caret_color  # makes caret visible immediately
        self.update(self.cursorRect())  # updates the caret to show the color

        self.__blink_timer.start()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.__blink_timer.stop()
        self.__current_color = self.__background_color  # makes caret invisible on focus loss
        self.update()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.__current_color = self.__caret_color   # makes caret visible after a key press
        self.__blink_timer.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.__caret_size > 0:
            qp = QPainter(self)
            full_rect = self.cursorRect()
            x = full_rect.x() + round(full_rect.width() / 2) - round(self.__caret_size / 2)
            cr = QRect(x, full_rect.y(), max(1, self.__caret_size), self.fontMetrics().height())
            qp.fillRect(cr, self.__current_color)


class CustomCaretTextEditStyle(QProxyStyle):
    def pixelMetric(self, pm, opt=None, widget=None):
        if (
            pm == QStyle.PixelMetric.PM_TextCursorWidth and opt
            and isinstance(opt.styleObject, CustomCaretTextEdit)
            and opt.styleObject.property('customCaret')
        ):
            return 0
        return super().pixelMetric(pm, opt, widget)


class CustomCaretTextEdit(QPlainTextEdit):
    # default values
    __caret_size = -1
    __caret_color = QColor(255, 255, 255)  # the active color of the caret
    __background_color = QColor(0, 0, 0)  # background color to hide the caret

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyle(CustomCaretTextEditStyle())
        self.__blink_timer = QTimer(self, timeout=self.__toggle_caret_color, interval=QApplication.styleHints().cursorFlashTime() // 2)
        self.__current_color = self.__background_color

    @pyqtProperty(int)
    def caret_size(self):
        return self.__caret_size

    @caret_size.setter
    def caret_size(self, size):
        if size < 0:
            size = -1
        if self.__caret_size != size:
            self.__caret_size = size
            self.update()

    @pyqtProperty(QColor)
    def caret_color(self):
        return self.__caret_color

    @caret_color.setter
    def caret_color(self, color: QColor):
        self.__caret_color = color
        self.update(self.cursorRect())

    @pyqtProperty(QColor)
    def background_color(self):
        return self.__background_color

    @background_color.setter
    def background_color(self, color: QColor):
        self.__background_color = color
        self.__current_color = self.__background_color
        self.update(self.cursorRect())

    def __toggle_caret_color(self):
        # toggles between the caret color and the background color
        if self.__current_color == self.__background_color:
            self.__current_color = self.__caret_color  # sets to visible color
        else:
            self.__current_color = self.__background_color  # sets to background color to hide
        self.update(self.cursorRect())

    def focusInEvent(self, event):
        super().focusInEvent(event)

        self.__current_color = self.__caret_color  # makes caret visible immediately
        self.update(self.cursorRect())  # updates the caret to show the color

        self.__blink_timer.start()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.__blink_timer.stop()
        self.__current_color = self.__background_color  # makes caret invisible on focus loss
        self.update()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.__current_color = self.__caret_color   # makes caret visible after a key press
        self.__blink_timer.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.__caret_size > 0:
            qp = QPainter(self.viewport())
            full_rect = self.cursorRect()
            x = full_rect.x() + round(full_rect.width() / 2) - round(self.__caret_size / 2)
            cr = QRect(x, full_rect.y(), max(1, self.__caret_size), self.fontMetrics().height())
            qp.fillRect(cr, self.__current_color)
