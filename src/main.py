""" Tenny: a simple stopwatch application that can be controlled by a hotkey.

    Interface: GUI (PyQt5)
    Language: Python 3.5.2
    Author: mokachokokarbon <tokidokitalkyou@gmail.com>
    Created: 23 Oct 2015 @ 03:20 AM
 """

import sys
from PyQt5.QtWidgets import QApplication
from src.main_window import Ten

__author__ = 'mokachokokarbon'
APP = QApplication(sys.argv)


def configure_app_icon() -> None:
    """ This will show the icon of Betty in the taskbar """

    import ctypes
    APP_ID = u'novus.mokachokokarbon.tenny.04'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

if __name__ == '__main__':
    configure_app_icon()
    window = Ten()
    window.show()
    APP.exec()
