from PyQt6 import QtCore, QtGui, QtWidgets
from typing import Callable

from ui.common.GridButtons import GridButtons


class SectionGridButtons(QtWidgets.QWidget):
    """
    A section which includes a title, a horizontal line, and a scroll area containing buttons.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None, labelText: str | None = None, buttonTexts: list[str] = [], function: Callable[[], None] | None = None, buttonWidth: int = 50) -> None:
        super().__init__(parent)

        self.__labelText: str | None = labelText
        self.__buttonTexts: list[str] = buttonTexts
        self.__function: Callable[[], None] | None = function
        self.__buttonWidth: int = buttonWidth
        
        self.__initUi()

        self.__scrollArea.viewport().installEventFilter(self)  # event filter used to resize the QScrollArea

    def __initUi(self) -> None:
        """
        Initializes the UI components.
        """

        self.setLayout(QtWidgets.QVBoxLayout())

        if self.__labelText is not None:
            # add title
            self.__label: QtWidgets.QLabel = QtWidgets.QLabel(self.__labelText)
            self.layout().addWidget(self.__label)

            # add line under title
            self.__line: QtWidgets.QFrame = QtWidgets.QFrame()
            self.__line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            self.__line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
            self.layout().addWidget(self.__line)

        else:
            self.__label = None
            self.__line = None

        # add scroll area
        self.__scrollArea = QtWidgets.QScrollArea()
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout().addWidget(self.__scrollArea)

        self.__buttonGrid = GridButtons(None, self.__buttonTexts, self.__function, self.__buttonWidth)
        self.__scrollArea.setWidget(self.__buttonGrid)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """
        Handles the resize event for the widget.
        """

        super().resizeEvent(a0)

    def label(self) -> QtWidgets.QLabel | None:
        """
        Returns the label widget.
        """

        return self.__label
    
    def line(self) -> QtWidgets.QFrame | None:
        """
        Returns the line widget.
        """

        return self.__line
    
    def scrollArea(self) -> QtWidgets.QScrollArea:
        """
        Returns the scroll area widget.
        """

        return self.__scrollArea
    
    def buttons(self) -> list[QtWidgets.QPushButton]:
        """
        Returns the list of button widgets.
        """

        return self.__buttonGrid.buttons()
    
    def setButtonWidth(self, width: int) -> None:
        """
        Sets the width of the buttons.
        """

        self.__buttonWidth = width
        self.__buttonGrid.setButtonWidth(self.__buttonWidth)
        self.resizeEvent(None)

    def setButtonHeight(self, height: int) -> None:
        """
        Sets the height of the buttons.
        """

        self.__buttonGrid.setButtonHeight(height)

    def connect(self, function: Callable[[], None] | None) -> None:
        """
        Connects the button grid's signals to the given function.
        """

        self.__buttonGrid.connect(function)
