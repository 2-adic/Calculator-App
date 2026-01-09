from PyQt6 import QtCore, QtWidgets

from core.style import Settings, Style
from core.system_settings import OperatingSystem
from ui.views.ControlWindow import ControlWindow


class SettingsWindow(ControlWindow):
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        ControlWindow.__init__(self, settings, style, op)

        self._set_title(self._settings_user.window_title_settings)
        self._set_size_min(*self._settings_user.window_size_min_settings)

        self._settings_user.window_border_radius_save = self._op.get_window_border_radius()  # sets the shape of the window corners

        self.answer_display = None

        # Settings Menu -----------------------------------------------------------------------------------------

        defaults: list[int] = self._settings_user.load_settings()

        settings_list = (
            ("General", (
                # function, default option number, setting label, option 1, option2, ... option n
                (self.__formatting_commas, defaults[0], "Number Format", "Standard", "Commas"),
            )),

            ("Answer", (
                (self.__format_display, defaults[1], "Display Format", "Image", "LaTeX", "Text"),
                (self.__format_copy, defaults[2], "Copy Format", "Image", "LaTeX", "Text"),
            )),

            ("Colors", (
                (self.__color_preset, defaults[3], "Appearance", "Gray", "Blue", "Pink"),
                (self.__text_color, defaults[4], "Text Color", "White", "Black"),
            )),
        )

        self.__settings_list = settings_list
        self.__button_storage: list[QtWidgets.QPushButton] = []  # keeps track of buttons for future stylesheet changes

        self.__menu = QtWidgets.QWidget(self)

        main_layout = QtWidgets.QVBoxLayout(self.__menu)
        button_layout = QtWidgets.QHBoxLayout()  # layout for the section buttons

        # section button spacers
        top_spacer = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)

        button_layout.addItem(left_spacer)  # adds spacing to the left of the top section buttons

        top_button_group = QtWidgets.QButtonGroup(self)
        stacked_widget = QtWidgets.QStackedWidget()
        self._style.set_stacked_widget(stacked_widget)

        self.__list_functions = {}
        for i, section in enumerate(settings_list):
            button = QtWidgets.QPushButton(section[0])  # creates the section buttons
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.setCheckable(True)  # allows the buttons to be toggleable
            button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed))

            if i == 0:  # the first section is selected by default
                button.setChecked(True)

            button_layout.addWidget(button)
            top_button_group.addButton(button)  # adds the button to a group so only one is active at a time

            container = self.__sections_initialize(section[1])  # gets the container for all the settings in a specific section
            stacked_widget.addWidget(container)
            button.clicked.connect(lambda checked, widget=container: stacked_widget.setCurrentWidget(widget))  # allows the section buttons to change the container

        button_layout.addItem(right_spacer)  # adds spacing to the right of the top section buttons

        # adds the apply button
        self.__button_apply = QtWidgets.QPushButton("Apply")  # keeps track of button for future stylesheet changes
        self.__button_apply.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__button_apply)

        # main_layout
        main_layout.addItem(top_spacer)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(stacked_widget)

        main_layout.addLayout(layout)

    def open_window(self, position: tuple[int, int]) -> None:
        """
        Sets the position of the window on the user's screen.
        """
        self._set_geometry(*(position + self._settings_user.window_start_size_settings))
        self._window_normal()  # takes the window out of its special states
        self.raise_()  # focuses the window to the front

        self.show()

    def connect_button_apply(self, function) -> None:
        self.__button_apply.clicked.connect(function)

    def update_settings(self) -> None:
        """
        Refreshes the windows to apply the new settings.
        """

        # activates the functions for all selected buttons
        for button in self.__button_storage:
            if button.isChecked():
                label = button.text()
                function = self.__list_functions[button]
                function(label)

        self.__update_colors()

    def __sections_initialize(self, settings_list) -> QtWidgets.QWidget:
        """
        Creates the container for each section in the settings.
        """

        section_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        for function, default_option, setting_name, *options in settings_list:
            h_layout = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(setting_name)

            h_layout.addWidget(label)
            h_layout.addStretch()

            button_group = QtWidgets.QButtonGroup(self)  # a button group lets the user select one option per setting
            button_group.setExclusive(True)  # makes it so only one button can be selected at a time

            for i, option in enumerate(options):  # creates a button for each option
                button = QtWidgets.QPushButton(option)
                button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                self.__button_storage.append(button)
                self.__list_functions[button] = function
                button.setCheckable(True)
                button_group.addButton(button)

                if i == default_option:  # logic for if the button is the default one
                    button.setChecked(True)  # visually shows the default button as selected
                    button.click()  # activates the button to run its logic

                h_layout.addWidget(button)

            layout.addLayout(h_layout)

        layout.addStretch()
        section_widget.setLayout(layout)

        # creates a scroll area and sets the section widget as its widget
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(section_widget)
        scroll_area.setWidgetResizable(True)

        # creates a container widget for the scroll area
        container_widget = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout()
        container_layout.addWidget(scroll_area)
        container_widget.setLayout(container_layout)

        return container_widget

    def __update_colors(self) -> None:
        """
        Updates the colors for the SettingWindow.
        """

        self.repaint()  # updates the colors for the title bar and background

        self._update_colors_control()  # updates the colors of stuff in the title bar

        self._style.set_button_apply(self.__button_apply)
        self._style.set_button_storage(self.__button_storage)
        self._style.set_menu(self.__menu)

    def __button_clicked(self, label: str) -> None:
        """
        Used to test if the settings buttons work.
        """

        # print("This setting currently does nothing")

    def __formatting_commas(self, label: str) -> None:
        """
        Toggles the comma formatting for numbers.
        """

        if label == "Standard":
            self._settings_user.use_commas = False
        else:
            self._settings_user.use_commas = True

    def __format_display(self, label: str) -> None:
        """
        Sets the format that the answer will display in.
        """

        self._settings_user.answer_display = label

    def __format_copy(self, label: str) -> None:
        """
        Sets the format that the answer be copied as.
        """

        self._settings_user.answer_copy = label

    def __color_preset(self, label: str) -> None:
        """
        Lets the user choose between multiple color themes.
        """

        if label == "Gray":
            self._style.set_gray()

        elif label == "Blue":
            self._style.set_blue()

        else:
            self._style.set_pink()

    def __text_color(self, label: str) -> None:
        if label == "White":
            self._settings_user.color_text = 255, 255, 255

        else:
            self._settings_user.color_text = 0, 0, 0

        self._settings_user.color_latex = self._settings_user.color_text

    def __update_self(self) -> None:
        """
        Updates the position of everything in SettingsWindow.
        """

        self.__menu.move(self._settings_user.box_padding, self._settings_user.title_bar_height + self._settings_user.box_padding)
        self.__menu.resize(self.width() - (2 * self._settings_user.box_padding), self.height() - self._settings_user.title_bar_height - (2 * self._settings_user.box_padding))

    def resizeEvent(self, event):
        self._update_control()
        self.__update_self()

    def closeEvent(self, event):
        self._settings_user.save_settings(self.__button_storage, self.__settings_list)
