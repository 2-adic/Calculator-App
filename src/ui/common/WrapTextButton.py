from PyQt6 import QtCore, QtGui, QtWidgets


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
            