from PyQt6 import QtWidgets
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class SortFormLayout(QtWidgets.QFormLayout):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.__sortKey: Callable[[T], Any] | None = None
        self.__sortReverse: bool = False

    def addRow(self, labelText: str | None, widget: QtWidgets.QWidget | None = None) -> None:
        """
        Adds a row to the form layout. All rows are separated by a line.
        """

        super().addRow(labelText, widget)

        # create line
        line: QtWidgets.QFrame = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        super().addRow(line)  # add line to row

    def setSortKey(self, key: Callable[[T], Any] | None = None, reverse: bool = False) -> None:
        self.__sortKey = key
        self.__sortReverse = reverse

    def sort(self):
        """
        Sorts the rows in the layout.
        This function only sorts rows with a label and a field, which are the even rows.
        The odd rows are separators and are not sorted.
        """

        sortedRows = []
        # collect all rows with their label text and field widgets
        for i in range(0, self.rowCount(), 2):
            labelItem = self.itemAt(i, QtWidgets.QFormLayout.ItemRole.LabelRole)
            fieldItem = self.itemAt(i, QtWidgets.QFormLayout.ItemRole.FieldRole)

            if labelItem and fieldItem:
                labelWidget = labelItem.widget()
                fieldWidget = fieldItem.widget()
                if labelWidget and fieldWidget:
                    # get the label text from the QLabel widget
                    labelText = labelWidget.text() if hasattr(labelWidget, 'text') else str(labelWidget)
                    sortedRows.append((labelText, fieldWidget))

        # define the key for sorting - sort based on label text
        if self.__sortKey:
            sortKeyFunc = lambda row: self.__sortKey(row[0])  # row[0] is labelText
        else:
            sortKeyFunc = lambda row: row[0]  # default sort by label text

        # sort the list of rows
        try:
            sortedRows.sort(key=sortKeyFunc, reverse=self.__sortReverse)
        except (TypeError, AttributeError):
            # fallback to string conversion if the key function fails
            sortedRows.sort(key=lambda row: str(row[0]), reverse=self.__sortReverse)

        # temporarily disable updates to avoid flickering
        if self.parentWidget():
            self.parentWidget().setUpdatesEnabled(False)

        # clear the layout completely
        while self.rowCount() > 0:
            rowResult = self.takeRow(0)

            # delete separator widgets (these are the horizontal lines)
            if rowResult.fieldItem and rowResult.fieldItem.widget():
                widget = rowResult.fieldItem.widget()
                # only delete if it's a separator line (QFrame)
                if isinstance(widget, QtWidgets.QFrame):
                    widget.deleteLater()

            if rowResult.labelItem and rowResult.labelItem.widget():
                widget = rowResult.labelItem.widget()
                # only delete if it's a separator line (QFrame)
                if isinstance(widget, QtWidgets.QFrame):
                    widget.deleteLater()

        # add the sorted rows back with their original labels
        for labelText, fieldWidget in sortedRows:
            self.addRow(labelText, fieldWidget)

        # re-enable updates and repaint
        if self.parentWidget():
            self.parentWidget().setUpdatesEnabled(True)
            self.parentWidget().update()

    def removeRowByWidget(self, widget: QtWidgets.QWidget) -> bool:
        """
        Removes a row from the layout by finding the row that contains the specified widget.
        This also removes the associated separator line.
        Returns True if the row was found and removed, False otherwise.
        """

        for i in range(self.rowCount()):
            fieldItem = self.itemAt(i, QtWidgets.QFormLayout.ItemRole.FieldRole)
            if fieldItem and fieldItem.widget() is widget:
                # remove the entire row (both label and field)
                rowResult = self.takeRow(i)

                # delete the label widget if it exists
                if rowResult.labelItem and rowResult.labelItem.widget():
                    rowResult.labelItem.widget().deleteLater()

                # delete the field widget
                if rowResult.fieldItem and rowResult.fieldItem.widget():
                    rowResult.fieldItem.widget().deleteLater()

                # remove the separator line (next row should be a separator)
                if i < self.rowCount():
                    separatorResult = self.takeRow(i)  # i is now the separator row
                    if separatorResult.fieldItem and separatorResult.fieldItem.widget():
                        separatorWidget = separatorResult.fieldItem.widget()
                        if isinstance(separatorWidget, QtWidgets.QFrame):
                            separatorWidget.deleteLater()

                return True

        return False