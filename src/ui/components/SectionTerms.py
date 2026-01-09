from PyQt6 import QtCore, QtWidgets

from ui.common.SortFormLayout import SortFormLayout


class SectionTermsScrollArea(QtWidgets.QScrollArea):
    """
    Custom scroll area that reports its content size as the preferred size hint.
    """
    MIN_COLLAPSED_HEIGHT = 98
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._contentHeight = self.MIN_COLLAPSED_HEIGHT
        self.setMinimumHeight(self.MIN_COLLAPSED_HEIGHT)
    
    def setContentHeight(self, height: int):
        self._contentHeight = max(self.MIN_COLLAPSED_HEIGHT, height)
        self.updateGeometry()
    
    def sizeHint(self):
        hint = super().sizeHint()
        hint.setHeight(self._contentHeight)
        return hint


class SectionTerms(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None, labelText: str | None = None) -> None:
        super().__init__(parent)

        self.__labelText: str | None = labelText
        self.__scrollUpdateScheduled = False

        self.__initUi()

    def __initUi(self) -> None:
        """
        Initializes the UI components.
        """

        self.setLayout(QtWidgets.QVBoxLayout())

        # init label and line
        self.__label = None
        self.__line = None
        if self.__labelText is not None:
            # add title
            self.__label: QtWidgets.QLabel = QtWidgets.QLabel(self.__labelText)
            self.layout().addWidget(self.__label)

            # add line under title
            self.__line: QtWidgets.QFrame = QtWidgets.QFrame()
            self.__line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            self.__line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
            self.layout().addWidget(self.__line)

        # add scroll area
        self.__scrollArea: SectionTermsScrollArea = SectionTermsScrollArea()
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.__scrollArea.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
        self.__scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout().addWidget(self.__scrollArea)

        # init form layout for sorted term rows
        self._formWidget = QtWidgets.QWidget()
        self._formWidget.setLayout(SortFormLayout())
        self._formWidget.layout().setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self._formWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum))
        self.__scrollArea.setWidget(self._formWidget)

        self._formWidget.installEventFilter(self)
        self._requestScrollAreaUpdate()

    def label(self) -> QtWidgets.QLabel | None:
        """
        Returns the label widget.
        """

        return self.__label
    
    def line(self) -> QtWidgets.QFrame | None:
        """
        Returns the line widget.
        """

        return self.__line

    def scrollArea(self) -> QtWidgets.QScrollArea:
        """
        Returns the scroll area widget.
        """

        return self.__scrollArea

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if obj is self._formWidget and event.type() in (
            QtCore.QEvent.Type.LayoutRequest,
            QtCore.QEvent.Type.Resize,
            QtCore.QEvent.Type.Show,
        ):
            self._requestScrollAreaUpdate()

        return super().eventFilter(obj, event)

    def _requestScrollAreaUpdate(self) -> None:
        """
        Schedules a deferred update so the scroll area height matches its contents.
        """

        if self.__scrollUpdateScheduled:
            return

        self.__scrollUpdateScheduled = True
        QtCore.QTimer.singleShot(0, self.__applyScrollAreaUpdate)

    def __applyScrollAreaUpdate(self) -> None:
        """
        Updates the scroll area height to match its contents.
        """

        self.__scrollUpdateScheduled = False

        layout = self._formWidget.layout()
        if layout is None:
            return

        contentHeight = max(0, layout.sizeHint().height())
        margins = self.__scrollArea.contentsMargins()
        padding = margins.top() + margins.bottom() + (self.__scrollArea.frameWidth() * 2)
        
        # calculate the ideal height for the content
        idealHeight = contentHeight + padding
        minHeight = SectionTermsScrollArea.MIN_COLLAPSED_HEIGHT
        targetHeight = max(minHeight, idealHeight)
        
        # update the scroll area's size hint to prefer the content height
        self.__scrollArea.setContentHeight(targetHeight)

        # let the layout shrink below the hint if needed, but never grow past content height
        if self.__scrollArea.minimumHeight() != minHeight:
            self.__scrollArea.setMinimumHeight(minHeight)

        if self.__scrollArea.maximumHeight() != targetHeight:
            self.__scrollArea.setMaximumHeight(targetHeight)
