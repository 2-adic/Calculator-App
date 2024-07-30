from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize


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
