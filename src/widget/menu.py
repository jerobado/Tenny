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

        # [] TODO: create preferences dialog
        logging.debug('display preference dialog')
