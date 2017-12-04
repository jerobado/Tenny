import keyboard
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QGridLayout,
                             QSystemTrayIcon,
                             QMenu,
                             QAction,
                             QMessageBox,
                             QLabel,
                             QVBoxLayout,
                             QHBoxLayout)
from PyQt5.QtCore import (QTime,
                          QTimer,
                          Qt,
                          QSettings)
from PyQt5.QtGui import QIcon
from src.dialog.preferences import SetOpacity
from resources import tenny_resources


__title__ = 'Tenny'
__author__ = 'mokachokokarbon'
__version__ = '0.5'
DEFAULT_STORT_SHORTCUT = 'shift+f1'
DEFAULT_RESET_SHORTCUT = 'shift+f2'
DEFAULT_QUIT_SHORCUT = 'ctrl+q'
DEFAULT_OPACITY_VALUE = 0.7


# [] TODO: implement a good logging system
# [] TODO: separate the logic and UI, this class is getting heavier
class Ten(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._START = '&START'
        self._STOP = '&STOP'
        self._RESET = '&RESET'
        self._FORMAT = 's.zzz'
        self.close_shortcut = False
        self.stort_hotkey = DEFAULT_STORT_SHORTCUT
        self.reset_hotkey = DEFAULT_RESET_SHORTCUT
        self.quit_hotkey = DEFAULT_QUIT_SHORCUT
        self.opacity_value = DEFAULT_OPACITY_VALUE
        self._EXISTING_HOTKEYS = {'Start/Stop': DEFAULT_STORT_SHORTCUT,
                                  'Reset': DEFAULT_RESET_SHORTCUT,
                                  'Quit': self.quit_hotkey}
        self._operations = {'Start/Stop': self._update_stort_hotkey,
                            'Reset': self._update_reset_hotkey}
        self.settings = QSettings()
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
        self.set_stortAction = QAction('Start/Stop', self,
                                       triggered=self.on_setShortcut_action)
        self.set_resetAction = QAction('Reset', self,
                                       triggered=self.on_setShortcut_action)
        self.set_opacityAction = QAction('Set Opacity', self,
                                         triggered=self.on_setOpacity_action)
        self.quitAction = QAction('Quit Tenny', self,
                                  shortcut=self.quit_hotkey,
                                  triggered=self.close)

    def _create_menus(self):

        # Sub-menu
        self.setShortCutKeysMenu = QMenu('Set Shortcut Keys')
        self.setShortCutKeysMenu.addAction(self.set_stortAction)
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

        self.tennyTime = QTime()            # The true time
        self.tennyTimer = QTimer()          # The ticker (increments the time)
        self.tennyTimeLabel = QLabel()      # The time display
        self.stortPushButton = QPushButton()
        self.resetPushButton = QPushButton()
        self.setOpacityDialog = SetOpacity()
        self.tennySystemTray = QSystemTrayIcon()
        self.setShortcutMessageBox = QMessageBox(self)

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.tennyTimeLabel, 0, 0, 1, 2)
        grid.addWidget(self.stortPushButton, 1, 0)
        grid.addWidget(self.resetPushButton, 1, 1)
        self.setLayout(grid)

    def _properties(self):

        # Main window
        self.setObjectName('Ten')
        self.setWindowIcon(QIcon(':/stopwatch-32.png'))
        self.resize(341, 89)    # width, height
        self.setWindowTitle(f'{__title__}')
        self.setWindowOpacity(self.opacity_value)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.tennyTime.setHMS(0, 0, 0)  # (hour, minute, second, ms = 0)

        self.tennyTimeLabel.setObjectName('tennyTimeLabel')
        self.tennyTimeLabel.setText(self.tennyTime.toString(self._FORMAT))
        self.tennyTimeLabel.setAlignment(Qt.AlignHCenter)

        self.stortPushButton.setObjectName('stortPushButton')
        self.stortPushButton.setToolTip(self.stort_hotkey)
        self.stortPushButton.setText(self._START)
        self.stortPushButton.setFlat(True)

        self.resetPushButton.setObjectName('resetPushButton')
        self.resetPushButton.setToolTip(self.reset_hotkey)
        self.resetPushButton.setText(self._RESET)
        self.resetPushButton.setFlat(True)

        self.setOpacityDialog.opacityLabel.setText(f'{self.opacity_value * 100:.0f}')
        self.setOpacityDialog.opacitySlider.setSliderPosition(self.opacity_value * 100)

        # SetShortcut QMessageBox
        self.setShortcutMessageBox.setIcon(QMessageBox.Warning)
        self.setShortcutMessageBox.setWindowTitle('Set Shortcut Message')

        self.tennySystemTray.setIcon(QIcon(':/stopwatch-32.png'))
        self.tennySystemTray.setToolTip(f'{__title__} {__version__}')
        self.tennySystemTray.setContextMenu(self.tennyMenu)
        self.tennySystemTray.show()

    def _connections(self):

        self.tennyTimer.timeout.connect(self.on_tennyTimer_timeout)
        self.stortPushButton.clicked.connect(self.on_stortPushButton_clicked)
        self.resetPushButton.clicked.connect(self.on_resetPushButton_clicked)
        self.setOpacityDialog.opacitySlider.valueChanged.connect(self.on_opacitySlider_valueChanged)

    def _hotkeys(self):

        keyboard.add_hotkey(self.stort_hotkey, self.stortPushButton.click)
        keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)

    def _read_settings(self):
        """ Method for restoring Tenny's position, size and values. """

        self.restoreGeometry(self.settings.value('tenny_geometry', self.saveGeometry()))
        self.stort_hotkey = self.settings.value('tenny_stort_hotkey', self.stort_hotkey)
        self.reset_hotkey = self.settings.value('tenny_reset_hotkey', self.reset_hotkey)
        self.opacity_value = float(self.settings.value('tenny_opacity', self.opacity_value))
        self._EXISTING_HOTKEYS.update({'Start/Stop': self.stort_hotkey,
                                       'Reset': self.reset_hotkey})

    def on_tennyTimer_timeout(self):
        """ Event handler for tennyTimer's timeout signal. """

        self.tennyTime = self.tennyTime.addMSecs(1)
        self.update_tennyTime_format()      # This will only update the self._FORMAT if the condition is met
        self.update_timerLabel_text(self._FORMAT)

    def update_tennyTime_format(self):
        """ Update self._FORMAT based on QTime's set condition. """

        if self.tennyTime == QTime(0, 0, 59, 999):
            self._FORMAT = 'm:ss.zzz'
        elif self.tennyTime == QTime(0, 59, 59, 999):
            self._FORMAT = 'h:mm:ss.zzz'
        elif self.tennyTime == QTime(23, 59, 59, 999):
            self._FORMAT = 's.zzz'

    def update_timerLabel_text(self, format: str) -> None:

        format = self.tennyTime.toString(format)
        self.tennyTimeLabel.setText(format)

    def on_stortPushButton_clicked(self):
        """ Call self.stort_timer to activate the tennyTimer. """

        self.stort_timer()

    def stort_timer(self):
        """ Method that will start or stop the tennyTimer. """

        self.start_tenny_timer() if self.stortPushButton.text() == self._START else self.stop_tenny_timer()

    def start_tenny_timer(self):

        self.tennyTimer.start(1)
        self.stortPushButton.setText(self._STOP)

    def stop_tenny_timer(self):

        self.tennyTimer.stop()
        self.stortPushButton.setText(self._START)

    def on_resetPushButton_clicked(self):
        """ Call self.reset_timer to reset tennyTimer. """

        self.reset_timer()

    def reset_timer(self):
        """ Method that will reset tennyTimer. """

        self.tennyTimer.stop()
        self.tennyTime.setHMS(0, 0, 0)
        self._FORMAT = 's.zzz'
        self.update_timerLabel_text(self._FORMAT)

        if self.stortPushButton.text() == self._STOP:
            self.stortPushButton.setText(self._START)

    def on_openTenny_action(self):
        """ Show Tenny window if its hidden. """

        if self.isHidden():
            self.show()

    def on_setShortcut_action(self):

        which_action = self.sender()
        selected_text = which_action.text()

        from src.dialog.preferences import SetShortcut
        dialog = SetShortcut(self)
        dialog.setWindowTitle(f'Set Shortcut for {selected_text}')

        # [x] TODO: make this block of code Pythonic, so far so good
        # [x] TODO: show a notification via Notif area, after update_hotkey()
        if dialog.exec():
            selected_hotkey = dialog.selected_hotkeys
            if selected_hotkey not in self._EXISTING_HOTKEYS.values():
                update_hotkey = self._operations.get(selected_text)
                update_hotkey(selected_text, selected_hotkey)
                self.tennySystemTray.showMessage('Tenny', f'{selected_text} button hotkey updated to {selected_hotkey}',
                                                 QSystemTrayIcon.Information, 4000)
            else:
                hotkey_owner = self._get_hotkey_owner(selected_hotkey)
                self._show_setShortcutMessageBox(selected_hotkey, hotkey_owner)

    def _get_hotkey_owner(self, user_hotkey):
        """ Return the current owner of an existing hotkey. """

        for k, v in self._EXISTING_HOTKEYS.items():
            if user_hotkey == v:
                return k

    def _show_setShortcutMessageBox(self, hotkey, owner):
        """ Set the text and show the message box. """

        self.setShortcutMessageBox.setText(f'\'{hotkey}\' already registered as shortcut for <b>{owner}</b> button. Try again.')
        self.setShortcutMessageBox.show()

    def _update_stort_hotkey(self, text, selected_hotkey):

        keyboard.remove_hotkey(self.stort_hotkey)                           # Remove previous hotkey
        self.stort_hotkey = selected_hotkey                                 # Update self.stort_hotkey
        keyboard.add_hotkey(self.stort_hotkey, self.stortPushButton.click)  # Register new hotkey in keyboard
        self.stortPushButton.setToolTip(self.stort_hotkey)                  # Update tooltip for the button
        self.stortAction.setShortcut(self.stort_hotkey)                     # Update stort QAction
        self._EXISTING_HOTKEYS.update({text: self.stort_hotkey})

    def _update_reset_hotkey(self, text, selected_hotkey):

        keyboard.remove_hotkey(self.reset_hotkey)
        self.reset_hotkey = selected_hotkey
        keyboard.add_hotkey(self.reset_hotkey, self.resetPushButton.click)
        self.resetPushButton.setToolTip(self.reset_hotkey)
        self.resetAction.setShortcut(self.reset_hotkey)
        self._EXISTING_HOTKEYS.update({text: self.reset_hotkey})

    def on_setOpacity_action(self):

        self.setOpacityDialog.show()
        self.setOpacityDialog.move(self.tennyMenu.pos())

    def on_opacitySlider_valueChanged(self):

        self.opacity_value = self.setOpacityDialog.opacitySlider.value() / 100
        self.setWindowOpacity(self.opacity_value)
        self.setOpacityDialog.opacityLabel.setText(f'{self.opacity_value * 100:.0f}')

    def mousePressEvent(self, event):

        if self.setOpacityDialog.isVisible():
            self.setOpacityDialog.close()

    def closeEvent(self, event):

        who_closes = self.sender()
        if isinstance(who_closes, QAction) or self.close_shortcut:
            self._write_settings()
            self.tennySystemTray.hide()
            event.accept()
        else:
            self.hide()
            self.tennySystemTray.showMessage('Tenny', 'You can still found me here :)', QSystemTrayIcon.Information, 3000)
            event.ignore()

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close_shortcut = True
            self.close()

    def _write_settings(self):
        """ Method for saving Tenny's position, size and values. """

        self.settings.setValue('tenny_geometry', self.saveGeometry())
        self.settings.setValue('tenny_stort_hotkey', self.stort_hotkey)
        self.settings.setValue('tenny_reset_hotkey', self.reset_hotkey)
        self.settings.setValue('tenny_opacity', self.opacity_value)

    def resizeEvent(self, QResizeEvent):

        #print(f'{self.height()} x {self.width()}')
        pass
