import logging
import sys
import unittest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from src.widget.window import MainWindow


APP = QApplication(sys.argv)


class TestMainWindow(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')
        self.tennyMainWindow = MainWindow()

    def test_startstopPushButton(self):

        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)

        self.assertEqual('&STOP', self.tennyMainWindow.startstopPushButton.text())

    def test_resetPushButton(self):

        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)
        QTest.mouseClick(self.tennyMainWindow.resetPushButton, Qt.LeftButton)

        self.assertEqual('&START', self.tennyMainWindow.startstopPushButton.text())


if __name__ == '__main__':
    unittest.main()
