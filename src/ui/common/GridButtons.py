from PyQt6 import QtCore, QtGui, QtWidgets
from typing import Callable


class GridButtons(QtWidgets.QWidget):
    """
    A grid of buttons that can be resized and rearranged. The column count is determined by the width of the widget and buttons.
    """
    
    def __init__(self, parent: QtWidgets.QWidget | None = None, buttonTexts: list[str] = [], function: Callable[[], None] | None = None, buttonWidth: int = 50) -> None:
        super().__init__(parent)

        self.__buttonTexts: list[str] = buttonTexts
        self.__function: Callable[[], None] | None = function
        self.__buttonWidth: int = buttonWidth
        
        self.__initUi()

    def __initUi(self) -> None:
        """
        Initializes the UI components.
        """

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # adds buttons to the grid layout
        self.__previous_column_count = -1
        self.__buttons: list[QtWidgets.QPushButton] = []
        for i, symbol in enumerate(self.__buttonTexts):
            button = QtWidgets.QPushButton(symbol)
            self.__buttons.append(button)

            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

            if self.__function is not None:
                button.clicked.connect(self.__function)

            self.layout().addWidget(button, i // 4, i % 4)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """
        Handles the resize event of the widget.
        """

        super().resizeEvent(a0)
        self.__updateGrid()
    
    def buttons(self) -> list[QtWidgets.QPushButton]:
        """
        Returns a list of all buttons.
        """

        return self.__buttons
    
    def setButtonWidth(self, width: int) -> None:
        """
        Sets the width of all buttons.
        """

        self.__buttonWidth = width
        self.resizeEvent(None)

    def setButtonHeight(self, height: int) -> None:
        """
        Sets the height of all buttons.
        """

        for button in self.__buttons:
            button.setFixedHeight(height)

    def connect(self, function: Callable[[], None] | None) -> None:
        """
        Connects all buttons to the given function.
        """

        for button in self.__buttons:
            # disconnect any existing connections
            try:
                button.clicked.disconnect()
            except Exception:
                pass
            # connect to new function
            if function is not None:
                button.clicked.connect(function)

    def __updateGrid(self) -> None:
        """
        Updates the grid layout based on the current width of the widget.
        """

        width = self.width()
        column_count = max(1, width // self.__buttonWidth)  # takes into account the gap between the buttons

        # only rearranges if the column count changes
        if column_count != self.__previous_column_count:
            self.__previous_column_count = column_count

            # rearranges the buttons
            for i, button in enumerate(self.__buttons):
                self.layout().addWidget(button, i // column_count, i % column_count)
