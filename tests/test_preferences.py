import logging
import sys
import unittest
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from src.dialog.preferences import PreferencesDialog


class TestPreferencesDialog(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')
        self.preferenceDialog = PreferencesDialog()

    def test_default_properties(self):

        self.assertEqual(381, self.preferenceDialog.width())
        self.assertEqual(149, self.preferenceDialog.height())
        self.assertEqual(QSize(381, 149), self.preferenceDialog.size())


if __name__ == '__main__':
    unittest.main()


