"""
Core operations of Tenny the timer

Demo
    import tenny
    tenny.start_timer()
    'timer started at xx:xx:xx:xx (see tenny.now() to display current time)
    tenny.stop_timer()
    'timer stops at xx:xx::xxx'
    tenny.reset_timer()
    'timer reset at xx:xx:xxx'
"""

from PyQt5.QtCore import (QTime,
                          QTimer,
                          QSettings)
import keyboard


class Stopwatch(QTimer):

    def __init__(self):

        super().__init__()
        self.time = QTime(0, 0, 0, 0)

    def reset(self):

        self.stop()
        self.time = QTime(0, 0, 0, 0)


class Hotkey:

    def __init__(self):

        self.shortcut = str

    def setShortcut(self, shortcut, slot):

        keyboard.add_hotkey(shortcut, slot)
        self.shortcut = shortcut

    def updateShortcut(self, new_shortcut, slot):

        keyboard.remove_hotkey(self.shortcut)
        keyboard.add_hotkey(new_shortcut, slot)
        self.shortcut = new_shortcut


class Settings(QSettings):

    def __init__(self, widget):

        super().__init__()
        self.widget = widget

    def loadSettings(self):

        self.widget.restoreGeometry(self.value('tennyGeometry', self.widget.saveGeometry()))
        self.widget.startstopHotkey.shortcut = self.value('startstopHotkey', self.widget.startstopHotkey.shortcut)
        self.widget.resetHotkey.shortcut = self.value('resetHotkey', self.widget.resetHotkey.shortcut)
        self.widget.unhideHotkey.shortcut = self.value('unhideHotkey', self.widget.unhideHotkey.shortcut)

        self.widget.startstopHotkey.setShortcut(self.widget.startstopHotkey.shortcut, self.widget.startstopPushButton.click)
        self.widget.resetHotkey.setShortcut(self.widget.resetHotkey.shortcut, self.widget.resetPushButton.click)
        self.widget.unhideHotkey.setShortcut(self.widget.unhideHotkey.shortcut, self.widget.unhide)

        self.widget.startstopPushButton.setToolTip(self.widget.startstopHotkey.shortcut)
        self.widget.resetPushButton.setToolTip(self.widget.resetHotkey.shortcut)

    def saveSettings(self):

        self.setValue('tennyGeometry', self.widget.saveGeometry())
        self.setValue('startstopHotkey', self.widget.startstopHotkey.shortcut)
        self.setValue('resetHotkey', self.widget.resetHotkey.shortcut)
        self.setValue('unhideHotkey', self.widget.unhideHotkey.shortcut)
