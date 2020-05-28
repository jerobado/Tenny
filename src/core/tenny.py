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
                          QTimer)
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
