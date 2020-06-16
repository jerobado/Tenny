# Recreating our main window

import logging
from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QPushButton,
                             QHBoxLayout,
                             QVBoxLayout,
                             QAction,
                             QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from src.core.tenny import Stopwatch, Hotkey, Settings
from src.widget.systemtray import SystemTrayIcon

# [] TODO: create a logger class that can be use anywhere in the codebase
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')


class MainWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.timeformat = 'hh:mm:ss'
        self.isQuit = False
        self.tennySettings = Settings(self)
        # self.tennySettings.clear()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self.tennySettings.loadSettings()

    def _widgets(self):

        self.preferencesAction = QAction()
        self.contextMenu = QMenu()
        self.stopwatch = Stopwatch()
        self.startstopHotkey = Hotkey()
        self.resetHotkey = Hotkey()
        self.unhideHotkey = Hotkey()
        self.timeLabel = QLabel()
        self.startstopPushButton = QPushButton()
        self.resetPushButton = QPushButton()
        self.tennySystemTray = SystemTrayIcon()

    def _layout(self):

        label = QVBoxLayout()
        label.addWidget(self.timeLabel)

        buttons = QHBoxLayout()
        buttons.addWidget(self.startstopPushButton)
        buttons.addWidget(self.resetPushButton)

        combine = QVBoxLayout()
        combine.addLayout(label)
        combine.addLayout(buttons)

        self.setLayout(combine)

    def _properties(self):

        self.timeLabel.setText('00:00:00')
        self.timeLabel.setAlignment(Qt.AlignHCenter)

        self.startstopPushButton.setText('&START')
        self.startstopHotkey.shortcut = 'Alt+Q'

        self.resetPushButton.setText('&RESET')
        self.resetHotkey.shortcut = 'Alt+W'

        self.unhideHotkey.shortcut = 'Alt+D'

        self.preferencesAction.setText('Preferences')

        self.contextMenu.addAction(self.preferencesAction)

        self.tennySystemTray.setContextMenu(self.contextMenu)
        self.tennySystemTray.show()

        self.setWindowIcon(QIcon(':/stopwatch-32.png'))
        self.setWindowTitle('Tenny')
        self.resize(341, 89)

    def _connections(self):

        self.stopwatch.timeout.connect(self._on_stopwatch_timeout)
        self.stopwatch.timeout.connect(self._update_timeLabel)
        self.stopwatch.timeout.connect(self._debug_message)

        self.startstopPushButton.clicked.connect(self._on_startstopPushButton_clicked)

        self.resetPushButton.clicked.connect(self._on_resetPushButton_clicked)
        self.resetPushButton.clicked.connect(self._update_timeLabel)

        self.tennySystemTray.activated.connect(self._on_tennySystemTray_activated)

        self.preferencesAction.triggered.connect(self._on_preferencesAction_triggered)

    def unhide(self):

        if self.isMinimized() or self.isMaximized() or self.isHidden():
            self.showNormal()

    # Slots
    def _on_stopwatch_timeout(self):

        self.stopwatch.time = self.stopwatch.time.addSecs(1)

    def _on_startstopPushButton_clicked(self):

        if not self.stopwatch.isActive():
            self.stopwatch.start(1000)
            self.startstopPushButton.setText('&STOP')
            logging.debug(f'{self.stopwatch.time.toString(self.timeformat)} stopwatch active')
        else:
            self.stopwatch.stop()
            self.startstopPushButton.setText('&START')
            logging.debug(f'{self.stopwatch.time.toString(self.timeformat)} stopwatch stop')

    def _on_resetPushButton_clicked(self):

        self.stopwatch.reset()
        self.startstopPushButton.setText('&START')
        logging.debug(f'{self.stopwatch.time.toString(self.timeformat)} stopwatch reset')

    def _on_tennySystemTray_activated(self, reason):

        if reason == self.tennySystemTray.Trigger:
            if self.isHidden():
                self.show()

    def _on_preferencesAction_triggered(self):

        from src.dialog.preferences import PreferencesDialog
        dialog = PreferencesDialog(self)
        dialog.startstopHotkey = self.startstopHotkey
        dialog.resetHotkey = self.resetHotkey
        dialog.unhideHotkey = self.unhideHotkey
        dialog.existing_hotkeys = [self.startstopHotkey.shortcut,
                                   self.resetHotkey.shortcut,
                                   self.unhideHotkey.shortcut]
        dialog.startstopPushButton_click = self.startstopPushButton.click
        dialog.resetPushButton_click = self.resetPushButton.click
        dialog.unhide_slot = self.unhide
        dialog.exec()

        # Update button's shortcut tooltip
        self.startstopPushButton.setToolTip(dialog.startstopHotkey.shortcut)
        self.resetPushButton.setToolTip(dialog.resetHotkey.shortcut)

    def _update_timeLabel(self):

        self.timeLabel.setText(self.stopwatch.time.toString(self.timeformat))

    def _debug_message(self):

        logging.debug(self.stopwatch.time.toString(self.timeformat))

    # Events
    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.isQuit = True
            self.close()

    def closeEvent(self, event):

        if self.isQuit:
            self.tennySettings.saveSettings()
            self.tennySystemTray.hide()
            event.accept()
            logging.debug('exited')
        else:
            self.hide()
            event.ignore()
            logging.debug('running in the background')
