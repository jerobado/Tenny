# Preference Dialog(s)
import logging
from PyQt5.QtWidgets import (QDialog,
                             QPushButton,
                             QGroupBox,
                             QHBoxLayout,
                             QVBoxLayout,
                             QGridLayout,
                             QLabel,
                             QMessageBox)
from src.widget.keysequenceedit import KeySequenceEdit

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.preferences = dict()
        self.common_hotkey = set()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.descriptionLabel = QLabel()
        self.startstopLabel = QLabel('Start/Stop:')
        self.resetLabel = QLabel('Reset:')
        self.unhideLabel = QLabel('Unhide:')
        self.startstopKeySequenceEdit = KeySequenceEdit()
        self.resetKeySequenceEdit = KeySequenceEdit()
        self.unhideKeySequenceEdit = KeySequenceEdit()
        self.okPushButton = QPushButton('OK')

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.startstopLabel, 0, 0)
        grid.addWidget(self.startstopKeySequenceEdit, 0, 1)
        grid.addWidget(self.resetLabel, 1, 0)
        grid.addWidget(self.resetKeySequenceEdit, 1, 1)
        grid.addWidget(self.unhideLabel, 2, 0)
        grid.addWidget(self.unhideKeySequenceEdit, 2, 1)

        hotkeyGroupBox = QGroupBox('Hotkey')
        hotkeyGroupBox.setLayout(grid)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(self.okPushButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.descriptionLabel)
        vbox.addWidget(hotkeyGroupBox)
        vbox.addLayout(buttons)

        self.setLayout(vbox)

    def _properties(self):

        self.descriptionLabel.setText('Set your preferred settings here:')
        self.resize(381, 149)

    def _connections(self):

        self.okPushButton.clicked.connect(self._on_okPushButton_clicked)

    def get_user_input(self):

        self.preferences['new-startstop'] = self.startstopKeySequenceEdit.keySequence().toString()
        self.preferences['new-reset'] = self.resetKeySequenceEdit.keySequence().toString()
        self.preferences['new-unhide'] = self.unhideKeySequenceEdit.keySequence().toString()

    def isHotkeyExist(self):

        new_hotkeys = [
            self.preferences['new-startstop'],
            self.preferences['new-reset'],
            self.preferences['new-unhide']
        ]
        self.common_hotkey = set(self.existing_hotkeys).intersection(new_hotkeys)

        return len(self.common_hotkey) > 0

    # Slots
    def _on_okPushButton_clicked(self):

        self.get_user_input()
        if not self.isHotkeyExist():
            # Update hotkeys one-by-one
            if self.preferences['new-startstop']:
                self.startstopHotkey.updateShortcut(self.preferences['new-startstop'], self.startstopPushButton_click)
                logging.debug(f'Start/Stop: new hotkey -> {self.preferences["new-startstop"]}')

            if self.preferences['new-reset']:
                self.resetHotkey.updateShortcut(self.preferences['new-reset'], self.resetPushButton_click)
                logging.debug(f'Reset: new hotkey -> {self.preferences["new-reset"]}')

            if self.preferences['new-unhide']:
                self.unhideHotkey.updateShortcut(self.preferences['new-unhide'], self.unhide_slot)
                logging.debug(f'Unhide: new hotkey -> {self.preferences["new-unhide"]}')

            self.hide()

        else:
            QMessageBox.warning(self, 'Set Hotkey', 'Entered hotkey already exist', QMessageBox.Ok)
            logging.debug(f'{self.common_hotkey} already exist')

    def closeEvent(self, event):

        self.hide()
        event.ignore()
