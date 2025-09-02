from PyQt6 import QtCore, QtGui, QtWidgets

from core.files import path
from core.style import Settings, Style
from core.system_settings import OperatingSystem


class ControlWindow(QtWidgets.QWidget):
    def __init__(self, settings: Settings, style: Style, op: OperatingSystem):
        QtWidgets.QWidget.__init__(self)

        # used to keep track of any settings the user changes within the window
        self._settings_user = settings
        self._style = style
        self._op = op

        self._op.set_fullscreen_function(self, self.__button_logic_maximize)

        # Window ------------------------------------------------------------------------------------------------

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint)  # removes default title bar
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # configures transparency

        # Title Bar ---------------------------------------------------------------------------------------------

        self.__window_moving = False  # initial state of the window moving
        self.__offset = None  # initial state of the window offset

        # window move widget
        self.__widget_move = QtWidgets.QWidget(self)

        # close button
        self.__button_close = QtWidgets.QPushButton('', self)
        self.__button_close.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.__button_close.setIcon(QtGui.QIcon(path("assets/icons/button_close_icon.png")))
        self.__button_close.clicked.connect(self.__button_logic_close)
        self.__button_close.pressed.connect(self.__button_close_press)
        self.__button_close.released.connect(self.__button_close_release)

        # maximize button
        self.__button_maximize = QtWidgets.QPushButton('', self)
        self.__button_maximize.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.__button_maximize.setIcon(QtGui.QIcon(path("assets/icons/button_maximize_icon.png")))
        self.__button_maximize.clicked.connect(self.__button_logic_maximize)

        # minimize button
        self.__button_minimize = QtWidgets.QPushButton('', self)
        self.__button_minimize.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.__button_minimize.setIcon(QtGui.QIcon(path("assets/icons/button_minimize_icon.png")))
        self.__button_minimize.clicked.connect(self.showMinimized)

        # Resizing Widgets --------------------------------------------------------------------------------------

        self.__window_resize = True  # initial state of resizing
        self.__window_resize_direction = None  # initial direction of resizing
        self.__widget_resize_toggle = True  # toggles resizing functionality

        self.__window_resize_allowed = True  # only allows resizing once the timer is over
        self.__window_resize_timer = QtCore.QTimer(self)  # timer for resizing
        self.__window_resize_timer.setSingleShot(True)  # timer triggers once before its cooldown
        self.__window_resize_timer.timeout.connect(self.__window_resize_enable)  # enables the timer after its cooldown
        self.__widget_resize = tuple(QtWidgets.QWidget(self) for _ in range(8))

        self.__widget_resize[0].setCursor(QtCore.Qt.CursorShape.SizeHorCursor)  # right
        self.__widget_resize[4].setCursor(QtCore.Qt.CursorShape.SizeHorCursor)  # left

        self.__widget_resize[1].setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)  # top right
        self.__widget_resize[5].setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)  # bottom left

        self.__widget_resize[2].setCursor(QtCore.Qt.CursorShape.SizeVerCursor)  # top
        self.__widget_resize[6].setCursor(QtCore.Qt.CursorShape.SizeVerCursor)  # bottom

        self.__widget_resize[3].setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)  # top left
        self.__widget_resize[7].setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)  # bottom right

        # -------------------------------------------------------------------------------------------------------

    def _set_title(self, title: str):
        """
        Sets the title of the window.
        """

        self.setWindowTitle(title)

        # displays title
        self.__title_label = QtWidgets.QLabel(title, self)
        self.__title_label.move(self._settings_user.window_title_position[0], self._settings_user.window_title_position[1])

    def _set_geometry(self, x_position: int, y_position: int, width: int, height: int):
        """
        Sets the initial size of the window.

        :param x_position: The x position of the top left corner.
        :param y_position: The y position of the top left corner.
        :param width: The width of the window.
        :param height: The height of the window.
        """
        self.setGeometry(x_position, y_position, width, height)  # initial window size / position

    def _set_size_min(self, min_width: int, min_height: int):
        self.setMinimumSize(min_width, min_height)  # sets the minimum size of the window (used for macOS since the OS automatically controls the resizing)

        self.size_min = min_width, min_height

    def _window_normal(self) -> None:
        """
        Returns the window to its normal state, and enables all resizing widgets. Takes the window out of all modes.
        """

        self.showNormal()

        for widget in self.__widget_resize:  # enables all resizing widgets
            widget.setEnabled(True)

        self.__widget_resize_toggle = True  # allows the window to be resized

    def _update_control(self) -> None:
        """
        Updates the positions of all widgets in the control class.
        """

        # move widget
        self.__widget_move.move(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_move.resize(self.width() - self._settings_user.widget_resize_size - (3 * self._settings_user.title_bar_height), self._settings_user.title_bar_height - self._settings_user.widget_resize_size)

        # close button
        self.__button_close.move(self.width() - self._settings_user.title_bar_button_width, 0)
        self.__button_close.resize(self._settings_user.title_bar_button_width, self._settings_user.title_bar_height)

        # maximize button
        self.__button_maximize.move(self.width() - (2 * self._settings_user.title_bar_button_width), 0)
        self.__button_maximize.resize(self._settings_user.title_bar_button_width, self._settings_user.title_bar_height)

        # minimize button
        self.__button_minimize.move(self.width() - (3 * self._settings_user.title_bar_button_width), 0)
        self.__button_minimize.resize(self._settings_user.title_bar_button_width, self._settings_user.title_bar_height)

        # Resize Widgets, Order: right, top right, top, top left, left, bottom left, bottom, bottom right
        self.__widget_resize[0].move(self.width() - self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[0].resize(self._settings_user.widget_resize_size, self.height() - (2 * self._settings_user.widget_resize_size))
        self.__widget_resize[1].move(self.width() - self._settings_user.widget_resize_size, 0)
        self.__widget_resize[1].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[2].move(self._settings_user.widget_resize_size, 0)
        self.__widget_resize[2].resize(self.width() - (2 * self._settings_user.widget_resize_size), self._settings_user.widget_resize_size)
        self.__widget_resize[3].move(0, 0)
        self.__widget_resize[3].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[4].move(0, self._settings_user.widget_resize_size)
        self.__widget_resize[4].resize(self._settings_user.widget_resize_size, self.height() - (2 * self._settings_user.widget_resize_size))
        self.__widget_resize[5].move(0, self.height() - self._settings_user.widget_resize_size)
        self.__widget_resize[5].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)
        self.__widget_resize[6].move(self._settings_user.widget_resize_size, self.height() - self._settings_user.widget_resize_size)
        self.__widget_resize[6].resize(self.width() - (2 * self._settings_user.widget_resize_size), self._settings_user.widget_resize_size)
        self.__widget_resize[7].move(self.width() - self._settings_user.widget_resize_size, self.height() - self._settings_user.widget_resize_size)
        self.__widget_resize[7].resize(self._settings_user.widget_resize_size, self._settings_user.widget_resize_size)

    def _update_colors_control(self) -> None:
        """
        Updates the colors for the ControlWindow.

        Updates the title bar button colors, and the title label color.
        """

        self._style.set_button_close(self.__button_close)
        self._style.set_button_maximize(self.__button_maximize)
        self._style.set_button_minimize(self.__button_minimize)
        self._style.set_title_label(self.__title_label)

    def __button_close_press(self) -> None:
        self.__button_close.setIcon(QtGui.QIcon(path("assets/icons/button_close_press_icon.png")))

    def __button_close_release(self) -> None:
        self.__button_close.setIcon(QtGui.QIcon(path("assets/icons/button_close_icon.png")))

    def __window_resize_enable(self) -> None:
        """
        Re-enables resizing after the timer expires.
        """

        self.__window_resize_allowed = True

    def __button_logic_close(self) -> None:
        """
        Closes the window.
        """

        self.close()

    def __button_logic_maximize(self) -> None:
        """
        Maximizes the screen using the maximize button.
        """

        if self._op.get_system_name() == "Darwin":  # on macOS, the maximize button full screens the window
            self.__logic_full_screen()
            return

        self.__logic_maximize()

    def __logic_maximize(self):
        """
        Maximizes the window.
        """

        if self.isMaximized():
            # return to state before maximized
            self.showNormal()
            self.__widget_resize_toggle = True

            for widget in self.__widget_resize:  # enables all resizing widgets
                widget.setEnabled(True)

        else:
            # maximize window
            self.showMaximized()
            self.__widget_resize_toggle = False

            for widget in self.__widget_resize:  # disables all resizing widgets
                widget.setEnabled(False)

        self.resizeEvent(None)  # resizes the window

    def __logic_full_screen(self) -> None:
        """
        Full screens the window.
        """

        if self.isFullScreen():
            # return to state before full screened
            self.showNormal()
            self.__widget_resize_toggle = True

            self._style.update_border_radius(False, self.__button_close)  # adds a border radius to the window

            self.activateWindow()  # focuses the window

            for widget in self.__widget_resize:  # enables all resizing widgets
                widget.setEnabled(True)

        else:
            # maximize window
            self.showFullScreen()
            self.__widget_resize_toggle = False

            self._style.update_border_radius(True, self.__button_close)  # removes the border radius

            for widget in self.__widget_resize:  # disables all resizing widgets
                widget.setEnabled(False)

        self.resizeEvent(None)  # resizes the window

    def paintEvent(self, event) -> None:
        """
        Gives the background and title bar their colors.
        """

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # stops the painter from painting the corners
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(0, 0, self.width(), self.height()), self._settings_user.window_border_radius, self._settings_user.window_border_radius)
        painter.setClipPath(path)

        # title bar
        painter.fillRect(0, 0, self.width(), self._settings_user.title_bar_height, QtGui.QColor(*self._settings_user.color_title_bar))

        # center window
        color_background_transparent_amount = max(1, self._settings_user.color_background_transparent_amount)  # if set to 0, the background isn't there, and lets the user click things behind the window (this is prevented by making the minimum value 1)
        painter.fillRect(0, self._settings_user.title_bar_height, self.width(), self.height() - self._settings_user.title_bar_height, QtGui.QColor(*self._settings_user.color_background, color_background_transparent_amount))

    def showEvent(self, event):
        super().showEvent(event)

        if self._settings_user.color_background_blurred:
            self._op.enable_blur(self)

    def keyPressEvent(self, event) -> None:

        # maximizes the window based on the operating system's shortcut
        if self._op.is_maximize_shortcut(event):
            self.__logic_full_screen()

            # focuses the window
            self.activateWindow()
            self.raise_()
            self.setFocus()

        else:
            super().keyPressEvent(event)  # passes other key presses

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        """
        Runs this function if the user double-clicks anywhere in the window.

        Used to maximize the window if the user double-clicks on the title bar.
        """

        if self.isFullScreen():  # double-clicking does nothing when full screened
            return

        if self.__widget_move.geometry().contains(event.pos()):  # checks if the user is in the title bar
            self.__logic_maximize()
        else:
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """
        Sets moving variables to false if the user stops hold left click.

        :param event: Detects when a mouse button is released.
        """

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__window_moving = False
            self.__window_resize = False

    def mousePressEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """
        Detects if the user pressed left click to resize or move the window.

        :param event: Detects when a mouse button is pressed.
        """

        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.__offset = event.position().toPoint()

            # moving Window
            self.__window_moving = False
            if self.__widget_move.rect().contains(self.__widget_move.mapFrom(self, self.__offset)):
                self.__window_moving = True
                self.__offset = event.globalPosition().toPoint() - self.pos()
                return

            # resizing Widgets
            self.__window_resize = False
            if self.__widget_resize_toggle:

                for i in range(len(self.__widget_resize)):  # checks if cursor is in any of the resizing widgets
                    if self.__widget_resize[i].rect().contains(self.__widget_resize[i].mapFrom(self, self.__offset)):
                        self.__window_resize_direction = i
                        self.__window_resize = True
                        break

    def mouseMoveEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """
        Detects when the user moves their mouse.

        Use to detect if the user trying to move or resize the window.

        :param event: Detects when the mouse is left-clicked and moves.
        """

        # Moving Window
        if self.__window_moving:

            # exits the maximized setting
            if self.isMaximized():

                offset_x = min(int(self.normalGeometry().width() * (self.__offset.x() / self.width())), self.normalGeometry().width() - (3 * self._settings_user.title_bar_button_width))
                self.__offset = QtCore.QPoint(offset_x, self.__offset.y())

                self.__button_logic_maximize()

                mouse_position = event.globalPosition().toPoint() - self.__offset

            elif self.isFullScreen():  # stops the window from moving if it is full screened
                return

            else:
                mouse_position = event.globalPosition().toPoint() - self.__offset

            self.move(mouse_position)

        # Resizing Widgets
        elif self.__window_resize:

            # right
            if self.__window_resize_direction == 0:
                new_width = event.position().toPoint().x()
                if new_width >= self.size_min[0]:
                    self.resize(new_width, self.height())

            # bottom
            elif self.__window_resize_direction == 6:
                new_height = event.position().toPoint().y()
                if new_height >= self.size_min[1]:
                    self.resize(self.width(), new_height)

            # top right
            elif self.__window_resize_direction == 1 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                new_width = event.position().toPoint().x()
                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_width >= self.size_min[0] and new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, new_width, new_height)

                elif new_width >= self.size_min[0]:
                    # resizes the window to the new size
                    self.resize(new_width, self.height())

                elif new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # bottom left
            elif self.__window_resize_direction == 5 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x
                new_height = event.position().toPoint().y()

                if new_width >= self.size_min[0] and new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, new_height)

                elif new_width >= self.size_min[0]:
                    # resizes the window to the new size
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

                elif new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.resize(self.width(), new_height)

            # top
            elif self.__window_resize_direction == 2 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # left
            if self.__window_resize_direction == 4 and self.__window_resize_allowed:  # Check if resizing is allowed

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x

                if new_width >= self.size_min[0]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

            # top left
            elif self.__window_resize_direction == 3 and self.__window_resize_allowed:

                self.__window_resize_allowed = False  # prevents further resizing until the timer expires
                self.__window_resize_timer.start(1)  # starts the timer

                temp_event_x = event.position().toPoint().x()  # gets the mouse x position
                new_width = self.width() - temp_event_x
                temp_event_y = event.position().toPoint().y()  # gets the mouse y position
                new_height = self.height() - temp_event_y

                if new_width >= self.size_min[0] and new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y() + temp_event_y, new_width, new_height)

                elif new_width >= self.size_min[0]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x() + temp_event_x, self.y(), new_width, self.height())

                elif new_height >= self.size_min[1]:
                    # moves window to new position and changes its shape
                    self.setGeometry(self.x(), self.y() + temp_event_y, self.width(), new_height)

            # bottom right
            elif self.__window_resize_direction == 7:

                new_width = max(self.size_min[0], event.position().toPoint().x())
                new_height = max(self.size_min[1], event.position().toPoint().y())
                self.resize(new_width, new_height)
