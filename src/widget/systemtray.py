from PyQt5.QtWidgets import (QSystemTrayIcon)
from PyQt5.QtGui import QIcon
from src.widget.menu import ContextMenu


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self):

        super().__init__()
        self.contextmenu = ContextMenu()

        self.setIcon(QIcon(':/stopwatch-32.png'))
        self.setToolTip('Tenny develop 0.6')
        self.setContextMenu(self.contextmenu)
