import logging
from PyQt5.QtWidgets import (QMenu, QAction)

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')


class ContextMenu(QMenu):

    def __init__(self):

        super().__init__()
        self.preferencesAction = QAction()
        # [] TODO: create a dedicated Action class to do the lines below
        # self.preferencesAction = PreferencesAction()
        # self.quitAction = QuitAction()

        self.addAction(self.preferencesAction)
        # self.addAction(self.quitAction)
