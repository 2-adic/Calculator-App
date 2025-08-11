from PyQt6 import QtCore, QtWidgets, QtCore, QtGui


class WrapTextButton:
    def __init__(self, text: str | None = None, parent = None, gap: int = 8) -> None:
        """
        A button with the ability to textwrap.

        :param text: The text to be displayed on the button.
        :param parent: The parent of the button.
        :param gap: The gap between the icon and the edges of the button.
        """

        self.__button = QtWidgets.QPushButton()
        self.__button.setParent(parent)
        self.__button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.__label = QtWidgets.QLabel(text, self.__button)
        self.__label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.__label.setWordWrap(True)
        self.__label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label.setMouseTracking(False)

        self.__button.setLayout(QtWidgets.QVBoxLayout())
        self.__button.layout().setContentsMargins(gap, gap, gap, gap)
        self.__button.layout().addWidget(self.__label)
        
        self.__gap = gap
        self.__icon_aspect_ratio = None

    def button(self) -> QtWidgets.QPushButton:
        """
        Returns the QPushButton.
        """

        return self.__button

    def label(self) -> QtWidgets.QLabel:
        """
        Returns the QLabel.
        """

        return self.__label

    def text(self) -> str:
        """
        Returns the button's text as a string.
        """

        return self.__label.text()

    def width(self) -> int:
        """
        Returns the button's width.
        """

        return self.__button.width()

    def height(self) -> int:
        """
        Returns the button's height.
        """

        return self.__button.height()

    def iconSize(self) -> QtCore.QSize:
        """
        Returns the button's icon size.
        """

        return self.__button.iconSize()

    def setText(self, new_string: str) -> None:
        """
        Changes the text of the button.
        """

        self.__label.setText(new_string)

    def setIcon(self, icon: QtGui.QIcon, aspect_ratio: float | None = None) -> None:
        """
        Sets the icon of the button to the given QtGui.QIcon.
        """

        self.__button.setIcon(icon)

        if aspect_ratio is None:
            icon_size = self.__button.iconSize()
            self.__icon_aspect_ratio = icon_size.width() / icon_size.height()

        else:  # this is needed since on macOS the aspect ratio changes to 1:1
            self.__icon_aspect_ratio = aspect_ratio


    def setIconSize(self, size: QtCore.QSize) -> None:
        """
        Changes the size of the icon.
        """
        
        self.__button.setIconSize(size)

    def setCursor(self, cursor: QtCore.Qt.CursorShape) -> None:
        """
        Sets the cursor which appears when hovering over the button.
        """

        self.__button.setCursor(cursor)

    def move(self, x: int, y: int) -> None:
        """
        Moves the buttons to the given x and y position.
        """
        
        self.__button.move(x, y)

    def resize(self, w: int, h: int) -> None:
        """
        Resizes the button to the given width and height.
        """
        
        self.__button.resize(w, h)
        self.__resizeIcon()
        
    def __resizeIcon(self) -> None:
        """
        Updates the size of the icon based on the button's current size.
        """

        gap = self.__gap * 2

        button_aspect_ratio = (self.width() - gap) / (self.height() - gap)
        icon_aspect_ratio = self.__icon_aspect_ratio

        if icon_aspect_ratio is not None:
            if icon_aspect_ratio > button_aspect_ratio:  # changes the size based on max width size
                width = self.width() - gap
                height = int((icon_aspect_ratio ** -1) * width)

            else:  # changes the size based on max height size
                height = self.height() - gap
                width = int(icon_aspect_ratio * height)

            self.__button.setIconSize(QtCore.QSize(width, height))


# custom caret code adapted from musicamante at https://stackoverflow.com/questions/68769475/how-to-set-the-color-of-caret-blinking-cursor-in-qlineedit
# modified by removing default caret from the left of the new caret
class CustomCaretLineEditStyle(QtWidgets.QProxyStyle):
    def pixelMetric(self, pm, opt=None, widget=None) -> int:
        if (
            pm == QtWidgets.QStyle.PixelMetric.PM_TextCursorWidth and opt
            and isinstance(opt.styleObject, CustomCaretLineEdit)
            and opt.styleObject.property("customCaret")
        ):
            return 0
        return super().pixelMetric(pm, opt, widget)


