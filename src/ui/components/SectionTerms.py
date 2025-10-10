from PyQt6 import QtCore, QtWidgets

from ui.common.SortFormLayout import SortFormLayout


class SectionTerms(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None, labelText: str | None = None) -> None:
        super().__init__(parent)

        self.__labelText: str | None = labelText

        self.__initUi()

    def __initUi(self) -> None:
        """
        Initializes the UI components.
        """

        self.setLayout(QtWidgets.QVBoxLayout())

        # init label and line
        self.__label = None
        self.__line = None
        if self.__labelText is not None:
            # add title
            self.__label: QtWidgets.QLabel = QtWidgets.QLabel(self.__labelText)
            self.layout().addWidget(self.__label)

            # add line under title
            self.__line: QtWidgets.QFrame = QtWidgets.QFrame()
            self.__line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            self.__line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
            self.layout().addWidget(self.__line)

        # add scroll area
        self.__scrollArea: QtWidgets.QScrollArea = QtWidgets.QScrollArea()
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setMinimumHeight(98)
        self.__scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.__scrollArea.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
        self.layout().addWidget(self.__scrollArea)

        # init form layout for sorted term rows
        self._formWidget = QtWidgets.QWidget()
        self._formWidget.setLayout(SortFormLayout())
        self._formWidget.layout().setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.__scrollArea.setWidget(self._formWidget)

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
