import logging
import sys
import unittest
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from src.widget.window import MainWindow


APP = QApplication(sys.argv)


class TestMainWindow(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')
        self.tennyMainWindow = MainWindow()

    def test_default_properties(self):

        self.assertEqual('00:00:00', self.tennyMainWindow.timeLabel.text())
        self.assertEqual('&START', self.tennyMainWindow.startstopPushButton.text())
        self.assertEqual('&RESET', self.tennyMainWindow.resetPushButton.text())
        self.assertEqual('Tenny', self.tennyMainWindow.windowTitle())
        self.assertEqual('alt+q', self.tennyMainWindow.startstopHotkey.shortcut)
        self.assertEqual('alt+w', self.tennyMainWindow.resetHotkey.shortcut)
        self.assertEqual(QSize(341, 89), self.tennyMainWindow.size())

    def test_startstopPushButton_start(self):

        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)

        self.assertTrue(self.tennyMainWindow.stopwatch.isActive())
        self.assertEqual('&STOP', self.tennyMainWindow.startstopPushButton.text())

    def test_starstopPushButton_stop(self):

        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)
        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)

        self.assertFalse(self.tennyMainWindow.stopwatch.isActive())
        self.assertEqual('&START', self.tennyMainWindow.startstopPushButton.text())

    def test_resetPushButton(self):

        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)
        QTest.mouseClick(self.tennyMainWindow.resetPushButton, Qt.LeftButton)

        self.assertEqual('&START', self.tennyMainWindow.startstopPushButton.text())


if __name__ == '__main__':
    unittest.main()