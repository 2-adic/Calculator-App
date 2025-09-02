from PIL import Image
import pyperclip
from PyQt6 import QtCore, QtGui, QtWidgets

import core.error_detection as error
from core.files import path
from core.functions import Solve
from core.str_format import contains_substring, function_convert
from core.style import Settings, Style
import core.symbols as symbols
from core.system_settings import OperatingSystem, get_data_path
from ui.widgets.CaretLineEdit import CaretLineEdit
from ui.widgets.CaretTextEdit import CaretTextEdit
from ui.widgets.WrapTextButton import WrapTextButton
from ui.views.ControlWindow import ControlWindow
from ui.views.MultiBox import MultiBox


class MainWindow(MultiBox, ControlWindow):
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        ControlWindow.__init__(self, settings, style, op)
        MultiBox._setup(self)

        self._set_title(self._settings_user.window_title_main)
        self._set_geometry(*self._settings_user.window_start_size_main)
        self._set_size_min(*self._settings_user.window_size_min_main)

        # settings button
        self.__button_settings = QtWidgets.QPushButton('', self)
        self.__button_settings.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.__button_settings.setIcon(QtGui.QIcon(path("assets/icons/gear_icon.png")))
        size = int(self._settings_user.title_bar_settings_icon_scale * (self._settings_user.title_bar_height - (2 * self._settings_user.title_bar_settings_spacing)))

        # answer box
        self.__answer = None  # user shouldn't be able to access this string yet
        self.__answer_temp = self._settings_user.answer_default
        self.__solution = None
        self.__flip_type_toggle = False

        self._box_answer = WrapTextButton(self._settings_user.answer_default, self, self._settings_user.box_answer_padding)
        self._box_answer.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._box_answer.button().clicked.connect(self.__copy)

        self.__answer_image_path_exact = get_data_path("latex_exact.png")  # gets the path of the latex image
        self.__answer_image_path_approximate = get_data_path("latex_approximate.png")  # gets the path of the latex image

        # answer format label
        self._box_answer_format_label = QtWidgets.QLabel('', self)
        self._box_answer_format_label.setFixedWidth(25)
        self._box_answer_format_label.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # text box
        self._user_select = None
        self._box_text = CaretTextEdit(parent=self, caretSize=self._settings_user.caret_size)
        self._box_text.textChanged.connect(self._text_update)
        self._box_text.focusOutEvent = self.__box_text_focus_event
        self.__set_custom_context_menu(self._box_text)

        self._bar_spacer = QtWidgets.QWidget(self)  # adds a blank space to the right of the bar buttons

        self._bar_answer = QtWidgets.QPushButton("Answer", self)  # the button that lets the user compute the answer
        self._bar_answer.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._bar_answer.clicked.connect(lambda: self._get_answer())

        self._bar_format = QtWidgets.QPushButton("Format", self)  # the button that changes the format of the answer
        self._bar_format.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._bar_format.clicked.connect(self._flip_type)
        self._style.set_button_format_visibility(self._bar_answer, self._bar_format, False)

        # storage
        self._symbols = ({}, {}, {})
        self._symbols_prev_keys = []

        self.__is_constant_value_used = False

        # other
        self._text_update_lambda = lambda: self._text_update()  # used to keep track of the function for when it gets disconnected

    def connect_button_settings(self, function) -> None:
        """
        Connects the settings button to a function.
        """

        self.__button_settings.clicked.connect(function)

    def update_settings(self) -> None:
        """
        Refreshes the windows to apply the new settings.
        """

        # tells if an answer is being displayed or not
        is_displaying_answer = not (self._box_answer.text() == self._settings_user.answer_default or self._box_answer.text()[:6] == "Error:")

        self.__update_colors(is_displaying_answer)  # updates all colors for MainWindow

        if is_displaying_answer:
            self._get_answer(self.__flip_type_toggle)

        self.update_settings_multi()

    def _get_answer(self, stop_format_reset: bool | None = None) -> None:
        """
        Calculates the answer from the user input.

        Displays the answer in the answer box.
        """

        if stop_format_reset is None:
            self.__flip_type_toggle = False  # resets the format type
        else:  # stops the format from flipping if the apply button was pressed
            self.__flip_type_toggle = not stop_format_reset

        self._style.set_button_format_visibility(self._bar_answer, self._bar_format, True)

        text = self._box_text.toPlainText()  # gets the string from the text box

        try:
            self.__solution = Solve(text, self.__variable_formatting(self._symbols), self.__generate_value_used_bool(), self._settings_user.answer_display, self._settings_user.answer_copy, self._settings_user.use_commas, self._settings_user.color_latex, self._settings_user.latex_image_dpi)
            self.__solution.print()  # shows the before and after expressions (for testing purposes)
            self.__answer = self.__solution.get_exact()

            if self.__is_constant_value_used:  # hides the format button if a constant value was used
                self._style.set_button_format_visibility(self._bar_answer, self._bar_format, False)

            self._flip_type()

        except Exception as error:
            self.__box_answer_set(f"Error: {error}", f"Error:\n{error}")  # displays the error
            print(f"Error: {error}")

    def _flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        self._box_answer.setText('')
        self._box_answer.setIcon(QtGui.QIcon())

        # uses answer_temp to save the answer
        if self.__flip_type_toggle or self.__is_constant_value_used:
            self.__answer_temp = self.__solution.get_approximate()  # turns the answer into its decimal format
            image_path = self.__answer_image_path_approximate
            self._box_answer_format_label.setText('≈')
        else:
            self.__answer_temp = self.__answer  # returns the original answer
            image_path = self.__answer_image_path_exact
            self._box_answer_format_label.setText('=')

        self.__flip_type_toggle = not self.__flip_type_toggle  # keeps track of which format is being displayed

        if self.__solution.is_text_used():
            self._box_answer.setText(self.__answer_temp)

        else:
            image = Image.open(image_path)
            icon = QtGui.QIcon(image_path)
            self._box_answer.setIcon(icon, image.width / image.height)

        self.resizeEvent(None)

    def _text_update(self, activated: bool = False) -> None:
        """
        Activates each time a user changes their input in the text box.

        Adds and removes variables in the variables box based on the new user input.
        Removes the answer from the answer box.
        """

        if activated:  # if the _text_update was activated automatically, then sender is set the text box
            self._user_select = self._box_text
        else:
            self._user_select = self.sender()  # saves which text box the user was typing in

        text = self._box_text.toPlainText()
        text = function_convert(text)

        temp = set()  # used later for deleting variables in self._symbols which are not in the text box

        self._symbols_prev_keys = sorted(self._symbols[0].keys())

        # adds all variables from the text box to a dictionary
        for x in text:
            # checks if the character is in one of the accepted lists
            if x in symbols.accepted_variables:
                index = 0
                temp.add(x)
            elif x in symbols.accepted_constants:
                index = 1
                temp.add(x)
            else:
                continue

            # adds the character's label and line edit to the correct dictionary in symbols
            if x not in self._symbols[index]:
                if index == 0:
                    label = QtWidgets.QLabel(f"{x} =", self)

                    text_box = CaretLineEdit(parent=self, caretSize=self._settings_user.caret_size, caretColor=QtGui.QColor(*self._settings_user.color_line_secondary))
                    text_box.setPlaceholderText(f"{x}")
                    self.__set_custom_context_menu(text_box)
                    self._symbols[0][x] = (label, text_box)

                elif index == 1:
                    label = QtWidgets.QLabel(f"{x}:", self)

                    option1 = QtWidgets.QRadioButton(f"{x}")
                    option1.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                    option2 = QtWidgets.QRadioButton(symbols.constant_preview[x] + "...")
                    option2.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                    option1.setChecked(True)

                    # displays the default answer if a radio button was selected
                    option1.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)  # used to see if a new value was selected
                    option2.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)

                    radio_group = QtWidgets.QButtonGroup(self)
                    radio_group.addButton(option1)
                    radio_group.addButton(option2)

                    self._style.set_variable_radio_button_initial(option1)
                    self._style.set_variable_radio_button_initial(option2)

                    self._symbols[1][x] = (label, option1, option2)

        formatted = {}  # used to preserve functions
        keys = list(self._symbols[0].keys())
        for y in keys:
            formatted[y] = function_convert(self._symbols[0][y][1].text())  # lets functions be inside of variables
            for x in formatted[y]:
                # checks if the character is in one of the accepted lists
                if x in symbols.accepted_variables:
                    index_2 = 0
                    temp.add(x)
                elif x in symbols.accepted_constants:
                    index_2 = 1
                    temp.add(x)
                else:
                    continue

                # adds the character's label and line edit to the correct dictionary in symbols
                if x not in self._symbols[index_2].keys():

                    if index_2 == 0:
                        label = QtWidgets.QLabel(f"{x} =", self)

                        text_box = CaretLineEdit(parent=self, caretSize=self._settings_user.caret_size, caretColor=QtGui.QColor(*self._settings_user.color_line_secondary))
                        text_box.setPlaceholderText(f"{x}")
                        self.__set_custom_context_menu(text_box)
                        self._symbols[0][x] = (label, text_box)

                    elif index_2 == 1:
                        label = QtWidgets.QLabel(f"{x}:", self)

                        option1 = QtWidgets.QRadioButton(f"{x}")
                        option1.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                        option2 = QtWidgets.QRadioButton(symbols.constant_preview[x] + "...")
                        option2.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                        option1.setChecked(True)

                        # displays the default answer if a radio button was selected
                        option1.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)  # used to see if a new value was selected
                        option2.toggled.connect(lambda checked: self.__box_answer_set(self._settings_user.answer_default) if checked else None)

                        radio_group = QtWidgets.QButtonGroup(self)
                        radio_group.addButton(option1)
                        radio_group.addButton(option2)

                        self._style.set_variable_radio_button_initial(option1)
                        self._style.set_variable_radio_button_initial(option2)

                        self._symbols[1][x] = (label, option1, option2)

        # deletes all variables not in the text box
        for index in range(len(self._symbols)):
            keys_to_delete = [x for x in self._symbols[index] if x not in temp]
            for x in keys_to_delete:
                del self._symbols[index][x]

        self._fill_variables()  # adds all variables found in the variable box

        if not activated:
            self.__box_answer_set(self._settings_user.answer_default)  # clears the previous answer

    def __update_self(self) -> None:
        """
        Updates the position of everything in MainWindow.
        """

        self.__button_settings.move(self.width() - self._settings_user.title_bar_settings_width - self._settings_user.title_bar_settings_separate - (3 * self._settings_user.title_bar_button_width), self._settings_user.title_bar_settings_spacing)
        self.__button_settings.resize(self._settings_user.title_bar_settings_width, self._settings_user.title_bar_height - (2 * self._settings_user.title_bar_settings_spacing))

        box_answer_height = int(self._settings_user.box_answer_height_scale * (self.height() - self._settings_user.title_bar_height - (3 * self._settings_user.box_padding)))

        box_text_y1 = self._settings_user.box_padding + self._settings_user.title_bar_height
        box_text_height = self.height() - box_answer_height - (self._settings_user.box_padding * 3) - self._settings_user.title_bar_height - self._settings_user.bar_button_height + self._settings_user.box_border
        box_text_x1 = self._settings_user.box_padding
        box_text_width = int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5))

        # text box
        self._box_text.move(box_text_x1, box_text_y1)
        self._box_text.resize(box_text_width, box_text_height)  # 1.5 is used so the gap to the right of the box isn't too big

        self._bar_answer.move(self._settings_user.box_padding, box_text_y1 + box_text_height - self._settings_user.box_border)
        self._bar_answer.resize(self._settings_user.bar_button_width, self._settings_user.bar_button_height)

        self._bar_format.move(self._settings_user.box_padding + self._settings_user.bar_button_width - self._settings_user.box_border, box_text_y1 + box_text_height - self._settings_user.box_border)
        self._bar_format.resize(self._settings_user.bar_button_width, self._settings_user.bar_button_height)

        self._bar_spacer.move(self._settings_user.box_padding + self._settings_user.bar_button_width - self._settings_user.box_border, box_text_y1 + box_text_height - self._settings_user.box_border)
        self._bar_spacer.resize(box_text_x1 + box_text_width - (self._settings_user.box_padding + self._settings_user.bar_button_width - self._settings_user.box_border), self._settings_user.bar_button_height)

        # answer box
        self._box_answer.move(self._settings_user.box_padding, self.height() - self._settings_user.box_padding - box_answer_height)
        self._box_answer.resize(int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), box_answer_height)

        # answer format label
        self._box_answer_format_label.move(self._settings_user.box_padding + self._settings_user.answer_format_indent, self.height() - self._settings_user.box_padding - box_answer_height)

    def __box_answer_set(self, text: str, displayed_text: str = None) -> None:
        """
        Sets the answer button to the display the given text.

        Used for displaying errors and the default answer.
        """

        if displayed_text is None:
            displayed_text = text

        self._box_answer.setIcon(QtGui.QIcon())  # removes the image
        self._box_answer_format_label.setText('')  # removes the format icon
        self._box_answer.setText(displayed_text)  # sets the text of the button

        self._style.set_button_format_visibility(self._bar_answer, self._bar_format, False)

        self.__answer = text
        self.__answer_temp = text

    def __set_custom_context_menu(self, widget) -> None:
        """
        Sets the context menu stylesheet.
        """

        def context_menu_event(event):
            menu = widget.createStandardContextMenu()
            self._style.set_context_menu(menu)
            menu.exec(event.globalPos())

        widget.contextMenuEvent = context_menu_event

    def __update_colors(self, is_displaying_answer) -> None:
        """
        Updates the stylesheets of everything in MainWindow.
        """

        self.repaint()  # updates the colors for the title bar and background
        self._text_update(True)  # updates the colors in the variables tab

        self._update_colors_control()  # updates the colors of stuff in the title bar
        self._style.set_button_format_visibility(self._bar_answer, self._bar_format, is_displaying_answer)  # updates the color for the answer button

        self._style.set_button_settings(self.__button_settings)
        self._style.set_box_answer(self._box_answer)
        self._style.set_box_answer_format_label(self._box_answer_format_label)
        self._style.set_box_text(self._box_text)
        self._style.set_bar_blank(self._bar_spacer)
        self._style.set_bar_format(self._bar_format)

    def __variable_formatting(self, symbols: tuple[dict, dict, dict]) -> dict:
        """
        Performs variable substitution, and checks for circularly defined variables.
        """

        self.__is_constant_value_used = False  # resets if a constant value was used

        temp1 = {}
        # adds all keys with their text to a new dict
        for index in range(len(symbols)):
            keys = list(symbols[index].keys())
            for key in keys:

                if index == 0:
                    temp1[key] = function_convert(symbols[index][key][1].text())

                    if temp1[key] == '':  # if the user did not define a variable, then it is equal to itself
                        temp1[key] = key

                elif index == 1:
                    if symbols[index][key][2].isChecked():
                        self.__is_constant_value_used = True  # keeps track if a constant value was used

        # performs chained variable substitution: a=b and b=5 -> a=5
        for x in temp1:

            if temp1[x] == x or not contains_substring(temp1[x], list(self._symbols[0].keys()) + list(self._symbols[1].keys())):
                continue

            temp2 = temp1.copy()
            for y in temp2:
                for z in temp2:

                    if temp2[z] == z or not contains_substring(temp2[z], list(self._symbols[0].keys()) + list(self._symbols[1].keys())):
                        continue

                    temp1[z] = temp1[z].replace(y, f"({temp2[y]})")

        error.circularly_defined(temp1)  # checks for circularly defined variables

        return temp1

    def __generate_value_used_bool(self) -> dict[str, bool]:
        """
        Returns a dictionary of True or False values depending on if the constant's value was used.
        """

        constant_symbol_used = {}
        for key in list(self._symbols[1].keys()):
            if self._symbols[1][key][1].isChecked():  # checks if a constant value was used
                constant_symbol_used[key] = True
            else:
                constant_symbol_used[key] = False

        return constant_symbol_used

    def __box_text_focus_event(self, event):
        if event.reason() == QtCore.Qt.FocusReason.MouseFocusReason:
            if QtWidgets.QApplication.activeWindow() is not None:
                cursor = self._box_text.textCursor()
                cursor.clearSelection()
                self._box_text.setTextCursor(cursor)
        CaretTextEdit.focusOutEvent(self._box_text, event)  # calls the original focusOutEvent method

    def __copy(self) -> None:
        """
        Lets the user copy the answer by clicking the answer box.
        """

        if self.__answer_temp == self._settings_user.answer_default or self.__answer_temp[:6] == "Error:":
            pyperclip.copy(self.__answer_temp)
            return

        if self.__flip_type_toggle:
            if self._settings_user.answer_copy == "Image":
                self._op.copy_image(get_data_path("latex_exact.png"))
                return
            else:
                string = self.__solution.get_exact_copy()
        else:
            if self._settings_user.answer_copy == "Image":
                self._op.copy_image(get_data_path("latex_approximate.png"))
                return
            else:
                string = self.__solution.get_approximate_copy()

        pyperclip.copy(string)  # copies answer to clipboard

    def resizeEvent(self, event):
        self._update_control()
        self.__update_self()
        self._update_multi()

    def closeEvent(self, event):
        """
        Closes all windows if the main window is closed.
        """
