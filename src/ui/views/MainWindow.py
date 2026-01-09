from PIL import Image
import pyperclip
from PyQt6 import QtCore, QtGui, QtWidgets

from core.files import path
from core.solve import Solve
from core.style import Settings, Style
import core.symbols as symbols
from core.system_settings import OperatingSystem, get_data_path
from ui.common.CaretTextEdit import CaretTextEdit
from ui.common.WrapTextButton import WrapTextButton
from ui.views.ControlWindow import ControlWindow
from ui.components.Sidebar import Sidebar


class MainWindow(ControlWindow):
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        ControlWindow.__init__(self, settings, style, op)

        # window properties
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
        self.__solve = None
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
        self._box_text = CaretTextEdit(parent=self, caretSize=self._settings_user.caret_size, setText="", defaultText="", tag="input")
        self._box_text.focusOutEvent = self.__box_text_focus_event

        self._bar_spacer = QtWidgets.QWidget(self)  # adds a blank space to the right of the bar buttons

        self._bar_answer = QtWidgets.QPushButton("Answer", self)  # the button that lets the user compute the answer
        self._bar_answer.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._bar_answer.clicked.connect(lambda: self.__get_answer())

        self._bar_format = QtWidgets.QPushButton("Format", self)  # the button that changes the format of the answer
        self._bar_format.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._bar_format.clicked.connect(self.__flip_type)
        self._style.set_button_format_visibility(self._bar_answer, self._bar_format, False)

        # sidebar
        self.__sidebar = Sidebar(self._settings_user, self._style, self._op, self._box_text, self)

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
            self.__get_answer(self.__flip_type_toggle)

    def __get_answer(self, stop_format_reset: bool | None = None) -> None:
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
            self.__solve = Solve(text, self.__sidebar.terms(), self._settings_user.answer_display, self._settings_user.answer_copy, self._settings_user.use_commas, self._settings_user.color_latex, self._settings_user.latex_image_dpi)
            self.__solve.print()  # shows the before and after expressions (for testing purposes)
            self.__answer = self.__solve.get_exact()

            if self.__solve.uses_constant_literal():  # hides the format button if a constant value was used
                self._style.set_button_format_visibility(self._bar_answer, self._bar_format, False)

            self.__flip_type()

        except Exception as error:
            self.__box_answer_set(f"Error: {error}", f"Error:\n{error}")  # displays the error
            print(f"Error: {error}")

    def __flip_type(self) -> None:
        """
        Flips the answer format between decimal and exact.
        """

        self._box_answer.setText('')
        self._box_answer.setIcon(QtGui.QIcon())

        # uses answer_temp to save the answer
        if self.__flip_type_toggle or self.__solve.uses_constant_literal():
            self.__answer_temp = self.__solve.get_approximate()  # turns the answer into its decimal format
            image_path = self.__answer_image_path_approximate
            self._box_answer_format_label.setText('≈')
        else:
            self.__answer_temp = self.__answer  # returns the original answer
            image_path = self.__answer_image_path_exact
            self._box_answer_format_label.setText('=')

        self.__flip_type_toggle = not self.__flip_type_toggle  # keeps track of which format is being displayed

        if self.__solve.is_text_used():
            self._box_answer.setText(self.__answer_temp)

        else:
            image = Image.open(image_path)
            icon = QtGui.QIcon(image_path)
            self._box_answer.setIcon(icon, image.width / image.height)

        self.__update_layout()

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

    def __box_text_focus_event(self, event: QtGui.QFocusEvent) -> None:
        """
        Clears text selection when the text box loses focus via mouse click.
        This matches the behavior of line edits, which remove highlighting when a user clicks off.
        """

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
                string = self.__solve.get_exact_copy()
        else:
            if self._settings_user.answer_copy == "Image":
                self._op.copy_image(get_data_path("latex_approximate.png"))
                return
            else:
                string = self.__solve.get_approximate_copy()

        pyperclip.copy(string)  # copies answer to clipboard

    def __update_colors(self, is_displaying_answer: bool) -> None:
        """
        Updates the stylesheets of everything in MainWindow.
        """

        self.repaint()  # updates the colors for the title bar and background

        self._update_colors_control()  # updates the colors of stuff in the title bar
        self._style.set_button_format_visibility(self._bar_answer, self._bar_format, is_displaying_answer)  # updates the color for the answer button

        self._style.set_button_settings(self.__button_settings)
        self._style.set_box_answer(self._box_answer)
        self._style.set_box_answer_format_label(self._box_answer_format_label)
        self._style.set_box_text(self._box_text)
        self._style.set_bar_blank(self._bar_spacer)
        self._style.set_bar_format(self._bar_format)

        # sidebar
        self.__sidebar.update_colors()

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

        # sidebar
        self.__sidebar.resize(int((self.width() * (1 - self._settings_user.box_width_left)) - (self._settings_user.box_padding * 1.5)), self.height() - (self._settings_user.title_bar_height + (self._settings_user.box_padding * 2)))
        self.__sidebar.move((self._settings_user.box_padding * 2) + int((self.width() * self._settings_user.box_width_left) - (self._settings_user.box_padding * 1.5)), self._settings_user.box_padding + self._settings_user.title_bar_height)

    def __update_layout(self) -> None:
        """
        Updates the layouts of MainWindow and everything within it.
        """

        self._update_control()
        self.__update_self()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.__update_layout()
