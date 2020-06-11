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
        self.assertEqual('Alt+Q', self.tennyMainWindow.startstopHotkey.shortcut)
        self.assertEqual('Alt+W', self.tennyMainWindow.resetHotkey.shortcut)
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

    def test_keyPressEvent_isQuit(self):

        QTest.keyPress(self.tennyMainWindow, Qt.Key_Q, Qt.ControlModifier)

        self.assertTrue(self.tennyMainWindow.isQuit)
        self.assertTrue(self.tennyMainWindow.close())

    def test_closeEvent_if_tennyMainWindow_isHidden(self):

        self.tennyMainWindow.show()
        self.tennyMainWindow.close()

        self.assertTrue(self.tennyMainWindow.isHidden())

    def test_closeEvent_if_stopwatch_isActive(self):

        QTest.mouseClick(self.tennyMainWindow.startstopPushButton, Qt.LeftButton)
        self.tennyMainWindow.close()

        self.assertTrue(self.tennyMainWindow.stopwatch.isActive())


if __name__ == '__main__':
    unittest.main()
