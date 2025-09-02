from PyQt6 import QtCore, QtWidgets
import pyperclip

import core.misc_functions as misc_functions
import core.symbols as symbols


class MultiBox(QtWidgets.QPushButton):  # inherits QPushButton to prevent reference warnings
    def __init__(self):
        super().__init__()

        # pre-initializes variables to None (to prevent reference warnings); variables are defined by MainWindow
        self._settings_user = None
        self._style = None
        self._symbols = None
        self._user_select = None
        self._box_text = None
        self._text_update_lambda = None
        self._symbols_prev_keys = None
        self._op = None

        self._setup()

    def _setup(self) -> None:

        # Scroll Area Setup -------------------------------------------------------------------------------------

        self.__selector_names = ["Variables", "Notation"]  # include at least 2 names (these will most likely be images in the future, for example: a simple image of a graph for the graph tab)
        self.__area_amount = len(self.__selector_names)  # amount of scroll areas, at least 2 are needed for correct formatting

        # creates the scroll areas
        self.__areas = []
        for i in range(self.__area_amount):
            area = QtWidgets.QWidget(self)

            layout = QtWidgets.QVBoxLayout(area)
            layout.setContentsMargins(self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin, self._settings_user.content_margin)

            area.hide()
            self.__areas.append([area, layout, []])

        self.__areas[0][0].show()  # defaults to the variables tab

        # Selectors ---------------------------------------------------------------------------------------------

        self.__button_selected = 0  # the default selected button is the variables tab

        self.__button_selectors = []
        group = QtWidgets.QButtonGroup(self)  # adds a button group to keep track of which selector is selected
        for i in range(self.__area_amount):
            button = QtWidgets.QPushButton(self.__selector_names[i], self)
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(self.__button_selector_logic)

            button.setCheckable(True)  # allows the button to be selected instead of only pressed
            group.addButton(button)
            if i == 0:  # selects the first selector by default
                button.setChecked(True)

            self._style.set_button_selector(button, i, self.__area_amount)
            self.__button_selectors.append(button)  # adds the button to a list

        self.__areas[0][0].show()  # shows the default tab

        # All Tabs ----------------------------------------------------------------------------------------------

        # sets a default label for each page
        for i, title in enumerate(self.__selector_names):

            if i == 1:  # skips the notation tab since it is never empty
                continue

            label = QtWidgets.QLabel(title)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self._style.set_selector_label(label)
            self.__areas[i][1].addStretch()
            self.__areas[i][1].addWidget(label)
            self.__areas[i][1].addStretch()

        self.__fill_notation()  # initializes the symbols tab

        # Variable Tab ------------------------------------------------------------------------------------------

        # scroll area container alignment
        self.__areas[0][1].setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # sections of the variable page
        self.__titles = ["Variables", "Constants", "Arbitrary Constants"]

    def update_settings_multi(self) -> None:
        """
        Refreshes the windows to apply the new settings.
        """

        self.__update_colors_multi()

    def _update_multi(self) -> None:
        """
        Updates the positions of all widgets in the multi class.
        """

        # selectors
        # although this works perfectly, a lot of the math in this section is not optimized
        selector_size = (1/len(self.__button_selectors)) * (self.width() * (1 - self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + self._settings_user.box_border - (self._settings_user.box_border/len(self.__button_selectors))  # width of the selector buttons
        for i, button in enumerate(self.__button_selectors):

            # corrects for rounding errors which makes the borders between the buttons change size
            correction = 0
            if i != len(self.__button_selectors) - 1:
                correction = (int(((selector_size - self._settings_user.box_border) * (i - 1)) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int(selector_size) - self._settings_user.box_border) - int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5))

                if correction == 0 and (int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int(selector_size) - self._settings_user.box_border) - int(((selector_size - self._settings_user.box_border) * (i + 1)) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) == -1:
                    correction -= 1

            # makes sure the last selector and the box below line up
            elif int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int(selector_size) != (self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)) + int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)):
                correction -= 1

            # move the buttons to their correct place, while keeping the borders the same size
            button.move(int(((selector_size - self._settings_user.box_border) * i) + (self._settings_user.box_padding * 2) + (self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height)
            button.resize(int(selector_size) - correction, self._settings_user.select_height)

        # multi box
        for tup in self.__areas:
            tup[0].move((self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height + self._settings_user.select_height - self._settings_user.box_border)
            tup[0].resize(int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)), self.height() - (self._settings_user.box_padding * 2) - self._settings_user.title_bar_height - self._settings_user.select_height + self._settings_user.box_border)

        # symbols tab
        if self.__button_selected == 1:
            for i in range(2):
                width = self.__areas[1][2][i].viewport().width()
                column_count = max(1, width // self._settings_user.symbols_button_width[i])  # takes into account the gap between the buttons

                # only rearranges if the column count changes
                if column_count != self.__previous_column_count[i]:
                    self.__previous_column_count[i] = column_count

                    # re-arranges the buttons
                    for x, button in enumerate(self.__button_symbols[i]):
                        self.__grid_layout[i].addWidget(button, x // column_count, x % column_count)

    def _fill_variables(self) -> None:
        """
        Displays widgets to the variable tab.

        Adds: labels and text boxes for each variable, lines to separate each variable, and a stretch to push all widgets to the top.
        """

        if self._user_select != self._box_text:
            scroll_area = self._user_select.parent().parent().parent()

            scroll_bar = scroll_area.verticalScrollBar()
            previous_scroll_amount = scroll_bar.value()

        self.__clear_variables()  # deletes everything in the variable page

        count = 0
        self.__areas[0][2] = []
        for index in range(len(self._symbols)):
            self.__areas[0][2].append(QtWidgets.QScrollArea())  # initializes the scroll areas
            count += len(self._symbols[index].keys())

        if count == 0:  # if there are no variables, the default text is generated
            label = QtWidgets.QLabel("Variables")
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self._style.set_selector_label(label)
            self.__areas[0][1].addStretch()
            self.__areas[0][1].addWidget(label)
            self.__areas[0][1].addStretch()

        else:  # if there are no variables, this does not run
            for i, title in enumerate(self.__titles):
                if i == 2:  # arbitrary constants are not implemented yet
                    continue

                if len(self._symbols[i]) == 0:  # skips individual sections if they are empty
                    continue

                if i > 0:  # adds spacing before each label
                    self.__areas[0][1].addSpacing(5)

                # label for each scroll area
                label = QtWidgets.QLabel(title)
                self._style.set_multibox_label(label)
                self.__areas[0][1].addWidget(label)

                # scroll area setup
                self.__areas[0][2][i].setWidgetResizable(True)
                self.__areas[0][2][i].setMinimumHeight(90)
                self.__areas[0][2][i].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                self.__areas[0][2][i].setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

                # inside the scroll areas
                layout = QtWidgets.QFormLayout()
                layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

                for key in sorted(self._symbols[i].keys()):
                    row = []
                    if i == 0:
                        label, edit = self._symbols[0][key]

                        edit.textChanged.connect(self._text_update_lambda)
                        edit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)

                        row.append(label)
                        row.append(edit)

                    if i == 1:
                        label, option1, option2 = self._symbols[1][key]

                        hbox = QtWidgets.QHBoxLayout()
                        hbox.addWidget(option1)
                        if key != 'i':  # 'i' doesn't need a second selector option
                            hbox.addWidget(option2)
                        hbox.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

                        row.append(label)
                        row.append(hbox)

                    layout.addRow(*row)

                    line = QtWidgets.QFrame()
                    line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                    line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                    self._style.set_line_secondary(line)

                    layout.addRow(line)

                content_widget = QtWidgets.QWidget()
                content_widget.setLayout(layout)

                # inner content widget
                self.__areas[0][2][i].setWidget(content_widget)

                line = QtWidgets.QFrame()
                line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                self._style.set_line_primary(line)
                self.__areas[0][1].addWidget(line)

                self._style.set_scroll_area(self.__areas[0][2][i])

                self.__areas[0][1].addWidget(self.__areas[0][2][i])

        # focuses the user to the current textbox they are typing in
        if self._user_select != self._box_text:

            scroll_area = self._user_select.parent().parent().parent()

            # finds the amount of variables inserted before the selected line edit
            key = misc_functions.get_line_edit_key(self._symbols[0], self._user_select)
            symbols_prev_keys = self._symbols_prev_keys
            symbols_curr_keys = sorted(self._symbols[0].keys())
            amount_inserted_before = misc_functions.get_position_change(symbols_prev_keys, symbols_curr_keys, key)

            QtCore.QTimer.singleShot(0, lambda: self.__set_scrollbar(scroll_area.verticalScrollBar(), previous_scroll_amount, amount_inserted_before))  # QTimer is used due to the max_scroll not being correctly calculated

            self._user_select.setFocus()

    def __update_colors_multi(self) -> None:

        self._style.set_areas(self.__areas)
        self._style.set_notation(self.__save_label, self.__save_line, self.__save_button)
        self._style.set_variable_radio_button(self._symbols)
        self._style.set_button_selectors(self.__button_selectors)

    def __fill_notation(self) -> None:
        """
        Creates all buttons of hard to get symbols within the symbols tab.

        Allows for the user to easily copy symbols to use in calculations.
        """

        label_titles = ["Symbols", "Functions"]

        self.__grid_layout = []
        self.__button_symbols = []
        self.__previous_column_count = []

        # saves specific elements for changing the stylesheets
        self.__save_line = []
        self.__save_label = []
        self.__save_button = []

        for i in range(2):

            # adds a title for each section
            label = QtWidgets.QLabel(label_titles[i])
            self.__save_label.append(label)  # saves for future stylesheet changes
            self.__areas[1][1].addWidget(label)

            # adds a line under the title
            line = QtWidgets.QFrame()
            self.__save_line.append(line)  # saves for future stylesheet changes
            line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
            self.__areas[1][1].addWidget(line)

            # adds a scroll area
            self.__areas[1][2].append(QtWidgets.QScrollArea())
            self.__areas[1][2][i].setWidgetResizable(True)
            if i == 0:
                self.__areas[1][2][0].setMinimumHeight(self._op.get_notation_symbols_min_height())  # stops the top scroll area from becoming too collapsed
            self.__areas[1][2][i].setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            # uses a QFrame to hold the grid layout
            grid_widget = QtWidgets.QFrame()
            grid_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

            # uses a QGridLayout to get the desired behavior
            self.__grid_layout.append(QtWidgets.QGridLayout())
            grid_widget.setLayout(self.__grid_layout[i])

            # creates a wrapper widget for the scroll area
            wrapper_widget = QtWidgets.QWidget()
            wrapper_layout = QtWidgets.QVBoxLayout(wrapper_widget)
            wrapper_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            wrapper_layout.addWidget(grid_widget)
            self.__areas[1][2][i].setWidget(wrapper_widget)

            # adds buttons to the grid layout
            self.__button_symbols.append([])
            for x, symbol in enumerate(symbols.copy_notation[i]):
                button = QtWidgets.QPushButton(symbol)
                button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                self.__save_button.append(button)  # saves for future stylesheet changes
                button.clicked.connect(self.__copy_button_label)
                button.setFixedHeight(self._settings_user.symbols_button_height)
                self.__button_symbols[i].append(button)
                self.__grid_layout[i].addWidget(button, x // 4, x % 4)

            self.__areas[1][1].addWidget(self.__areas[1][2][i])  # adds the scroll area to the layout

            self.__previous_column_count.append(-1)  # initializes the column count

    def __button_selector_logic(self) -> None:
        """
        Applies styles to the selector buttons and keeps track of which button was selected.
        """

        for i, scroll in enumerate(self.__areas):
            button = self.__button_selectors[i]

            if i == 1:
                QtCore.QTimer.singleShot(0, self._update_multi)  # the symbols section is not initialized correctly without this

            if self.sender() == button:
                scroll[0].show()
                self.__button_selected = i

            else:
                scroll[0].hide()

    def __set_scrollbar(self, scroll_bar, previous_scroll_amount, new_items) -> None:
        """
        Prevents the elements in the scroll bar from moving locations when variables are added in the line edits.
        """

        max_value = scroll_bar.maximum()
        if max_value != 0:
            new = previous_scroll_amount + (new_items * self._op.get_scroll_bar_variable_height())
            scroll_bar.setValue(min(max_value, new))

    def __clear_variables(self) -> None:
        """
        Removes all widgets from the variable tab, disconnecting signals and clearing nested layouts.
        """

        # disconnects all LineEdits from their function
        for index in range(len(self._symbols)):
            keys = list(self._symbols[index].keys())
            for key in keys:
                try:
                    self._symbols[index][key][1].textChanged.disconnect(self._text_update_lambda)
                except:
                    pass

        # deletes all elements in the layout
        layout = self.__areas[0][1]
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self.__clear_inner_layout(item.layout())
                item.layout().deleteLater()

    def __clear_inner_layout(self, layout: QtWidgets.QLayout) -> None:
        """
        Recursively removes all items from a given nested layout.
        """

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.__clear_inner_layout(item.layout())
                item.layout().deleteLater()

    def __copy_button_label(self) -> None:
        button = self.sender()
        text = button.text()

        if text not in symbols.copy_notation[0]:  # adds parentheses to functions
            text += "()"

        pyperclip.copy(text)
