from PyQt6 import QtCore, QtWidgets

import core.symbols as symbols
from ui.common.CaretLineEdit import CaretLineEdit
from ui.common.CaretTextEdit import CaretTextEdit
from ui.components.SectionTerms import SectionTerms


class SectionVariables(SectionTerms):
    variableChanged = QtCore.pyqtSignal(str, str)  # signal emitted when a variable's value changes     (text, tag)
    variableRemoved = QtCore.pyqtSignal(set)  # signal emitted when variables are removed               (removed variables)
    visibilityChanged = QtCore.pyqtSignal()  # signal emitted when section visibility changes
    def __init__(self, parent: QtWidgets.QWidget | None = None, labelText: str | None = None, edit: CaretLineEdit | CaretTextEdit | None = None) -> None:
        super().__init__(parent, labelText)

        self._formWidget.layout().setSortKey(key=self.__getVariableSortKey)

        self.edit = edit

        self.__termEdits: dict[str, QtWidgets.QLineEdit] = {}
        self.__termLinks: dict[str, set[str]] = {}
        self.__termPins: set[str] = set()

        self.hide()  # hide self until terms are added

        self.__setEdit()

    def __getVariableSortKey(self, labelText: str) -> tuple[int, str]:
        """
        Generate sort key for variables in the exact order of symbols.accepted_variables.
        Unknown variables are placed at the end and ordered alphabetically.
        
        Args:
            label_text: The label text from the form (e.g., "x =")
            
        Returns:
            Tuple of (order_index, variable_name) for sorting
        """

        name = labelText.strip()
        if name.endswith('='):
            name = name[:-1].strip()
        
        # create order mapping from accepted_variables
        variablesSorted = sorted(symbols.accepted_variables)
        orderMap = {var: i for i, var in enumerate(variablesSorted)}
        
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

        for key in self.__termEdits.keys():
            temp[key] = self.__termEdits[key].text()

        return temp

    def addTerms(self, terms: set[str]) -> None:
        """
        Adds new terms.
        """

        if terms == set():
            return

        for term in terms:

            if term not in self.__termEdits.keys():  # create new lineEdit
                lineEdit = CaretLineEdit(setText='', defaultText=term, tag=term)
                lineEdit.textChanged.connect(lambda text, le=lineEdit: self.__textUpdate(text, le.tag()))
                self.__termEdits[term] = lineEdit
                self.__termLinks[term] = set()  # initialize term links

        self.__updateTerms(terms)

        self._formWidget.layout().sort()

        # show self if some terms are present
        if len(self.__termEdits) > 0: 
            self.show()
            self.visibilityChanged.emit()

    def removeTerms(self, terms: set[str]) -> None:
        """
        Deletes given term's lineEdits and their links.
        """
        
        remove = set()  # track which terms were removed

        # remove given terms
        for term in terms:
            if term in self.__termPins:
                continue  # do not remove pinned terms

            self.__termLinks.pop(term, None)

            if term in self.__termEdits:
                lineEdit = self.__termEdits[term]
                
                # remove the term's row
                self._formWidget.layout().removeRowByWidget(lineEdit)
                
                del self.__termEdits[term]
                remove.add(term)

        # emit signal for removed variables
        if remove:
            self.variableRemoved.emit(remove)

        self.__resetLinks()

        # hide self if no terms remain
        if len(self.__termEdits) == 0:
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

        for lineEdit in list(self.__termEdits.keys()):
            if lineEdit not in links:
                self.removeTerms(set([lineEdit]))

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
            self._formWidget.layout().addRow(f"{term} =", self.__termEdits[term])

    def __textUpdate(self, text: str, tag: str | None) -> None:
        """
        Handle text changes from internal and external edits.
        """

        text = text.replace(' ', '')

        # remove all functions to prevent variable false positives
        for function in symbols.accepted_functions:
            text = text.replace(function, '')

        terms = set(text) & symbols.accepted_variables  # find all variables in text
        add = terms - self.__termLinks[tag]  # find all added terms

        self.__updateLinks(tag, terms)

        self.__termLinks[tag].update(add)  # add new links
        self.addTerms(add)  # add new terms

        # emit signal when variables change
        if tag:
            self.variableChanged.emit(text, tag)
