from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class Preferences(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets()
        self._layout()
        self._properties()
        #self._connections()

    def _widgets(self):

        self.shiftCheckBox = QCheckBox('Shift')
        self.ctrlCheckBox = QCheckBox('Ctrl')
        self.winkeyCheckBox = QCheckBox('Winkey')
        self.altCheckBox = QCheckBox('Alt')
        self.keyLineEdit = QLineEdit()
        self.applyPushButton = QPushButton('&Apply')

    def _layout(self):

        horizontal = QHBoxLayout()
        horizontal.addWidget(self.shiftCheckBox)
        horizontal.addWidget(self.ctrlCheckBox)
        horizontal.addWidget(self.winkeyCheckBox)
        horizontal.addWidget(self.altCheckBox)
        horizontal.addWidget(self.keyLineEdit)

        groupbox = QGroupBox('Set Hotkey')
        groupbox.setLayout(horizontal)

        button = QHBoxLayout()
        button.addStretch()
        button.addWidget(self.applyPushButton)

        vertical = QVBoxLayout()
        vertical.addWidget(groupbox)
        vertical.addLayout(button)

        self.setLayout(vertical)

    def _properties(self):

        # self.keyLineEdit
        self.keyLineEdit.setMaxLength(1)
        self.keyLineEdit.setMaximumWidth(20)

        # Main window
        self.setWindowTitle('Preferences')
        self.resize(300, 104)

    def resizeEvent(self, event):

        print('width: {0}, height: {1}'.format(self.width(), self.height()))

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Shift:
            self.shiftCheckBox.setChecked(True) if not self.shiftCheckBox.isChecked() else self.shiftCheckBox.setChecked(False)

        if event.key() == Qt.Key_Control:
            self.ctrlCheckBox.setChecked(True) if not self.ctrlCheckBox.isChecked() else self.ctrlCheckBox.setChecked(False)

        if event.key() == Qt.Key_Meta:
            self.winkeyCheckBox.setChecked(True) if not self.winkeyCheckBox.isChecked() else self.winkeyCheckBox.setChecked(False)

        if event.key() == Qt.Key_Alt:
            self.altCheckBox.setChecked(True) if not self.altCheckBox.isChecked() else self.altCheckBox.setChecked(False)
