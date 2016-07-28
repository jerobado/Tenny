""" 10K Hours: a timer that will track your progress in coding

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 23 Oct 2015 @ 03:20 AM
 """

import sys

from PyQt5.QtWidgets import QApplication

from src.main_window import Ten

__author__ = 'Jero'

APP = QApplication(sys.argv)

if __name__ == '__main__':
    window = Ten()
    window.show()
    APP.exec_()