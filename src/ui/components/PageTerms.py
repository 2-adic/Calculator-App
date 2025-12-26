from PyQt6 import QtCore, QtWidgets

from ui.common.CaretLineEdit import CaretLineEdit
from ui.common.CaretTextEdit import CaretTextEdit
from ui.components.SectionConstants import SectionConstants
from ui.components.SectionVariables import SectionVariables


class PageTerms(QtWidgets.QFrame):
    """
    A page that contains sections for defining terms such as variables and constants.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None, edit: CaretLineEdit | CaretTextEdit | None = None) -> None:
        super().__init__(parent)

        self.__edit = edit

        self.initUi()

    def initUi(self) -> None:
        """
        Initializes the UI components.
        """

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.__sections: list[QtWidgets.QWidget] = []

        # container widget for label and stretches
        self.__labelContainer = QtWidgets.QWidget()
        self.__labelContainer.setObjectName("LabelContainer")
        self.__labelContainer.setLayout(QtWidgets.QVBoxLayout())
        self.__labelContainer.layout().addStretch()
        self.__labelContainer.layout().addWidget(QtWidgets.QLabel("Variables"), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__labelContainer.layout().addStretch()
        self.layout().addWidget(self.__labelContainer)

        self.__sections.append(SectionVariables(None, labelText="Variables", edit=self.__edit))
        self.__sections.append(SectionConstants(None, labelText="Constants", edit=self.__edit))

        sectionVariables = self.__sections[0]  # SectionVariables
        sectionConstants = self.__sections[1]  # SectionConstants

        # connect signals for inter-section communication
        sectionVariables.variableChanged.connect(sectionConstants.variableChangedHandler)
        sectionVariables.variableRemoved.connect(sectionConstants.variableRemovedHandler)

        # connect visibility signals to hideLabelContainer
        sectionVariables.visibilityChanged.connect(self.updateLabelContainerVisibility)
        sectionConstants.visibilityChanged.connect(self.updateLabelContainerVisibility)

        for section in self.__sections:
            self.layout().addWidget(section)
            section.layout().setContentsMargins(0, 0, 0, 0)

    def updateLabelContainerVisibility(self) -> None:
        """
        Hides or shows the label container that holds the label and stretches.
        """

        # hide label container if any section has terms
        for section in self.__sections:
            if len(section) > 0:
                self.__labelContainer.hide()
                return

        self.__labelContainer.show()  # show if no sections are visible
        
    def getSections(self) -> list[QtWidgets.QWidget]:
        """
        Returns the list of sections.
        """

        return self.__sections

    def terms(self) -> dict[str, str]:
        """
        Combines all terms into one dictionary. Assumes all sections use different terms.
        """

        terms = {}
        for section in self.__sections:
            terms.update(section.terms())

        return terms
