from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class Settings:
    def __init__(self):
        # Window ------------------------------------------------------------------------------------------------

        self.__window_start_size_main = (
            100,  # initial x position
            100,  # initial y position
            800,  # initial x size
            600  # initial y size
        )

        self.__window_settings_scale = .8  # number that the settings window's dimensions will be scaled by
        self.__window_start_size_settings = (
            int(self.__window_start_size_main[2] * self.__window_settings_scale),  # initial x size
            int(self.__window_start_size_main[3] * self.__window_settings_scale)  # initial y size
        )

        self.__widget_resize_size = 5  # thickness of the resizing widgets
        self.__window_size_min_main = 650, 450  # min size of the main window
        self.__window_size_min_settings = int(self.window_size_min_main[0] * self.__window_settings_scale), int(self.window_size_min_main[1] * self.__window_settings_scale)  # min size of the settings window
        self.__window_border_radius = 0
        self.__window_border_radius_save = self.__window_border_radius

        # title bar
        self.__title_bar_height = 22  # height of the title bar
        self.__title_bar_button_width = int(1.5 * self.__title_bar_height)  # width of the title bar buttons
        self.__title_bar_settings_icon_scale = .8  # the size of the icon relative to the button size
        self.__title_bar_settings_spacing = int(self.__title_bar_height / 11)  # spacing between the button and the top / bottom of the title bar
        self.__title_bar_settings_width = self.__title_bar_height - (2 * self.__title_bar_settings_spacing)  # width of the settings button
        self.__title_bar_settings_separate = 20  # spacing between the settings button, and the other buttons

        self.__window_title_main = 'Calculator'
        self.__window_title_settings = 'Settings'
        self.__window_title_position = (
            int(5 + (self.__title_bar_height / 2) - (22 / 2)),  # x position
            int(3 + (self.__title_bar_height / 2) - (22 / 2))  # y position
        )

        # Testing Buttons ---------------------------------------------------------------------------------------

        self.__test_button_width = 80  # width of the buttons
        self.__test_button_height = 40  # height of the buttons

        # Boxes -------------------------------------------------------------------------------------------------

        # general
        self.__box_width_left = 1 / 2  # fraction of screen width
        self.__box_padding = 20  # amount of spacing between the boxes
        self.__box_border = 4  # the border thickness for all widgets
        self.__box_border_radius = self.__box_border * 2  # the curvature of the border corners
        self.__caret_size = 2

        # text box
        self.__bar_button_width = 80  # width of the bar buttons under the text box
        self.__bar_button_height = 40  # height of the bar buttons under the text box

        # answer box
        self.__answer_default = 'Answer'
        self.__answer_format_size = 20  # the size of the symbol that shows the current selected answer format
        self.__answer_format_indent = 10  # the distance from the format symbol and the left side of the answer box

        self.__box_answer_height_scale = 2 / 5  # fraction of screen height
        self.__box_answer_padding = 20  # distance from the image to the border of the answer box
        self.__latex_image_dpi = 800

        # multi box
        self.__content_margin = 10  # distance between the scroll content, and the border
        self.__select_height = 50  # height of the selector buttons
        self.__symbols_button_width = 50, 120  # width of the copy buttons within the symbols tab, a tuple is used for the width of different sections
        self.__symbols_button_height = 50  # height of the copy buttons, all buttons have the same height
        self.__radio_button_radius = 13  # the radius of the radio buttons
        self.__radio_button_border_radius = int(self.__radio_button_radius / 2) + 2  # the border radius of the radio buttons

        # buttons
        self.__button_text_hover_raise = 5  # the height text is raised when a button is being hovered

        # Colors ------------------------------------------------------------------------------------------------
        # all int values in this section can be from 0 to 255

        # background
        self.__color_background = None
        self.__color_background_transparent_amount = 150  # the transparency value of the background: lower means more transparent
        self.__color_background_blurred = True  # blurs the background if it is transparent,

        # text
        self.__color_text = None
        self.__color_text_highlight_active = None
        self.__color_text_highlight_inactive = None
        self.__color_text_secondary = None

        # title bar
        self.__color_title_bar = None
        self.__color_title_bar_text = None
        self.__color_title_bar_button_hover = None
        self.__color_title_bar_button_press = None
        self.__color_title_bar_button_exit_hover = 242, 63, 66
        self.__color_title_bar_button_exit_press = 241, 112, 122

        # boxes
        self.__color_box_background = None
        self.__color_box_hover = None
        self.__color_box_selected = None
        self.__color_box_border = None

        # other
        self.__color_line_primary = None
        self.__color_line_secondary = None
        self.__color_scrollbar_background = None
        self.__color_latex = None

        # Other -------------------------------------------------------------------------------------------------

        self.__use_degrees = False
        self.__use_commas = False
        self.__answer_display = None
        self.__answer_copy = None

    def save_settings(self, buttons, settings_list):
        """
        Saves the settings to a txt file.
        """

        # gets the buttons that are selected
        selected_buttons = []
        for button in buttons:
            if button.isChecked():
                selected_buttons.append(button)

        # finds the button number for each setting and saves it to a string
        i = 0
        save = ''
        for section in settings_list:
            for function, default, setting_name, *options in section[1]:
                button = selected_buttons[i]
                text = button.text()
                save += f'{options.index(text)} '

                i += 1

        save = save[:-1]  # removes the last space

        # saves the settings to the txt file
        with open('settings.txt', 'w') as file:
            file.write(save)

    def load_settings(self) -> list:
        """
        Loads the settings from a txt file. This is used when the program is launched.
        """

        try:
            # gets the saved settings from the file
            with open('settings.txt', 'r') as file:
                line = file.readline()

            # turns the string into a list of numbers
            line = line.split(' ')
            defaults = []
            for num in line:
                defaults.append(int(num))

            return defaults

        except Exception as error:
            print('Error: could not load settings, default settings will be used instead.')
            return self.__default_settings()

    def __default_settings(self) -> list:
        """
        Converts all settings to their default values.
        """

        return [0, 0, 0, 2, 0, 0]

    @property
    def window_start_size_main(self) -> tuple[int, int, int, int]:
        return self.__window_start_size_main

    @window_start_size_main.setter
    def window_start_size_main(self, value: tuple[int, int, int, int]) -> None:
        self.__window_start_size_main = value

    @property
    def window_settings_scale(self) -> float:
        return self.__window_settings_scale

    @window_settings_scale.setter
    def window_settings_scale(self, value: float) -> None:
        self.__window_settings_scale = value

    @property
    def window_start_size_settings(self) -> tuple[int, int]:
        return self.__window_start_size_settings

    @window_start_size_settings.setter
    def window_start_size_settings(self, value: tuple[int, int]) -> None:
        self.__window_start_size_settings = value

    @property
    def widget_resize_size(self) -> int:
        return self.__widget_resize_size

    @widget_resize_size.setter
    def widget_resize_size(self, value: int) -> None:
        self.__widget_resize_size = value

    @property
    def window_size_min_main(self) -> tuple[int, int]:
        return self.__window_size_min_main

    @window_size_min_main.setter
    def window_size_min_main(self, value: tuple[int, int]) -> None:
        self.__window_size_min_main = value

    @property
    def window_size_min_settings(self) -> tuple[int, int]:
        return self.__window_size_min_settings

    @window_size_min_settings.setter
    def window_size_min_settings(self, value: tuple[int, int]) -> None:
        self.__window_size_min_settings = value

    @property
    def window_border_radius(self) -> int:
        return self.__window_border_radius

    @window_border_radius.setter
    def window_border_radius(self, value: int) -> None:
        self.__window_border_radius = value

    @property
    def window_border_radius_save(self) -> int:
        return self.__window_border_radius_save

    @window_border_radius_save.setter
    def window_border_radius_save(self, value: int) -> None:
        self.window_border_radius = value  # sets this variable to the same value
        self.__window_border_radius_save = value

    @property
    def title_bar_height(self) -> int:
        return self.__title_bar_height

    @title_bar_height.setter
    def title_bar_height(self, value: int) -> None:
        self.__title_bar_height = value

    @property
    def title_bar_button_width(self) -> int:
        return self.__title_bar_button_width

    @title_bar_button_width.setter
    def title_bar_button_width(self, value: int) -> None:
        self.__title_bar_button_width = value

    @property
    def title_bar_settings_icon_scale(self) -> float:
        return self.__title_bar_settings_icon_scale

    @title_bar_settings_icon_scale.setter
    def title_bar_settings_icon_scale(self, value: float) -> None:
        self.__title_bar_settings_icon_scale = value

    @property
    def title_bar_settings_spacing(self) -> int:
        return self.__title_bar_settings_spacing

    @title_bar_settings_spacing.setter
    def title_bar_settings_spacing(self, value: int) -> None:
        self.__title_bar_settings_spacing = value

    @property
    def title_bar_settings_width(self) -> int:
        return self.__title_bar_settings_width

    @title_bar_settings_width.setter
    def title_bar_settings_width(self, value: int) -> None:
        self.__title_bar_settings_width = value

    @property
    def title_bar_settings_separate(self) -> int:
        return self.__title_bar_settings_separate

    @title_bar_settings_separate.setter
    def title_bar_settings_separate(self, value: int) -> None:
        self.__title_bar_settings_separate = value

    @property
    def window_title_main(self) -> str:
        return self.__window_title_main

    @window_title_main.setter
    def window_title_main(self, value: str) -> None:
        self.__window_title_main = value

    @property
    def window_title_settings(self) -> str:
        return self.__window_title_settings

    @window_title_settings.setter
    def window_title_settings(self, value: str) -> None:
        self.__window_title_settings = value

    @property
    def window_title_position(self) -> tuple[int, int]:
        return self.__window_title_position

    @window_title_position.setter
    def window_title_position(self, value: tuple[int, int]) -> None:
        self.__window_title_position = value

    @property
    def test_button_width(self) -> int:
        return self.__test_button_width

    @test_button_width.setter
    def test_button_width(self, value: int) -> None:
        self.__test_button_width = value

    @property
    def test_button_height(self) -> int:
        return self.__test_button_height

    @test_button_height.setter
    def test_button_height(self, value: int) -> None:
        self.__test_button_height = value

    @property
    def box_width_left(self) -> float:
        return self.__box_width_left

    @box_width_left.setter
    def box_width_left(self, value: float) -> None:
        self.__box_width_left = value

    @property
    def box_padding(self) -> int:
        return self.__box_padding

    @box_padding.setter
    def box_padding(self, value: int) -> None:
        self.__box_padding = value

    @property
    def box_border(self) -> int:
        return self.__box_border

    @box_border.setter
    def box_border(self, value: int) -> None:
        self.__box_border = value

    @property
    def box_border_radius(self) -> int:
        return self.__box_border_radius

    @box_border_radius.setter
    def box_border_radius(self, value: int) -> None:
        self.__box_border_radius = value

    @property
    def caret_size(self) -> int:
        return self.__caret_size

    @caret_size.setter
    def caret_size(self, value: int) -> None:
        self.__caret_size = value

    @property
    def bar_button_width(self) -> int:
        return self.__bar_button_width

    @bar_button_width.setter
    def bar_button_width(self, value: int) -> None:
        self.__bar_button_width = value

    @property
    def bar_button_height(self) -> int:
        return self.__bar_button_height

    @bar_button_height.setter
    def bar_button_height(self, value: int) -> None:
        self.__bar_button_height = value

    @property
    def answer_default(self) -> str:
        return self.__answer_default

    @answer_default.setter
    def answer_default(self, value: str) -> None:
        self.__answer_default = value

    @property
    def answer_format_size(self) -> int:
        return self.__answer_format_size

    @answer_format_size.setter
    def answer_format_size(self, value: int) -> None:
        self.__answer_format_size = value

    @property
    def answer_format_indent(self) -> int:
        return self.__answer_format_indent

    @answer_format_indent.setter
    def answer_format_indent(self, value: int) -> None:
        self.__answer_format_indent = value

    @property
    def box_answer_height_scale(self) -> float:
        return self.__box_answer_height_scale

    @box_answer_height_scale.setter
    def box_answer_height_scale(self, value: float) -> None:
        self.__box_answer_height_scale = value

    @property
    def box_answer_padding(self) -> int:
        return self.__box_answer_padding

    @box_answer_padding.setter
    def box_answer_padding(self, value: int) -> None:
        self.__box_answer_padding = value

    @property
    def latex_image_dpi(self) -> int:
        return self.__latex_image_dpi

    @latex_image_dpi.setter
    def latex_image_dpi(self, value: int) -> None:
        self.__latex_image_dpi = value

    @property
    def content_margin(self) -> int:
        return self.__content_margin

    @content_margin.setter
    def content_margin(self, value: int) -> None:
        self.__content_margin = value

    @property
    def select_height(self) -> int:
        return self.__select_height

    @select_height.setter
    def select_height(self, value: int) -> None:
        self.__select_height = value

    @property
    def symbols_button_width(self) -> tuple[int, int]:
        return self.__symbols_button_width

    @symbols_button_width.setter
    def symbols_button_width(self, value: tuple[int, int]) -> None:
        self.__symbols_button_width = value

    @property
    def symbols_button_height(self) -> int:
        return self.__symbols_button_height

    @symbols_button_height.setter
    def symbols_button_height(self, value: int) -> None:
        self.__symbols_button_height = value

    @property
    def radio_button_radius(self) -> int:
        return self.__radio_button_radius

    @radio_button_radius.setter
    def radio_button_radius(self, value: int) -> None:
        self.__radio_button_radius = value

    @property
    def radio_button_border_radius(self) -> int:
        return self.__radio_button_border_radius

    @radio_button_border_radius.setter
    def radio_button_border_radius(self, value: int) -> None:
        self.__radio_button_border_radius = value

    @property
    def button_text_hover_raise(self) -> int:
        return self.__button_text_hover_raise

    @button_text_hover_raise.setter
    def button_text_hover_raise(self, value: int) -> None:
        self.__button_text_hover_raise = value

    @property
    def color_background(self) -> tuple[int, int, int]:
        return self.__color_background

    @color_background.setter
    def color_background(self, value: tuple[int, int, int]) -> None:
        self.__color_background = value

    @property
    def color_background_transparent_amount(self) -> int:
        return self.__color_background_transparent_amount

    @color_background_transparent_amount.setter
    def color_background_transparent_amount(self, value: int) -> None:
        self.__color_background_transparent_amount = value

    @property
    def color_background_blurred(self) -> bool:
        return self.__color_background_blurred

    @color_background_blurred.setter
    def color_background_blurred(self, value: bool) -> None:
        self.__color_background_blurred = value

    @property
    def color_text(self) -> tuple[int, int, int]:
        return self.__color_text

    @color_text.setter
    def color_text(self, value: tuple[int, int, int]) -> None:
        self.__color_text = value

    @property
    def color_text_highlight_active(self) -> tuple[int, int, int]:
        return self.__color_text_highlight_active

    @color_text_highlight_active.setter
    def color_text_highlight_active(self, value: tuple[int, int, int]) -> None:
        self.__color_text_highlight_active = value

    @property
    def color_text_highlight_inactive(self) -> tuple[int, int, int]:
        return self.__color_text_highlight_inactive

    @color_text_highlight_inactive.setter
    def color_text_highlight_inactive(self, value: tuple[int, int, int]) -> None:
        self.__color_text_highlight_inactive = value

    @property
    def color_text_secondary(self) -> tuple[int, int, int]:
        return self.__color_text_secondary

    @color_text_secondary.setter
    def color_text_secondary(self, value: tuple[int, int, int]) -> None:
        self.__color_text_secondary = value

    @property
    def color_title_bar(self) -> tuple[int, int, int]:
        return self.__color_title_bar

    @color_title_bar.setter
    def color_title_bar(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar = value

    @property
    def color_title_bar_text(self) -> tuple[int, int, int]:
        return self.__color_title_bar_text

    @color_title_bar_text.setter
    def color_title_bar_text(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_text = value

    @property
    def color_title_bar_button_hover(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_hover

    @color_title_bar_button_hover.setter
    def color_title_bar_button_hover(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_hover = value

    @property
    def color_title_bar_button_press(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_press

    @color_title_bar_button_press.setter
    def color_title_bar_button_press(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_press = value

    @property
    def color_title_bar_button_exit_hover(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_exit_hover

    @color_title_bar_button_exit_hover.setter
    def color_title_bar_button_exit_hover(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_exit_hover = value

    @property
    def color_title_bar_button_exit_press(self) -> tuple[int, int, int]:
        return self.__color_title_bar_button_exit_press

    @color_title_bar_button_exit_press.setter
    def color_title_bar_button_exit_press(self, value: tuple[int, int, int]) -> None:
        self.__color_title_bar_button_exit_press = value

    @property
    def color_box_background(self) -> tuple[int, int, int]:
        return self.__color_box_background

    @color_box_background.setter
    def color_box_background(self, value: tuple[int, int, int]) -> None:
        self.__color_box_background = value

    @property
    def color_box_selected(self) -> tuple[int, int, int]:
        return self.__color_box_selected

    @color_box_selected.setter
    def color_box_selected(self, value: tuple[int, int, int]) -> None:
        self.__color_box_selected = value

    @property
    def color_box_border(self) -> tuple[int, int, int]:
        return self.__color_box_border

    @color_box_border.setter
    def color_box_border(self, value: tuple[int, int, int]) -> None:
        self.__color_box_border = value

    @property
    def color_box_hover(self) -> tuple[int, int, int]:
        return self.__color_box_hover

    @color_box_hover.setter
    def color_box_hover(self, value: tuple[int, int, int]) -> None:
        self.__color_box_hover = value

    @property
    def color_line_primary(self) -> tuple[int, int, int]:
        return self.__color_line_primary

    @color_line_primary.setter
    def color_line_primary(self, value: tuple[int, int, int]) -> None:
        self.__color_line_primary = value

    @property
    def color_line_secondary(self) -> tuple[int, int, int]:
        return self.__color_line_secondary

    @color_line_secondary.setter
    def color_line_secondary(self, value: tuple[int, int, int]) -> None:
        self.__color_line_secondary = value

    @property
    def color_scrollbar_background(self) -> tuple[int, int, int]:
        return self.__color_scrollbar_background

    @color_scrollbar_background.setter
    def color_scrollbar_background(self, value: tuple[int, int, int]) -> None:
        self.__color_scrollbar_background = value

    @property
    def color_latex(self) -> tuple[int, int, int]:
        return self.__color_latex

    @color_latex.setter
    def color_latex(self, value: tuple[int, int, int]) -> None:
        self.__color_latex = value

    @property
    def use_degrees(self) -> bool:
        return self.__use_degrees

    @use_degrees.setter
    def use_degrees(self, value: bool) -> None:
        self.__use_degrees = value

    @property
    def use_commas(self) -> bool:
        return self.__use_commas

    @use_commas.setter
    def use_commas(self, value: bool) -> None:
        self.__use_commas = value

    @property
    def answer_display(self) -> str:
        return self.__answer_display

    @answer_display.setter
    def answer_display(self, value: str) -> None:
        self.__answer_display = value

    @property
    def answer_copy(self) -> str:
        return self.__answer_copy

    @answer_copy.setter
    def answer_copy(self, value: str) -> None:
        self.__answer_copy = value


class Style:
    def __init__(self, settings: Settings):
        self.__settings = settings

    def set_gray(self) -> None:
        self.__settings.color_background = 49, 51, 56
        self.__settings.color_text_highlight_active = 70, 115, 156
        self.__settings.color_text_highlight_inactive = 176, 176, 176
        self.__settings.color_text_secondary = 35, 36, 41
        self.__settings.color_title_bar = 30, 31, 34
        self.__settings.color_title_bar_text = 148, 155, 164
        self.__settings.color_title_bar_button_hover = 45, 46, 51
        self.__settings.color_title_bar_button_press = 53, 54, 60
        self.__settings.color_box_background = 85, 88, 97
        self.__settings.color_box_hover = 81, 100, 117
        self.__settings.color_box_selected = 51, 75, 97
        self.__settings.color_box_border = 35, 36, 40
        self.__settings.color_line_primary = 41, 42, 47
        self.__settings.color_line_secondary = 49, 51, 56
        self.__settings.color_scrollbar_background = 63, 65, 72
        
    def set_blue(self) -> None:
        self.__settings.color_background = 49, 89, 153
        self.__settings.color_text_highlight_active = 47, 111, 130
        self.__settings.color_text_highlight_inactive = 98, 151, 156
        self.__settings.color_text_secondary = 40, 45, 46
        self.__settings.color_title_bar = 23, 37, 51
        self.__settings.color_title_bar_text = 88, 118, 168
        self.__settings.color_title_bar_button_hover = 32, 50, 69
        self.__settings.color_title_bar_button_press = 36, 57, 79
        self.__settings.color_box_background = 99, 106, 115
        self.__settings.color_box_hover = 98, 151, 156
        self.__settings.color_box_selected = 47, 111, 130
        self.__settings.color_box_border = self.__settings.color_title_bar
        self.__settings.color_line_primary = 15, 38, 71
        self.__settings.color_line_secondary = 19, 49, 92
        self.__settings.color_scrollbar_background = 59, 63, 69

    def set_pink(self) -> None:
        self.__settings.color_background = 206, 146, 141
        self.__settings.color_text_highlight_active = 191, 124, 119
        self.__settings.color_text_highlight_inactive = 215, 177, 168
        self.__settings.color_text_secondary = 61, 55, 55
        self.__settings.color_title_bar = 55, 33, 42
        self.__settings.color_title_bar_text = 153, 100, 96
        self.__settings.color_title_bar_button_hover = 74, 44, 56
        self.__settings.color_title_bar_button_press = 84, 50, 63
        self.__settings.color_box_background = 163, 143, 142
        self.__settings.color_box_hover = 215, 177, 168
        self.__settings.color_box_selected = 191, 124, 119
        self.__settings.color_box_border = 63, 39, 50
        self.__settings.color_line_primary = 74, 46, 59
        self.__settings.color_line_secondary = 92, 57, 73
        self.__settings.color_scrollbar_background = 105, 92, 91

    # ControlWindow --------------------------------------------------------------------------------

    def set_button_close(self, button) -> None:
        button.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
                border-top-right-radius: {self.__settings.window_border_radius}px;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_title_bar_button_exit_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_title_bar_button_exit_press};
            }}
            '''
        )

    def set_button_maximize(self, button) -> None:
        button.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_title_bar_button_press};
            }}
            '''
        )

    def set_button_minimize(self, button) -> None:
        button.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_title_bar_button_press};
            }}
            QPushButton::icon {{
                margin-bottom: -5px; 
            }}
            '''
        )

    def set_title_label(self, label) -> None:
        label.setStyleSheet(
            f'''
            color: rgb{self.__settings.color_title_bar_text};
            font-weight: bold;
            font-size: 11px;
            '''
        )

    def update_border_radius(self, remove_radius: bool, button) -> None:
        if remove_radius:
            self.__settings.window_border_radius = 0

        else:
            self.__settings.window_border_radius = self.__settings.window_border_radius_save

        self.set_button_close(button)

    # SettingWindow --------------------------------------------------------------------------------

    def set_stacked_widget(self, widget) -> None:
        widget.setStyleSheet(
            f'''
            * {{
                border: none;
            }}
            '''
        )

    def set_button_apply(self, button) -> None:
        button.setStyleSheet(
            f'''
            QPushButton {{ 
                max-width: 100px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_box_selected}
            }}
            '''
        )

    def set_button_storage(self, buttons) -> None:
        for button in buttons:
            button.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    width: 80px;
                }}
                '''
            )

    def set_menu(self, widget) -> None:
        widget.setStyleSheet(
            f'''
            QWidget {{
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                background-color: rgb{self.__settings.color_box_background};
                border-radius: {self.__settings.box_border_radius}px;
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            QPushButton {{
                width: 100px; 
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_box_hover};
                padding-top: -{self.__settings.button_text_hover_raise}px;
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
            }}
            QPushButton:checked {{
                background-color: rgb{self.__settings.color_box_selected};
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self.__settings.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self.__settings.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )

    # MainWindow -----------------------------------------------------------------------------------
    
    def set_context_menu(self, menu) -> None:
        menu.setStyleSheet(
            f'''
            QMenu {{
                background-color: rgb{self.__settings.color_box_background};
                border: 1px solid rgb{self.__settings.color_box_border};
                border-radius: 0px;
                color: white;
                font-size: 13px;
            }}
            QMenu::item::selected {{
                background-color: rgb{self.__settings.color_box_hover};
            }}
            QMenu::item:pressed {{
                background-color: rgb{self.__settings.color_box_selected};
            }}
            '''
        )
    
    def set_button_settings(self, button) -> None:
        button.setStyleSheet(
            f'''
            QPushButton {{
                background-color: transparent;
                border-radius: 3px
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_title_bar_button_hover};
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_title_bar_button_press}
            }}
            '''
        )

    def set_box_answer(self, wrap_button) -> None:
        button = wrap_button.button()
        label = wrap_button.label()

        button.setStyleSheet(
            f'''
            QPushButton {{
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-radius: {self.__settings.box_border_radius}px;
                background-color: rgb{self.__settings.color_box_background};
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_box_hover};
                padding-top: -{self.__settings.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_box_selected};
            }}
            '''
        )

        label.setStyleSheet(
            f'''
            QLabel {{
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            '''
        )
        
    def set_box_answer_format_label(self, label) -> None:
        label.setStyleSheet(
            f'''
            QLabel {{
                font-size: {self.__settings.answer_format_size}px;
                color: rgb{self.__settings.color_text}
            }}
            '''
        )

    def set_box_text(self, text_box) -> None:
        # changes the caret color
        text_box.caret_color = QColor(*self.__settings.color_line_secondary)
        text_box.background_color = QColor(*self.__settings.color_box_background)

        text_box.setStyleSheet(
            f'''
            QPlainTextEdit {{
                border-top: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-left: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-right: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                background-color: rgb{self.__settings.color_box_background};
                border-top-left-radius: {self.__settings.box_border_radius}px;
                border-top-right-radius: {self.__settings.box_border_radius}px;
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            QPlainTextEdit:active {{
                selection-background-color: rgb{self.__settings.color_text_highlight_active};
                selection-color: rgb{self.__settings.color_text};
            }}
            QPlainTextEdit:!active {{
                selection-background-color: rgb{self.__settings.color_text_highlight_inactive};
                selection-color: rgb{self.__settings.color_text};
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self.__settings.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self.__settings.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )

    def set_bar_blank(self, widget) -> None:
        widget.setStyleSheet(
            f'''
            QWidget {{
                border-bottom: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-right: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-bottom-right-radius: {self.__settings.box_border_radius}px;
                background-color: rgb{self.__settings.color_box_background};
            }}
            '''
        )

    def set_bar_format(self, button) -> None:
        button.setStyleSheet(
            f'''
            QPushButton {{
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-top-right-radius: {self.__settings.box_border_radius}px;
                background-color: rgb{self.__settings.color_box_background};
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_box_hover};
                padding-top: -{self.__settings.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_box_selected};
            }}
            '''
        )

    def set_button_format_visibility(self, bar_answer, bar_format, is_visible: bool) -> None:
        """
        Hides or shows the format button. Allows for correct visuals.

        :param is_visible: If the format button is going to be visible or not.
        """

        if is_visible:
            bar_format.show()
            bar_answer.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    border-bottom-left-radius: {self.__settings.box_border_radius}px;
                    background-color: rgb{self.__settings.color_box_background};
                    color: rgb{self.__settings.color_text};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    background-color: rgb{self.__settings.color_box_hover};
                    padding-top: -{self.__settings.button_text_hover_raise}px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self.__settings.color_box_selected};
                }}
                '''
            )

        else:
            bar_format.hide()
            bar_answer.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    border-bottom-left-radius: {self.__settings.box_border_radius}px;
                    border-top-right-radius: {self.__settings.box_border_radius}px;
                    background-color: rgb{self.__settings.color_box_background};
                    color: rgb{self.__settings.color_text};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    background-color: rgb{self.__settings.color_box_hover};
                    padding-top: -{self.__settings.button_text_hover_raise}px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self.__settings.color_box_selected};
                }}
                '''
            )

    # MultiWindow ----------------------------------------------------------------------------------

    def set_selector_label(self, label) -> None:
        label.setStyleSheet(
            f'''
            * {{
                border: none;
                color: rgb{self.__settings.color_text_secondary};
                font-size: 15px;
            }}
            '''
        )
    
    def set_scroll_area(self, scroll_area) -> None:
        scroll_area.setStyleSheet(
            f'''
            * {{
                border: none;
            }}
            QScrollArea {{
                background-color: rgb{self.__settings.color_box_background};
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                border-radius: 4px;
                background-color: rgb{self.__settings.color_scrollbar_background};
                width: 12px;
                margin: 4px 4px 4px 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgb{self.__settings.color_box_border};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical {{
                width: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            '''
        )
    
    def set_areas(self, test) -> None:

        # updates colors for the widgets in all the tabs
        for i, areas in enumerate(test):
            area = areas[0]

            area.setStyleSheet(
                f'''
                QLineEdit:active {{
                    selection-background-color: rgb{self.__settings.color_text_highlight_active};
                    selection-color: rgb{self.__settings.color_text};
                }}
                QLineEdit:!active {{
                    selection-background-color: rgb{self.__settings.color_text_highlight_inactive};
                    selection-color: rgb{self.__settings.color_text};
                }}
                QWidget {{
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    background-color: rgb{self.__settings.color_box_background};
                    border-bottom-left-radius: {self.__settings.box_border_radius}px;
                    border-bottom-right-radius: {self.__settings.box_border_radius}px;
                    color: rgb{self.__settings.color_text};
                    font-size: 15px;
                }}
                '''
            )

        # updates colors for the scroll areas in the notation tab
        for scroll_area in test[1][2]:
            self.set_scroll_area(scroll_area)

    def set_multibox_label(self, label) -> None:
        label.setStyleSheet(
            f'''
            QLabel {{
                font-weight: bold;
                font-size: 14px;
                color: rgb{self.__settings.color_text};
                border: none;
            }}
            '''
        )

    def set_line_primary(self, line) -> None:
        line.setStyleSheet(
            f'''
            QFrame {{
                border: 1px solid rgb{self.__settings.color_line_primary};
                background-color: rgb{self.__settings.color_line_primary};
                border-radius: 1px
            }}
            '''
        )

    def set_line_secondary(self, line) -> None:
        line.setStyleSheet(
            f'''
            background-color: rgb{self.__settings.color_line_secondary};
            border-radius: 1px
            '''
        )

    def set_notation(self, labels, lines, buttons) -> None:

        # updates the label colors in the notation tab
        for label in labels:
            self.set_multibox_label(label)

        # updates the line colors in the notation tab
        for line in lines:
            self.set_line_primary(line)

        # updates the button colors in the notation tab
        for button in buttons:
            button.setStyleSheet(
                f'''
                QPushButton {{
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    border-radius: {self.__settings.box_border_radius}px;
                }}
                QPushButton:hover {{
                    background-color: rgb{self.__settings.color_box_hover};
                    padding-top: -{self.__settings.button_text_hover_raise}px;
                }}
                QPushButton:pressed {{
                    background-color: rgb{self.__settings.color_box_selected};
                }}
                '''
            )
        
    def set_variable_radio_button_initial(self, radio_button) -> None:
        radio_button.setStyleSheet(
            f'''
            QRadioButton::indicator {{
                width: {self.__settings.radio_button_radius}px;
                height: {self.__settings.radio_button_radius}px;
                border-radius: {self.__settings.radio_button_border_radius}px;
                border: 2px solid rgb{self.__settings.color_box_border};
                background-color: rgb{self.__settings.color_box_background};
            }}
            QRadioButton::indicator:hover {{
                background-color: rgb{self.__settings.color_box_hover};
            }}
            QRadioButton::indicator:checked {{
                background-color: rgb{self.__settings.color_box_selected};
            }}
            '''
        )
        
    def set_variable_radio_button(self, symbols) -> None:

        for i, section in enumerate(symbols):
            # updates the caret colors for the line edits
            if i == 0:
                for key in list(section.keys()):
                    line_edit = section[key][1]
                    line_edit.caret_color = QColor(*self.__settings.color_line_secondary)
                    line_edit.background_color = QColor(*self.__settings.color_box_background)

            # updates the colors for the constant's radio buttons
            if i == 1:
                for key in list(section.keys()):
                    element = section[key]

                    for j, button in enumerate(element):
                        if j > 0:
                            button.setStyleSheet(
                                f'''
                                QRadioButton::indicator {{
                                    border-radius: 6px;
                                    border: 2px solid rgb{self.__settings.color_box_border};
                                    background-color: rgb{self.__settings.color_box_background};
                                }}
                                QRadioButton::indicator:hover {{
                                    background-color: rgb{self.__settings.color_box_hover};
                                }}
                                QRadioButton::indicator:checked {{
                                    background-color: rgb{self.__settings.color_box_selected};
                                }}
                                '''
                            )

    def set_button_selector(self, button, i: int, total):
        if i == 0:  # left selector has a curved left corner
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self.__settings.color_text};
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    background-color: rgb{self.__settings.color_box_background};
                    border-top-left-radius: {self.__settings.box_border_radius}px;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -{self.__settings.button_text_hover_raise}px;
                    background-color: rgb{self.__settings.color_box_hover};
                }}
                QPushButton:checked {{
                    background-color: rgb{self.__settings.color_box_selected};
                }}
                '''
            )

        elif i == total - 1:  # middle selectors have no curved corners
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self.__settings.color_text};
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    background-color: rgb{self.__settings.color_box_background};
                    border-top-right-radius: {self.__settings.box_border_radius}px;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -{self.__settings.button_text_hover_raise}px;
                    background-color: rgb{self.__settings.color_box_hover};
                }}
                QPushButton:checked {{
                    background-color: rgb{self.__settings.color_box_selected};
                }}
                '''
            )

        else:  # right selector has a curved right corner
            button.setStyleSheet(
                f'''
                QPushButton {{
                    color: rgb{self.__settings.color_text};
                    border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                    background-color: rgb{self.__settings.color_box_background};
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    padding-top: -{self.__settings.button_text_hover_raise}px;
                    background-color: rgb{self.__settings.color_box_hover};
                }}
                QPushButton:pressed {{
                    background-color: rgb{self.__settings.color_box_selected};
                }}
                '''
            )

    def set_button_selectors(self, buttons) -> None:
        total = len(buttons)

        # updates the color for the selector buttons
        for i, button in enumerate(buttons):
            self.set_button_selector(button, i, total)

    # TestWindow ----------------------------------------------------------------------------------

    def init_test_buttons(self, buttons):
        for i, button in enumerate(buttons):  # sets the button parameters
            button.setFixedSize(self.__settings.test_button_width, self.__settings.test_button_height)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_test_box_buttons(self, widget) -> None:
        widget.setStyleSheet(
            f'''
            QWidget {{
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                background-color: rgb{self.__settings.color_box_background};
                border-radius: {self.__settings.box_border_radius}px;
                color: rgb{self.__settings.color_text};
                font-size: 15px;
            }}
            QPushButton {{
                border: {self.__settings.box_border}px solid rgb{self.__settings.color_box_border};
                border-radius: {self.__settings.box_border_radius}px;
            }}
            QPushButton:hover {{
                background-color: rgb{self.__settings.color_box_hover};
                padding-top: -{self.__settings.button_text_hover_raise}px;
            }}
            QPushButton:pressed {{
                background-color: rgb{self.__settings.color_box_selected};
            }}
            '''
        )
