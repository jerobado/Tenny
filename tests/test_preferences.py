import logging
import sys
import unittest
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QKeySequenceEdit, QPushButton
from src.dialog.preferences import PreferencesDialog

APP = QApplication(sys.argv)


class TestPreferencesDialog(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')
        self.preferenceDialog = PreferencesDialog()

    def test_default_properties(self):

        self.assertEqual('Start/Stop:', self.preferenceDialog.startstopLabel.text())
        self.assertEqual('Reset:', self.preferenceDialog.resetLabel.text())
        self.assertEqual('Unhide:', self.preferenceDialog.unhideLabel.text())
        self.assertEqual('OK', self.preferenceDialog.okPushButton.text())
        self.assertIsInstance(self.preferenceDialog.preferences, dict)
        self.assertIsInstance(self.preferenceDialog.common_hotkey, set)
        self.assertIsInstance(self.preferenceDialog.startstopKeySequenceEdit, QKeySequenceEdit)
        self.assertIsInstance(self.preferenceDialog.resetKeySequenceEdit, QKeySequenceEdit)
        self.assertIsInstance(self.preferenceDialog.unhideKeySequenceEdit, QKeySequenceEdit)
        self.assertIsInstance(self.preferenceDialog.okPushButton, QPushButton)
        self.assertEqual(QSize(381, 149), self.preferenceDialog.size())

    def test_unhideKeySequenceEdit_on_KeySequenceChanged(self):

        QTest.keyPress(self.preferenceDialog.unhideKeySequenceEdit, Qt.Key_D, Qt.ControlModifier)
        QTest.keyPress(self.preferenceDialog.unhideKeySequenceEdit, Qt.Key_4, Qt.ShiftModifier)
        self.assertGreater(len(self.preferenceDialog.unhideKeySequenceEdit.keySequence()), 1)

        self.preferenceDialog._on_KeySequenceChanged()
        self.assertEqual('', self.preferenceDialog.unhideKeySequenceEdit.keySequence().toString())

    def test_get_user_input(self):

        QTest.keyPress(self.preferenceDialog.startstopKeySequenceEdit, Qt.Key_1, Qt.ControlModifier)
        QTest.keyPress(self.preferenceDialog.resetKeySequenceEdit, Qt.Key_2, Qt.ControlModifier)
        QTest.keyPress(self.preferenceDialog.unhideKeySequenceEdit, Qt.Key_3, Qt.ControlModifier)

        self.preferenceDialog.get_user_input()

        self.assertEqual('Ctrl+1', self.preferenceDialog.preferences['new-startstop'])
        self.assertEqual('Ctrl+2', self.preferenceDialog.preferences['new-reset'])
        self.assertEqual('Ctrl+3', self.preferenceDialog.preferences['new-unhide'])

    def test_isHotkeyExist_True(self):

        QTest.keyPress(self.preferenceDialog.startstopKeySequenceEdit, Qt.Key_1, Qt.ControlModifier)

        self.preferenceDialog.get_user_input()
        self.preferenceDialog.existing_hotkeys = ['Ctrl+1', 'Ctrl+2', 'Ctrl+3']

        self.assertTrue(self.preferenceDialog.isHotkeyExist())

    def test_isHotkeyExist_False(self):

        QTest.keyPress(self.preferenceDialog.startstopKeySequenceEdit, Qt.Key_X, Qt.ControlModifier)

        self.preferenceDialog.get_user_input()
        self.preferenceDialog.existing_hotkeys = ['Ctrl+1', 'Ctrl+2', 'Ctrl+3']

        self.assertFalse(self.preferenceDialog.isHotkeyExist())


if __name__ == '__main__':
    unittest.main()


