# Recreating our main window

import logging
from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QPushButton,
                             QHBoxLayout,
                             QVBoxLayout)
from PyQt5.QtCore import Qt
from src.core.tenny import Stopwatch

# [] TODO: create a logger class that can be use anywhere in the codebase
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')


class MainWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.timeformat = 'hh:mm:ss'
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.stopwatch = Stopwatch()
        self.timeLabel = QLabel()
        self.startstopPushButton = QPushButton()
        self.resetPushButton = QPushButton()

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
        self.resetPushButton.setText('&RESET')
        self.setWindowTitle('Tenny')
        self.resize(341, 89)

    def _connections(self):

        self.stopwatch.timeout.connect(self._on_stopwatch_timeout)
        self.stopwatch.timeout.connect(self._update_timeLabel)
        self.stopwatch.timeout.connect(self._debug_message)

        self.startstopPushButton.clicked.connect(self._on_startstopPushButton_clicked)

        self.resetPushButton.clicked.connect(self._on_resetPushButton_clicked)
        self.resetPushButton.clicked.connect(self._update_timeLabel)

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
        logging.debug(f'{self.stopwatch.time.toString(self.timeformat)} stopwatch reset')

    def _update_timeLabel(self):

        self.timeLabel.setText(self.stopwatch.time.toString(self.timeformat))

    def _debug_message(self):

        logging.debug(self.stopwatch.time.toString(self.timeformat))

    # Events
    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()
