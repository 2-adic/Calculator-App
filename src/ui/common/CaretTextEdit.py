from PyQt6 import QtCore, QtGui, QtWidgets


# custom caret code adapted from musicamante at https://stackoverflow.com/questions/68769475/how-to-set-the-color-of-caret-blinking-cursor-in-qlineedit
# modified by removing default caret from the left of the new caret
class CaretTextEditStyle(QtWidgets.QProxyStyle):
    def pixelMetric(self, pm, opt=None, widget=None) -> int:
        if (
            pm == QtWidgets.QStyle.PixelMetric.PM_TextCursorWidth and opt
            and isinstance(opt.styleObject, CaretTextEdit)
            # hide native cursor only when a custom caret is active
            and (opt.styleObject.property("caretSize") or 0) > 0
        ):
            return 0
        return super().pixelMetric(pm, opt, widget)


class CaretTextEdit(QtWidgets.QPlainTextEdit):
    # default values
    __caretSize: int = 2  # visible by default
    __caretColor = QtGui.QColor(255, 255, 255)  # color of the custom caret

    def __init__(self, text: str | None = None, defaultText: str | None = None, tag: str | None = None, *args, **kwargs) -> None:
        self.__tag = tag

        # accept legacy kwargs used elsewhere (e.g. setText="...") and normalized names
        if "setText" in kwargs:
            text = kwargs.pop("setText")
        if "defaultText" in kwargs:
            defaultText = kwargs.pop("defaultText")

        # prepare state before super() as setters might be called early
        self.__caretVisible = False
        super().__init__(*args, **kwargs)

        self.setStyle(CaretTextEditStyle())
        
        self.__nativeCursorVisibility()  # show/hide native cursor based on caret size

        self.__blinkTimer = QtCore.QTimer(
            self,
            timeout=self.__toggleCaretVisibility,
            interval=QtWidgets.QApplication.styleHints().cursorFlashTime() // 2
        )

        # apply initial plain text / placeholder if provided
        if text is not None:
            self.setPlainText(text)
        if defaultText is not None:
            # QPlainTextEdit supports a placeholder text property
            try:
                self.setPlaceholderText(defaultText)
            except Exception:
                # fallback: do nothing if environment doesn't support placeholder
                pass

    def __nativeCursorVisibility(self) -> None:
        """
        Show/Hide native cursor based on caret size.
        """

        if self.__caretSize > 0:
            self.setCursorWidth(0)  # hide native cursor
        else:
            self.setCursorWidth(1)  # show native cursor

    @QtCore.pyqtProperty(int)
    def caretSize(self) -> int:
        return self.__caretSize

    @caretSize.setter
    def caretSize(self, size: int) -> None:
        if size < 0:
            size = -1
        if self.__caretSize != size:
            self.__caretSize = size
            self.__nativeCursorVisibility()  # hide/show native cursor based on caret size
            self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def caretColor(self) -> QtGui.QColor:
        return self.__caretColor

    @caretColor.setter
    def caretColor(self, color: QtGui.QColor) -> None:
        if self.__caretColor == color:
            return
        self.__caretColor = color
        # repaint immediately if caret is visible
        if getattr(self, "_CaretTextEdit__caretVisible", False) and self.hasFocus():
            self.update(self.cursorRect())
        else:
            self.update()

    def __toggleCaretVisibility(self) -> None:
        self.__caretVisible = not self.__caretVisible
        self.update(self.cursorRect())

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)
        self.__caretVisible = True
        self.__blinkTimer.start()
        self.update(self.cursorRect())

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.__blinkTimer.stop()
        self.__caretVisible = False
        self.update()

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        self.__caretVisible = True
        self.__blinkTimer.start()
        self.update(self.cursorRect())

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if self.__caretSize > 0 and self.hasFocus() and self.__caretVisible:
            qp = QtGui.QPainter(self.viewport())
            cr = self.cursorRect()
            x = cr.x() + round(cr.width() / 2) - round(self.__caretSize / 2)
            rect = QtCore.QRect(x, cr.y(), max(1, self.__caretSize), self.fontMetrics().height())
            qp.fillRect(rect, self.__caretColor)

    def tag(self) -> str | None:
        return self.__tag
    
    def setTag(self, tag: str | None) -> None:
        self.__tag = tag