class CustomCaretLineEdit(QtWidgets.QLineEdit):
    # default values
    __caret_size: int = -1
    __caret_color = QtGui.QColor(255, 255, 255)  # the active color of the caret
    __background_color = QtGui.QColor(0, 0, 0)  # background color to hide the caret

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyle(CustomCaretLineEditStyle())
        self.__blink_timer = QtCore.QTimer(self, timeout=self.__toggle_caret_color, interval=QtWidgets.QApplication.styleHints().cursorFlashTime() // 2)
        self.__current_color = self.__background_color

    @QtCore.pyqtProperty(int)
    def caret_size(self) -> int:
        return self.__caret_size

    @caret_size.setter
    def caret_size(self, size: int) -> None:
        if size < 0:
            size = -1
        if self.__caret_size != size:
            self.__caret_size = size
            self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def caret_color(self) -> QtGui.QColor:
        return self.__caret_color

    @caret_color.setter
    def caret_color(self, color: QtGui.QColor) -> None:
        self.__caret_color = color
        self.update(self.cursorRect())

    @QtCore.pyqtProperty(QtGui.QColor)
    def background_color(self) -> QtGui.QColor:
        return self.__background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self.__background_color = color
        self.__current_color = self.__background_color
        self.update(self.cursorRect())

    def __toggle_caret_color(self) -> None:
        # toggles between the caret color and the background color
        if self.__current_color == self.__background_color:
            self.__current_color = self.__caret_color  # set to visible color
        else:
            self.__current_color = self.__background_color  # set to background color to hide
        self.update(self.cursorRect())

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)

        self.__current_color = self.__caret_color  # makes caret visible immediately
        self.update(self.cursorRect())  # updates the caret to show the color

        self.__blink_timer.start()

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.__blink_timer.stop()
        self.__current_color = self.__background_color  # makes caret invisible on focus loss
        self.update()

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        self.__current_color = self.__caret_color   # makes caret visible after a key press
        self.__blink_timer.start()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if self.__caret_size > 0:
            qp = QtGui.QPainter(self)
            full_rect = self.cursorRect()
            x = full_rect.x() + round(full_rect.width() / 2) - round(self.__caret_size / 2)
            cr = QtCore.QRect(x, full_rect.y(), max(1, self.__caret_size), self.fontMetrics().height())
            qp.fillRect(cr, self.__current_color)


class CustomCaretTextEditStyle(QtWidgets.QProxyStyle):
    def pixelMetric(self, pm, opt=None, widget=None) -> int:
        if (
            pm == QtWidgets.QStyle.PixelMetric.PM_TextCursorWidth and opt
            and isinstance(opt.styleObject, CustomCaretTextEdit)
            and opt.styleObject.property("customCaret")
        ):
            return 0
        return super().pixelMetric(pm, opt, widget)


class CustomCaretTextEdit(QtWidgets.QPlainTextEdit):
    # default values
    __caret_size: int = -1
    __caret_color = QtGui.QColor(255, 255, 255)  # the active color of the caret
    __background_color = QtGui.QColor(0, 0, 0)  # background color to hide the caret

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyle(CustomCaretTextEditStyle())
        self.__blink_timer = QtCore.QTimer(self, timeout=self.__toggle_caret_color, interval=QtWidgets.QApplication.styleHints().cursorFlashTime() // 2)
        self.__current_color = self.__background_color

    @QtCore.pyqtProperty(int)
    def caret_size(self) -> int:
        return self.__caret_size

    @caret_size.setter
    def caret_size(self, size) -> None:
        if size < 0:
            size = -1
        if self.__caret_size != size:
            self.__caret_size = size
            self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def caret_color(self) -> QtGui.QColor:
        return self.__caret_color

    @caret_color.setter
    def caret_color(self, color: QtGui.QColor) -> None:
        self.__caret_color = color
        self.update(self.cursorRect())

    @QtCore.pyqtProperty(QtGui.QColor)
    def background_color(self) -> QtGui.QColor:
        return self.__background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self.__background_color = color
        self.__current_color = self.__background_color
        self.update(self.cursorRect())

    def __toggle_caret_color(self) -> None:
        # toggles between the caret color and the background color
        if self.__current_color == self.__background_color:
            self.__current_color = self.__caret_color  # sets to visible color
        else:
            self.__current_color = self.__background_color  # sets to background color to hide
        self.update(self.cursorRect())

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)

        self.__current_color = self.__caret_color  # makes caret visible immediately
        self.update(self.cursorRect())  # updates the caret to show the color

        self.__blink_timer.start()

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.__blink_timer.stop()
        self.__current_color = self.__background_color  # makes caret invisible on focus loss
        self.update()

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        self.__current_color = self.__caret_color   # makes caret visible after a key press
        self.__blink_timer.start()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if self.__caret_size > 0:
            qp = QtGui.QPainter(self.viewport())
            full_rect = self.cursorRect()
            x = full_rect.x() + round(full_rect.width() / 2) - round(self.__caret_size / 2)
            cr = QtCore.QRect(x, full_rect.y(), max(1, self.__caret_size), self.fontMetrics().height())
            qp.fillRect(cr, self.__current_color)
