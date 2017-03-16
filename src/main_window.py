from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QGridLayout
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QIcon

__title__ = 'Tenny'
__author__ = 'Jero'
__version__ = 0.1


class Ten(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._START = '&START'
        self._STOP = '&STOP'
        self._RESET = '&RESET'
        self._FORMAT = 'hh:mm:ss.zzz'

        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.shiverTimer = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timerLCDNumber = QLCDNumber()
        self.timerLCDNumber.setDigitCount(12)
        self.timerLCDNumber.display("00:00:00.000")
        self.stortPushButton = QPushButton(self._START)
        self.resetPushButton = QPushButton(self._RESET)

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.timerLCDNumber, 0, 0, 1, 2)
        grid.addWidget(self.stortPushButton, 1, 0)
        grid.addWidget(self.resetPushButton, 1, 1)

        self.setLayout(grid)

    def _properties(self):

        self.setWindowIcon(QIcon('images\chronometer.png'))
        self.resize(350, 125)
        self.setWindowTitle('{} {}'.format(__title__, __version__))
        #self.setWindowOpacity(0.7)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.MSWindowsFixedSizeDialogHint)

    def _connections(self):

        self.timer.timeout.connect(self.showStopwatch)
        self.stortPushButton.clicked.connect(self.on_stortPushButton_clicked)
        self.resetPushButton.clicked.connect(self.on_resetPushButton_clicked)

    def showStopwatch(self):
        """
            Event handler for showing elapsed time, just like a stopwatch
        """

        self.shiverTimer = self.shiverTimer.addMSecs(1)
        text = self.shiverTimer.toString(self._FORMAT)
        self.timerLCDNumber.display(text)

    def on_stortPushButton_clicked(self):

        if self.stortPushButton.text() == self._START:
            self.timer.start(1)                     # Start the timer
            self.stortPushButton.setText(self._STOP)
        else:
            self.timer.stop()                       # Stop the timer
            self.stortPushButton.setText(self._START)

    def on_resetPushButton_clicked(self):

        self.timer.stop()
        self.shiverTimer = QTime(0, 0, 0)
        self.timerLCDNumber.display(self.shiverTimer.toString(self._FORMAT))

        if self.stortPushButton.text() == self._STOP:
            self.stortPushButton.setText(self._START)

    def enterEvent(self, event):

        #print('mouse entering')
        pass

    def leaveEvent(self, event):

        #print('mouse leaving')
        pass