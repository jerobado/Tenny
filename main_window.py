__author__ = 'Jero'

import time

from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QTime, QTimer


class Ten(QWidget):

    def __init__(self, parent=None):
        super(Ten, self).__init__(parent)

        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.shiverTimer = QTime(0, 0, 0)
        self.coding_time = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timerLCDNumber = QLCDNumber()
        self.timerLCDNumber.setDigitCount(12)
        self.timerLCDNumber.display("00:00:00.00")
        self.startPushButton = QPushButton("&Start")
        self.stopPushButton = QPushButton("S&top")

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.timerLCDNumber, 0, 0, 1, 2)
        grid.addWidget(self.startPushButton, 1, 0)
        grid.addWidget(self.stopPushButton, 1, 1)

        self.setLayout(grid)

    def _properties(self):

        self.resize(350, 125)
        self.setWindowTitle("10K Hours Tracker | version 0.1")

    def _connections(self):

        #self.timer.timeout.connect(self.showCurrentTime)
        self.timer.timeout.connect(self.showStopwatch)
        self.startPushButton.clicked.connect(self.on_startPushButton_clicked)
        self.stopPushButton.clicked.connect(self.on_stopPushButton_clicked)

    def showCurrentTime(self):
        """
            Event handler for showing the current system clock
        """

        self.time = QTime.currentTime()
        text = self.time.toString('hh:mm')
        print("TEN:", text)
        print("TEN:", self.time.second())
        if (self.time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]
        self.timerLCDNumber.display(text)

    def showStopwatch(self):
        """
            Event handler for showing elapsed time, just like a stopwatch
        """

        self.shiverTimer = self.shiverTimer.addMSecs(1)
        print(self.shiverTimer.msec())
        text = self.shiverTimer.toString('hh:mm:ss.zzz')
        self.timerLCDNumber.display(text)
        print(text)


    def on_startPushButton_clicked(self):

        print("TEN: start timer")
        self.timer.start(1)
        print(self.shiverTimer.hour(), self.shiverTimer.minute(), self.shiverTimer.second())

    def on_stopPushButton_clicked(self):

        self.timer.stop()
