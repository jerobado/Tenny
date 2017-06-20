import keyboard
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QGridLayout, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QIcon
from resources import tenny_resources


__title__ = 'Tenny'
__author__ = 'mokachokokarbon'
__version__ = 0.3


class Ten(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._START = '&START'
        self._STOP = '&STOP'
        self._RESET = '&RESET'
        self._FORMAT = 'hh:mm:ss.zzz'

        self.stort_hotkey = 'ctrl+9'
        self.reset_hotkey = 'ctrl+0'

        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._create_actions()
        self._create_menus()
        self._hotkeys(self.stort_hotkey)
        #self._systemTray()

    def _widgets(self):

        self.shiverTimer = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timerLCDNumber = QLCDNumber()
        self.timerLCDNumber.setDigitCount(12)
        self.timerLCDNumber.display("00:00:00.000")
        self.stortPushButton = QPushButton(self._START)
        self.resetPushButton = QPushButton(self._RESET)
        self.stortPushButton.setToolTip("Start/Stop ({0})".format(self.stort_hotkey))
        self.resetPushButton.setToolTip("Reset ({0})".format(self.stort_hotkey))
        #self.tennySystemTray = QSystemTrayIcon()

        # TODO: playing with QSystemTrayIcon here
        #self.tennySystemTray.setIcon(QIcon(':/stopwatch-32.png'))
        #self.tennySystemTray.setToolTip('Tenny 0.2')
        #self.tennySystemTray.show()

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.timerLCDNumber, 0, 0, 1, 2)
        grid.addWidget(self.stortPushButton, 1, 0)
        grid.addWidget(self.resetPushButton, 1, 1)

        self.setLayout(grid)

    def _properties(self):

        # Main window
        self.setWindowIcon(QIcon(':/stopwatch-32.png'))
        self.resize(350, 125)
        self.setWindowTitle('{} {}'.format(__title__, __version__))
        self.setWindowOpacity(0.7)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # self.stortPushButton
        self.stortPushButton.setContextMenuPolicy(Qt.CustomContextMenu)
        self.stortPushButton.customContextMenuRequested.connect(self.on_context_menu)

        # self.stortPushButton
        self.resetPushButton.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resetPushButton.customContextMenuRequested.connect(self.on_context_menu)

    def _connections(self):

        self.timer.timeout.connect(self.showStopwatch)
        self.stortPushButton.clicked.connect(self.on_stortPushButton_clicked)
        self.resetPushButton.clicked.connect(self.on_resetPushButton_clicked)

    def _create_menus(self):

        # Context menu for self.stortPushButton
        self.stortPushButton_contextMenu = QMenu()
        self.stortPushButton_contextMenu.addAction(self.setShortcutAction)

    def _create_actions(self):

        self.setShortcutAction = QAction("Set shortcut", self,
                                         triggered=self.on_setShortcut_action)

    def _hotkeys(self, stort):

        keyboard.add_hotkey(stort, self.stortPushButton.click)
        keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)

    def _systemTray(self):

        self.tennySystemTray.showMessage('Tenny', 'Tenny is now active.', QSystemTrayIcon.Information, 3000)

    def showStopwatch(self):
        """
            Event handler for showing elapsed time, just like a stopwatch
        """

        self.shiverTimer = self.shiverTimer.addMSecs(1)
        text = self.shiverTimer.toString(self._FORMAT)
        self.timerLCDNumber.display(text)

    def on_stortPushButton_clicked(self):

        if self.stortPushButton.text() == self._START:
            self.timer.start(1)
            self.stortPushButton.setText(self._STOP)
            # title, message, icon, time
            #self.tennySystemTray.showMessage('Tenny timer started', 'Press Ctrl + 1 to stop the timer.', QSystemTrayIcon.Information, 5000)
        else:
            self.timer.stop()
            self.stortPushButton.setText(self._START)
            #self.tennySystemTray.showMessage('Tenny timer stopped', 'Press Ctrl + 1 to start the timer.', QSystemTrayIcon.Information, 5000)

    def on_resetPushButton_clicked(self):

        self.timer.stop()
        self.shiverTimer = QTime(0, 0, 0)
        self.timerLCDNumber.display(self.shiverTimer.toString(self._FORMAT))

        if self.stortPushButton.text() == self._STOP:
            self.stortPushButton.setText(self._START)

    def on_setShortcut_action(self):

        from src.dialog.preferences import SetShortcut
        dialog = SetShortcut(self)
        if dialog.exec():
            print('user preferred shortcut:', dialog.selected_hotkeys)
            keyboard.add_hotkey(dialog.selected_hotkeys, self.stortPushButton.click)

    def on_context_menu(self, point):

        self.stortPushButton_contextMenu.exec(self.stortPushButton.mapToGlobal(point))
