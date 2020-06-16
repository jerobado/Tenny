from PyQt5.QtWidgets import QKeySequenceEdit
from PyQt5.QtGui import QKeySequence


class KeySequenceEdit(QKeySequenceEdit):

    def __init__(self, parent=None):

        super().__init__(parent)

    def keyPressEvent(self, event):

        super().keyPressEvent(event)
        value = self.keySequence()
        self.setKeySequence(QKeySequence(value))
