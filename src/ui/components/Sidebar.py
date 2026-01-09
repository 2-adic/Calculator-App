import pyperclip
from PyQt6 import QtCore, QtWidgets

from core.style import Settings, Style
import core.symbols as symbols
from core.system_settings import OperatingSystem
from ui.common.CaretLineEdit import CaretLineEdit
from ui.common.CaretTextEdit import CaretTextEdit
from ui.common.VerticalPageSelector import VerticalPageSelector
from ui.components.PageNotation import PageNotation
from ui.components.PageTerms import PageTerms
from ui.components.SectionGridButtons import SectionGridButtons


class Sidebar(VerticalPageSelector):

    def __init__(self, settings: Settings, style: Style, op: OperatingSystem, edit: CaretLineEdit | CaretTextEdit | None = None, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._settings_user: Settings = settings
        self._style: Style = style
        self._op: OperatingSystem = op

        n = 2
        for i in range(n):  # create n pages
            button = QtWidgets.QPushButton()
            button.setMinimumHeight(self._settings_user.select_height)
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.setCheckable(True)  # allows the button to be selected

            if i == 0:
                button.setText("Variables")
                button.setChecked(True)  # check the first button by default

                widget = PageTerms(edit = edit)
                self.__PageTerms = widget

            elif i == 1:
                button.setText("Notation")

                widget = PageNotation()

                self.__PageNotationSections: list[QtWidgets.QWidget] = widget.getSections()

                # configure notation sections
                for j, section in enumerate(self.__PageNotationSections):
                    if isinstance(section, SectionGridButtons):
                        section.layout().setContentsMargins(0, 0, 0, 0)
                        section.connect(self.__copy_button_label)
                        section.setButtonHeight(self._settings_user.symbols_button_height)

                        if j == 0:
                            section.scrollArea().setMinimumHeight(self._op.get_notation_symbols_min_height())  # stops the top scroll area from becoming too collapsed
                            section.setButtonWidth(self._settings_user.symbols_button_width[0])

                        elif j == 1:
                            section.setButtonWidth(self._settings_user.symbols_button_width[1])

            widget.layout().setContentsMargins(self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin)

            self.addPage(button, widget)

        self.layout().setSpacing(0)

    def terms(self) -> dict[str, str]:
        return self.__PageTerms.terms()
    
    def update_colors(self) -> None:
        # page selector
        for i, page in enumerate(self.pages()):
            self._style.set_page_selector(page)

        # selector buttons
        n = len(self.buttons())
        for i, button in enumerate(self.buttons()):
            self._style.set_selector(button, i, n)

        # page notation
        for i, section in enumerate(self.__PageNotationSections):
            if isinstance(section, SectionGridButtons):
                self._style.set_page_notation(section, section.scrollArea(), section.label(), section.line(), section.buttons())

        # page terms
        self._style.set_page_terms(self.__PageTerms)

    def __copy_button_label(self) -> None:
        button = self.sender()
        text = button.text()

        if text not in symbols.copy_notation[0]:  # adds parentheses to functions
            text += "()"

        pyperclip.copy(text)

