from PyQt6 import QtCore, QtWidgets

import core.symbols as symbols
from ui.common.CaretLineEdit import CaretLineEdit
from ui.common.CaretTextEdit import CaretTextEdit
from ui.components.SectionTerms import SectionTerms


class SectionConstants(SectionTerms):
    visibilityChanged = QtCore.pyqtSignal()  # signal emitted when section visibility changes
    
    def __init__(self, parent: QtWidgets.QWidget | None = None, labelText: str | None = None, edit: CaretLineEdit | CaretTextEdit | None = None) -> None:
        super().__init__(parent, labelText)

        self._formWidget.layout().setSortKey(key=self.__getConstantSortKey)

        self.edit = edit

        self.__termContainers: dict[str, QtWidgets.QRadioButton] = {}
        self.__termRadioButtons: dict[str, list[QtWidgets.QRadioButton]] = {}
        self.__termPins: set[str] = set()

        self.__termLinks: dict[str, set[str]] = {}

        self.hide()  # hide self until terms are added

        self.__setEdit()

    def __getConstantSortKey(self, labelText: str) -> tuple[int, str]:
        """
        Generate sort key for constants in the exact order of symbols.constants.keys().
        Unknown constants are placed at the end and ordered alphabetically.
        
        Args:
            label_text: The label text from the form (e.g., "π:")
            
        Returns:
            Tuple of (order_index, constant_name) for sorting
        """

        name = labelText.strip()
        if name.endswith(':'):
            name = name[:-1].strip()
        
        # create order mapping from constants.keys()
        constantsOrder = list(symbols.constants.keys())
        orderMap = {const: i for i, const in enumerate(constantsOrder)}
        
        return (orderMap.get(name, len(orderMap)), name)

    def __setEdit(self) -> None:
        """
        Sets the external edit widget for tracking term changes.
        """

        if self.edit is None:
            raise ValueError("Edit widget cannot be None.")

        elif self.edit.tag() is None:
            raise ValueError("Edit widget's tag cannot be None.")

        elif self.edit.tag() in symbols.accepted_variables or self.edit.tag() in symbols.accepted_constants:
            raise ValueError("Edit widget's tag cannot be a term.")

        self.edit.textChanged.connect(lambda text, le=self.edit: self.__textUpdate(text, le.tag()))
        self.__termLinks[self.edit.tag()] = set()
        self.__termPins.add(self.edit.tag())

    def terms(self) -> dict[str, str]:
        """
        Return a dictionary of all terms and their current values.
        """

        temp: dict[str, str] = {}

        for key in self.__termContainers.keys():  # iterate through all terms
            buttons = self.__termRadioButtons[key]
            for index, button in enumerate(buttons):  # find checked button
                if button.isChecked():
                    buttonIndex = index
                    break

            temp[key] = symbols.constants[key][buttonIndex]

        return temp

    def addTerms(self, terms: list[str]) -> None:
        """
        Adds new terms.
        """

        if terms == set():
            return

        for term in terms:

            if term not in self.__termContainers.keys():  # create new container if needed
                container: QtWidgets.QWidget = QtWidgets.QWidget()
                container.setStyleSheet("margin-top: -1px;")  # raise the container by 1 pixel
                container.setLayout(QtWidgets.QHBoxLayout())
                container.layout().setContentsMargins(0, 0, 0, 0)
                container.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
                group: QtWidgets.QButtonGroup = QtWidgets.QButtonGroup(container)

                buttons = []
                for i, eq in enumerate(symbols.constants_terms[term]):  # create radio buttons for all term equivalents
                    button: QtWidgets.QRadioButton = QtWidgets.QRadioButton(eq)
                    button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                    buttons.append(button)

                    container.layout().addWidget(button)
                    group.addButton(button)

                    if i == 0:  # default selection
                        button.setChecked(True)

                self.__termRadioButtons[term] = buttons

                container.layout().addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

                self.__termContainers[term] = container
                self.__termLinks[term] = set()  # initialize term links

        self.__updateTerms(terms)

        self._formWidget.layout().sort()

        # show self if some terms are present
        if len(self.__termContainers) > 0: 
            self.show()
            self.visibilityChanged.emit()

    def removeTerms(self, terms: set[str]) -> None:
        """
        Deletes given term's containers, buttons, and their links.
        """

        # remove given terms
        for term in terms:
            if term in self.__termPins:
                continue  # do not remove pinned terms

            self.__termLinks.pop(term, None)

            if term in self.__termContainers:
                container = self.__termContainers[term]

                # remove the term's row
                self._formWidget.layout().removeRowByWidget(container)

                del self.__termContainers[term]
                del self.__termRadioButtons[term]

        self.__resetLinks()

        # hide self if no terms remain
        if len(self.__termContainers) == 0:
            self.hide()
            self.visibilityChanged.emit()

    def __resetLinks(self) -> None:
        """
        Reset links and remove any orphaned terms.
        """
        
        # get all links
        links: set[str] = set()
        for term in self.__termLinks:
            links.update(self.__termLinks[term])

        for container in list(self.__termContainers.keys()):
            if container not in links:
                self.removeTerms(set([container]))

    def __updateLinks(self, term: str, newLinks: set[str]) -> None:
        """
        Update links for a term and remove any orphaned terms.
        """
        
        if self.__termLinks[term] == newLinks:
            return  # return if no change

        # get all terms that were removed
        diff = self.__termLinks[term] - newLinks

        self.__termLinks[term] -= diff  # remove old links

        # get all terms that are not linked to any other terms
        links = set().union(*self.__termLinks.values())
        remove = diff - links

        if len(remove) > 0:
            self.removeTerms(remove)

    def __updateTerms(self, terms) -> None:
        """
        Update the form layout with current terms.
        """

        for term in terms:
            self._formWidget.layout().addRow(f"{term}:", self.__termContainers[term])

    def __textUpdate(self, text: str, tag: str | None) -> None:
        """
        Handle text updates from external edits.
        """

        text = text.replace(' ', '')

        # remove all functions to prevent variable false positives
        for function in symbols.accepted_functions:
            text = text.replace(function, '')

        terms = set(text) & symbols.accepted_constants  # find all variables in text
        add = terms - self.__termLinks[tag]  # find all added terms

        self.__updateLinks(tag, terms)

        self.__termLinks[tag].update(add)  # add new links
        self.addTerms(add)  # add new terms

    def variableChangedHandler(self, text: str, tag: str | None) -> None:
        """
        Handle variable updates from SectionVariables and any external lineEdits.
        Allows constants to be aware of variable changes.
        """

        if tag not in self.__termLinks:
            self.__termLinks[tag] = set()  # initialize links for this tag

        self.__textUpdate(text, tag)

    def variableRemovedHandler(self, removed_variables: set[str]) -> None:
        """
        Clean up links when variables are removed from SectionVariables.
        This prevents orphaned constants from staying in the constants section.
        """

        for variable in removed_variables:
            # remove the link entry for this variable
            if variable in self.__termLinks:
                del self.__termLinks[variable]
        
        # trigger link reset to clean up any orphaned constants
        self.__resetLinks()
