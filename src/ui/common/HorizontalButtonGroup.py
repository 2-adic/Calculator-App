from PyQt6 import QtCore, QtWidgets


class HorizontalButtonGroup(QtWidgets.QHBoxLayout):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.__buttonGroup: QtWidgets.QButtonGroup = QtWidgets.QButtonGroup(self)
        
    def addWidget(self, a0: QtWidgets.QWidget, stretch: int = 0, alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag(0)):
        """
        Adds a widget to the layout, and to the button group if it's a button.
        """

        super().addWidget(a0, stretch, alignment)

        # add to button group if the widget is a button
        if isinstance(a0, QtWidgets.QAbstractButton):  
            self.__buttonGroup.addButton(a0)

    def buttons(self) -> list[QtWidgets.QAbstractButton]:
        """
        Returns a list of all buttons in the button group.
        """

        return self.__buttonGroup.buttons()
    
    def buttonGroup(self) -> QtWidgets.QButtonGroup:
        """
        Returns the button group.
        """

        return self.__buttonGroup
