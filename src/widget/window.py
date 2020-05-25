# Recreating our main window

from PyQt5.QtWidgets import QWidget


class MainWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        ...

    def _layout(self):

        ...

    def _properties(self):

        self.setWindowTitle('Tenny MainWindow')

    def _connections(self):

        ...
