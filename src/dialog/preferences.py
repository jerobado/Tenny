# Preference Dialog(s)
import logging
from PyQt5.QtWidgets import (QDialog,
                             QCheckBox,
                             QPushButton,
                             QGroupBox,
                             QHBoxLayout,
                             QVBoxLayout,
                             QGridLayout,
                             QGridLayout,
                             QLineEdit,
                             QLabel,
                             QSlider,
                             QKeySequenceEdit,
                             QMessageBox)
from PyQt5.QtCore import Qt
import keyboard
from src.widget.keysequenceedit import KeySequenceEdit

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')


# [] TODO: design your 'Settings' dialog
class SetShortcut(QDialog):
    """ A dialog that will let the user choose his/her preferred hotkey. """

    def __init__(self, parent=None):

        super().__init__(parent)
        self.modifier_keys = []
        self.single_key = ''
        self.selected_hotkeys = ''      # Combination of self.modifier_keys and self.single_key
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self) -> None:
        """ List of QWidgets used in this dialog. """

        self.shiftCheckBox = QCheckBox('Shift')
        self.ctrlCheckBox = QCheckBox('Ctrl')
        self.winCheckBox = QCheckBox('Win')
        self.altCheckBox = QCheckBox('Alt')
        self.keyLineEdit = QLineEdit()
        self.messageLabel = QLabel()
        self.okPushButton = QPushButton('&OK')

    def _layout(self) -> None:
        """ Layout design in this dialog. """

        horizontal = QHBoxLayout()
        horizontal.addWidget(self.shiftCheckBox)
        horizontal.addWidget(self.ctrlCheckBox)
        horizontal.addWidget(self.winCheckBox)
        horizontal.addWidget(self.altCheckBox)
        horizontal.addWidget(self.keyLineEdit)

        groupbox = QGroupBox('Keys')
        groupbox.setLayout(horizontal)

        button = QHBoxLayout()
        button.addWidget(self.messageLabel)
        button.addStretch()
        button.addWidget(self.okPushButton)

        vertical = QVBoxLayout()
        vertical.addWidget(groupbox)
        vertical.addLayout(button)

        self.setLayout(vertical)

    def _properties(self) -> None:
        """ Settings of all QObjects stored are all here. """

        self.keyLineEdit.setPlaceholderText('type any key')
        self.keyLineEdit.setReadOnly(True)

        # SetShortcut(QDialog)
        self.resize(300, 104)
        self.setModal(True)

    def _connections(self) -> None:
        """ Connect all signals and slots here. """

        self.shiftCheckBox.clicked.connect(self.on_anyCheckBox_clicked)
        self.altCheckBox.clicked.connect(self.on_anyCheckBox_clicked)
        self.ctrlCheckBox.clicked.connect(self.on_anyCheckBox_clicked)
        self.winCheckBox.clicked.connect(self.on_anyCheckBox_clicked)
        self.okPushButton.clicked.connect(self.accept)

    def on_anyCheckBox_clicked(self) -> None:
        """ Call self.update_modifier_keys() everytime the user clicked any of the four (4) checkboxes. """

        self.update_modifier_keys()

    def update_modifier_keys(self) -> None:
        """ Update self.modifier_keys based on the checkbox clicked. """

        checkbox = self.sender()
        text = checkbox.text().lower()
        if checkbox.isChecked():
            self.modifier_keys.append(text)
        else:
            self.modifier_keys.remove(text)

    def update_single_key(self):
        """ Update self.single_key based on self.keyLineEdit's text. """

        self.single_key = self.keyLineEdit.text()

    def accept(self):
        """ Call self.update_user_hotkeys() based on the user's selected keys. """

        self.update_user_hotkeys()
        self.done(1)

    def update_user_hotkeys(self) -> None:
        """ Update self.selected_hotkeys based on the combined self.modifier_keys and self.single_key. """

        self.selected_hotkeys = '+'.join(self.get_combined_modifier_and_single_keys())

    def get_combined_modifier_and_single_keys(self) -> list:
        """ Return combined self.modifier_keys and self.single_key. """

        return self.modifier_keys + [self.single_key]

    def keyPressEvent(self, event):
        """ Update self.single_key based on the key pressed in the self.keyLineEdit. """

        self.keyLineEdit.setText(keyboard.read_key())
        self.update_single_key()


class SetOpacity(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._layout()
        self._properties()

    def _widgets(self):

        self.opacityLabel = QLabel()
        self.opacitySlider = QSlider()

    def _layout(self):

        horizontal = QVBoxLayout()
        horizontal.addWidget(self.opacityLabel)
        horizontal.addWidget(self.opacitySlider)

        self.setLayout(horizontal)

    def _properties(self):

        self.opacitySlider.setRange(0, 100)
        self.opacitySlider.setSingleStep(1)
        self.opacitySlider.setPageStep(25)
        self.opacitySlider.setTracking(True)

        self.opacityLabel.setAlignment(Qt.AlignHCenter)

        self.setWindowFlags(Qt.ToolTip)


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
        self.startstopKeySequenceEdit.keySequenceChanged.connect(self._on_KeySequenceChanged)
        self.resetKeySequenceEdit.keySequenceChanged.connect(self._on_KeySequenceChanged)
        self.unhideKeySequenceEdit.keySequenceChanged.connect(self._on_KeySequenceChanged)

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
            # [] TODO: prevent accepting multiple key sequence
            if self.preferences['new-startstop']:
                self.startstopHotkey.updateShortcut(self.preferences['new-startstop'], self.startstopPushButton_click)
                logging.debug(f'Start/Stop: new hotkey -> {self.preferences["new-startstop"]}')

            if self.preferences['new-reset']:
                self.resetHotkey.updateShortcut(self.preferences['new-reset'], self.resetPushButton_click)
                logging.debug(f'Reset: new hotkey -> {self.preferences["new-reset"]}')

            if self.preferences['new-unhide']:
                self.unhideHotkey.updateShortcut(self.preferences['new-unhide'], self.unhide_slot)

            self.hide()

        else:
            QMessageBox.warning(self, 'Set Hotkey', 'Entered hotkey already exist', QMessageBox.Ok)
            logging.debug(f'{self.common_hotkey} already exist')

    def _on_KeySequenceChanged(self):

        if len(self.startstopKeySequenceEdit.keySequence()) > 1:
            self.startstopKeySequenceEdit.clear()

        if len(self.resetKeySequenceEdit.keySequence()) > 1:
            self.resetKeySequenceEdit.clear()

        if len(self.unhideKeySequenceEdit.keySequence()) > 1:
            self.unhideKeySequenceEdit.clear()

    def closeEvent(self, event):

        self.hide()
        event.ignore()

