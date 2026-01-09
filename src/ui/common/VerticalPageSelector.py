from PyQt6 import QtWidgets

from ui.common.HorizontalButtonGroup import HorizontalButtonGroup


class VerticalPageSelector(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.__horizontalButtonGroup = HorizontalButtonGroup()  # buttons to change page
        self.__stackedWidget: QtWidgets.QStackedWidget = QtWidgets.QStackedWidget()  # pages

        self.layout().addLayout(self.__horizontalButtonGroup)
        self.layout().addWidget(self.__stackedWidget)

    def buttons(self) -> list[QtWidgets.QAbstractButton]:
        """
        Returns the list of buttons in the horizontal button group.
        """

        return self.__horizontalButtonGroup.buttons()

    def pages(self) -> list[QtWidgets.QWidget]:
        """
        Returns the list of pages in the stacked widget.
        """

        pages: list[QtWidgets.QWidget] = []
        for i in range(self.__stackedWidget.count()):
            pages.append(self.__stackedWidget.widget(i))

        return pages
    
    def addPage(self, b: QtWidgets.QAbstractButton, w: QtWidgets.QWidget) -> None:
        """
        Adds a page to the stacked widget and connects the button to the page selection.
        """

        b.clicked.connect(self.__pageSelect)
        
        self.__horizontalButtonGroup.addWidget(b)
        self.__stackedWidget.addWidget(w)

    def __pageSelect(self):
        """
        Function for handling page selection.
        """

        for i, button in enumerate(self.buttons()):
            if self.sender() == button:
                self.__stackedWidget.setCurrentIndex(i)
