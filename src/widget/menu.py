import logging
from PyQt5.QtWidgets import (QMenu, QAction)

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')


class ContextMenu(QMenu):

    def __init__(self):

        super().__init__()
        self.preferencesAction = QAction()
        self.preferencesAction.setText('Preferences')
        self.preferencesAction.triggered.connect(self._on_preferencesAction_triggered)

        self.addAction(self.preferencesAction)

    def _on_preferencesAction_triggered(self):

        from src.dialog.preferences import PreferencesDialog

        dialog = PreferencesDialog()
        if dialog.exec():
            logging.debug('settings to be udpated:')
            logging.debug(f'Start/Stop: {dialog.startstopHotkeyLineEdit.keySequence().toString()}')
            logging.debug(f'Reset: {dialog.resetHotkeyLineEdit.keySequence().toString()}')
