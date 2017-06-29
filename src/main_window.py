import keyboard
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QGridLayout, QSystemTrayIcon, QMenu, QAction, QSlider
from PyQt5.QtCore import QTime, QTimer, Qt, QSettings
from PyQt5.QtGui import QIcon
from src.dialog.preferences import SetOpacity
from resources import tenny_resources


__title__ = 'Tenny'
__author__ = 'mokachokokarbon'
__version__ = '0.3-release_candidate'
DEFAULT_STORT_SHORTCUT = 'shift+f1'
DEFAULT_RESET_SHORTCUT = 'shift+f2'
DEFAULT_OPACITY_VALUE = 0.7


class Ten(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._START = '&START'
        self._STOP = '&STOP'
        self._RESET = '&RESET'
        self._FORMAT = 'hh:mm:ss.zzz'
        self.stort_hotkey = DEFAULT_STORT_SHORTCUT
        self.reset_hotkey = DEFAULT_RESET_SHORTCUT
        self.opacity_value = DEFAULT_OPACITY_VALUE
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
        self.openAction = QAction('Open Tenny', self,
                                  triggered=self.on_openTenny_action)
        self.stortAction = QAction('Start/Stop', self,
                                   triggered=self.stort_timer,
                                   shortcut=self.stort_hotkey)
        self.resetAction = QAction('Reset', self,
                                   triggered=self.reset_timer,
                                   shortcut=self.reset_hotkey)

        # self.setShortCutKeysMenu actions
        self.set_startstopAction = QAction('Start/Stop', self,
                                           triggered=self.on_setShortcut_action)
        self.set_resetAction = QAction('Reset', self,
                                       triggered=self.on_setShortcut_action)
        self.set_opacityAction = QAction('Set Opacity', self,
                                         triggered=self.on_setOpacity_action)
        self.quitAction = QAction('Quit Tenny', self,
                                  triggered=self.close)

    def _create_menus(self):

        # Sub-menu
        self.setShortCutKeysMenu = QMenu('Set Shortcut Keys')
        self.setShortCutKeysMenu.addAction(self.set_startstopAction)
        self.setShortCutKeysMenu.addAction(self.set_resetAction)

        # Main menu
        self.tennyMenu = QMenu()
        self.tennyMenu.addAction(self.openAction)
        self.tennyMenu.addAction(self.stortAction)
        self.tennyMenu.addAction(self.resetAction)
        self.tennyMenu.addSeparator()
        self.tennyMenu.addMenu(self.setShortCutKeysMenu)
        self.tennyMenu.addAction(self.set_opacityAction)
        self.tennyMenu.addSeparator()
        self.tennyMenu.addAction(self.quitAction)

    def _widgets(self):

        self.shiverTimer = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timerLCDNumber = QLCDNumber()
        self.stortPushButton = QPushButton(self._START)
        self.resetPushButton = QPushButton(self._RESET)
        self.set_opacityDialog = SetOpacity()
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
        self.setWindowOpacity(self.opacity_value)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.timerLCDNumber.setDigitCount(12)
        self.timerLCDNumber.display("00:00:00.000")

        self.stortPushButton.setToolTip(self.stort_hotkey)
        self.resetPushButton.setToolTip(self.reset_hotkey)

        self.set_opacityDialog.opacityLabel.setText('{:.0f}'.format(self.opacity_value * 100))
        self.set_opacityDialog.opacitySlider.setSliderPosition(self.opacity_value * 100)

        self.tennySystemTray.setIcon(QIcon(':/stopwatch-32.png'))
        self.tennySystemTray.setToolTip('{} {}'.format(__title__, __version__))
        self.tennySystemTray.setContextMenu(self.tennyMenu)
        self.tennySystemTray.show()

    def _connections(self):

        self.timer.timeout.connect(self.showStopwatch)
        self.stortPushButton.clicked.connect(self.on_stortPushButton_clicked)
        self.resetPushButton.clicked.connect(self.on_resetPushButton_clicked)
        self.set_opacityDialog.opacitySlider.valueChanged.connect(self.on_opacitySlider_valueChanged)

    def _hotkeys(self):

        keyboard.add_hotkey(self.stort_hotkey, self.stortPushButton.click)
        keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)

    def _read_settings(self):
        """ Method for restoring Tenny's position, size and values. """

        settings = QSettings('GIPSC Core Team', 'Tenny')
        self.restoreGeometry(settings.value('tenny_geometry', self.saveGeometry()))
        self.stort_hotkey = settings.value('tenny_stort_hotkey', self.stort_hotkey)
        self.reset_hotkey = settings.value('tenny_reset_hotkey', self.reset_hotkey)
        self.opacity_value = float(settings.value('tenny_opacity', self.opacity_value))
        print('stort:', settings.value('tenny_stort_hotkey'))
        print('reset:', settings.value('tenny_reset_hotkey'))
        print('opacity:', settings.value('tenny_opacity'))

    def showStopwatch(self):
        """ Event handler for showing elapsed time, just like a stopwatch. """

        self.shiverTimer = self.shiverTimer.addMSecs(1)
        text = self.shiverTimer.toString(self._FORMAT)
        self.timerLCDNumber.display(text)

    def on_stortPushButton_clicked(self):
        """ Call self.stort_timer to activate the timer. """

        self.stort_timer()

    def stort_timer(self):
        """ Method that will start or stop the timer. """

        if self.stortPushButton.text() == self._START:
            self.timer.start(1)
            self.stortPushButton.setText(self._STOP)
        else:
            self.timer.stop()
            self.stortPushButton.setText(self._START)

    def on_resetPushButton_clicked(self):
        """ Call self.reset_timer to reset the timer. """

        self.reset_timer()

    def reset_timer(self):
        """ Method that will reset the timer. """

        self.timer.stop()
        self.shiverTimer = QTime(0, 0, 0)
        self.timerLCDNumber.display(self.shiverTimer.toString(self._FORMAT))

        if self.stortPushButton.text() == self._STOP:
            self.stortPushButton.setText(self._START)

    def on_openTenny_action(self):
        """ Show Tenny window if its hidden. """

        if self.isHidden():
            self.show()

    def on_setShortcut_action(self):

        which_action = self.sender()
        text = which_action.text()

        from src.dialog.preferences import SetShortcut
        dialog = SetShortcut(self)
        dialog.setWindowTitle('Set Shortcut for {0}'.format(text))

        if dialog.exec():
            print('user preferred shortcut:', dialog.selected_hotkeys)
            if text == 'Start/Stop':
                keyboard.remove_hotkey(self.stort_hotkey)                           # Remove previous hotkey
                self.stort_hotkey = dialog.selected_hotkeys                         # Update self.stort_hotkey
                keyboard.add_hotkey(self.stort_hotkey, self.stortPushButton.click)  # Register new hotkey in keyboard
                self.stortPushButton.setToolTip(self.stort_hotkey)                  # Update tooltip for the button
                self.stortAction.setShortcut(self.stort_hotkey)
            else:
                keyboard.remove_hotkey(self.reset_hotkey)
                self.reset_hotkey = dialog.selected_hotkeys
                keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)
                self.resetPushButton.setToolTip(self.reset_hotkey)
                self.resetAction.setShortcut(self.reset_hotkey)

    def on_setOpacity_action(self):

        self.set_opacityDialog.show()
        self.set_opacityDialog.move(self.tennyMenu.pos())

    def on_opacitySlider_valueChanged(self):

        self.opacity_value = self.set_opacityDialog.opacitySlider.value() / 100
        self.setWindowOpacity(self.opacity_value)
        self.set_opacityDialog.opacityLabel.setText('{:.0f}'.format(self.opacity_value * 100))

    def mousePressEvent(self, QMouseEvent):

        if self.set_opacityDialog.isVisible():
            self.set_opacityDialog.close()

    def closeEvent(self, event):

        who_closes = self.sender()
        if isinstance(who_closes, QAction):
            self._write_settings()
            self.tennySystemTray.hide()
            event.accept()
        else:
            self.hide()
            self.tennySystemTray.showMessage('Tenny', 'You can still found me here :)', QSystemTrayIcon.Information, 3000)
            event.ignore()

    def _write_settings(self):
        """ Method for saving Tenny's position, size and values. """

        settings = QSettings('GIPSC Core Team', 'Tenny')
        settings.setValue('tenny_geometry', self.saveGeometry())
        settings.setValue('tenny_stort_hotkey', self.stort_hotkey)
        settings.setValue('tenny_reset_hotkey', self.reset_hotkey)
        settings.setValue('tenny_opacity', self.opacity_value)
