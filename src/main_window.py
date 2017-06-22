import keyboard
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QGridLayout, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTime, QTimer, Qt, QSettings
from PyQt5.QtGui import QIcon
from resources import tenny_resources


__title__ = 'Tenny'
__author__ = 'mokachokokarbon'
__version__ = 0.3
DEFAULT_STORT_SHORTCUT = 'shift+f1'
DEFAULT_RESET_SHORTCUT = 'shift+f2'


class Ten(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._START = '&START'
        self._STOP = '&STOP'
        self._RESET = '&RESET'
        self._FORMAT = 'hh:mm:ss.zzz'
        self.stort_hotkey = DEFAULT_STORT_SHORTCUT
        self.reset_hotkey = DEFAULT_RESET_SHORTCUT
        self._read_settings()
        self._create_actions()
        self._create_menus()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._hotkeys()

    def _create_actions(self):

        # self.tennyMenu actions
        self.quitAction = QAction('Quit Tenny', self,
                                  triggered=self.close)

        # self.setShortCutKeysMenu actions
        self.startstopAction = QAction('Start or Stop', self,
                                       triggered=self.on_setShortcut_action)
        self.resetAction = QAction('Reset', self,
                                   triggered=self.on_setShortcut_action)

    def _create_menus(self):

        # Sub-menu
        self.setShortCutKeysMenu = QMenu('Set Shortcut Keys')
        self.setShortCutKeysMenu.addAction(self.startstopAction)
        self.setShortCutKeysMenu.addAction(self.resetAction)

        # Main menu
        self.tennyMenu = QMenu()
        self.tennyMenu.addMenu(self.setShortCutKeysMenu)
        self.tennyMenu.addSeparator()
        self.tennyMenu.addAction(self.quitAction)

    def _widgets(self):

        self.shiverTimer = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timerLCDNumber = QLCDNumber()
        self.timerLCDNumber.setDigitCount(12)
        self.timerLCDNumber.display("00:00:00.000")
        self.stortPushButton = QPushButton(self._START)
        self.resetPushButton = QPushButton(self._RESET)
        self.stortPushButton.setToolTip(self.stort_hotkey)
        self.resetPushButton.setToolTip(self.reset_hotkey)
        self.tennySystemTray = QSystemTrayIcon()

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

        # TODO: playing with QSystemTrayIcon here
        self.tennySystemTray.setIcon(QIcon(':/stopwatch-32.png'))
        self.tennySystemTray.setToolTip('Tenny 0.3')
        self.tennySystemTray.setContextMenu(self.tennyMenu)
        self.tennySystemTray.show()

    def _connections(self):

        self.timer.timeout.connect(self.showStopwatch)
        self.stortPushButton.clicked.connect(self.on_stortPushButton_clicked)
        self.resetPushButton.clicked.connect(self.on_resetPushButton_clicked)

    def _hotkeys(self):

        keyboard.add_hotkey(self.stort_hotkey, self.stortPushButton.click)
        keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)

    def _read_settings(self):
        """ Method for restoring Tenny's position, size and values. """

        settings = QSettings('GIPSC Core Team', 'Tenny')
        self.restoreGeometry(settings.value('tenny_geometry', self.saveGeometry()))
        self.stort_hotkey = settings.value('tenny_stort_hotkey')
        self.reset_hotkey = settings.value('tenny_reset_hotkey')
        print('stort:', settings.value('tenny_stort_hotkey'))
        print('reset:', settings.value('tenny_reset_hotkey'))

    def showStopwatch(self):
        """ Event handler for showing elapsed time, just like a stopwatch. """

        self.shiverTimer = self.shiverTimer.addMSecs(1)
        text = self.shiverTimer.toString(self._FORMAT)
        self.timerLCDNumber.display(text)

    def on_stortPushButton_clicked(self):

        if self.stortPushButton.text() == self._START:
            self.timer.start(1)
            self.stortPushButton.setText(self._STOP)
        else:
            self.timer.stop()
            self.stortPushButton.setText(self._START)

    def on_resetPushButton_clicked(self):

        self.timer.stop()
        self.shiverTimer = QTime(0, 0, 0)
        self.timerLCDNumber.display(self.shiverTimer.toString(self._FORMAT))

        if self.stortPushButton.text() == self._STOP:
            self.stortPushButton.setText(self._START)

    def on_setShortcut_action(self):

        which_action = self.sender()
        text = which_action.text()

        from src.dialog.preferences import SetShortcut
        dialog = SetShortcut(self)
        dialog.setWindowTitle('Set Shortcut for {0}'.format(text))

        if dialog.exec():

            print('user preferred shortcut:', dialog.selected_hotkeys)
            if text == 'Start or Stop':
                keyboard.remove_hotkey(self.stort_hotkey)                           # Remove previous hotkey
                self.stort_hotkey = dialog.selected_hotkeys                         # Update self.stort_hotkey
                keyboard.add_hotkey(self.stort_hotkey, self.stortPushButton.click)  # Register new hotkey in keyboard
                self.stortPushButton.setToolTip(self.stort_hotkey)                  # Update tooltip for the button
            else:
                keyboard.remove_hotkey(self.reset_hotkey)
                self.reset_hotkey = dialog.selected_hotkeys
                keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)
                self.resetPushButton.setToolTip(self.reset_hotkey)

    def closeEvent(self, event):

        # TODO: keep Tenny running even if the main window is close
        self.tennySystemTray.showMessage('Tenny', 'You can still found me here :)', QSystemTrayIcon.Information, 3000)
        self._write_settings()

    def _write_settings(self):
        """ Method for saving Tenny's position, size and values. """

        settings = QSettings('GIPSC Core Team', 'Tenny')
        settings.setValue('tenny_geometry', self.saveGeometry())
        settings.setValue('tenny_stort_hotkey', self.stort_hotkey)
        settings.setValue('tenny_reset_hotkey', self.reset_hotkey)
