from PyQt6 import QtWidgets

import core.symbols as symbols
from ui.components.SectionGridButtons import SectionGridButtons


class PageNotation(QtWidgets.QFrame):
    """
    A page that contains buttons for symbols and functions.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.setLayout(QtWidgets.QVBoxLayout())

        self.__sections: list[QtWidgets.QWidget] = []
        self.__sections.append(SectionGridButtons(None, "Symbols", symbols.copy_notation[0]))
        self.__sections.append(SectionGridButtons(None, "Functions", symbols.copy_notation[1]))

        for section in self.__sections:
            self.layout().addWidget(section)
            section.layout().setContentsMargins(0, 0, 0, 0)

    def getSections(self) -> list[QtWidgets.QWidget]:
        """
        Returns the list of sections.
        """

        return self.__sections
