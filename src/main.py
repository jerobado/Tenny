""" Tenny: a simple stopwatch application that can be controlled by a hotkey.

    Interface: GUI (PyQt5)
    Language: Python 3.6.6
    Author: Jero Bado <tokidokitalkyou@gmail.com>
    Created: 23 Oct 2015 @ 03:20 AM
 """

import sys
sys.path.append('..')
from PyQt5.QtWidgets import QApplication
from src.main_window import Ten
from resources import tenny_resources

# [] TODO: add this to constant.py
__author__ = 'Jero Bado'
__version__ = '0.5'
APP = QApplication(sys.argv)
APP.setOrganizationName('GIPSC Core Team')
APP.setApplicationName('Tenny')


def check_tools_version() -> None:
    """ Check tools version for debugging. """

    import sys
    import logging
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'[TEN]: Tenny version {__version__}')
    logging.info(f'[TEN]: Python version {sys.version[:5]}')
    logging.info(f'[TEN]: Qt version {QT_VERSION_STR}')
    logging.info(f'[TEN]: PyQt version {PYQT_VERSION_STR}')
    logging.info(f'[TEN]: SIP version {SIP_VERSION_STR}')


def configure_app_icon() -> None:
    """ This will show the icon of Betty in the taskbar. """

    import ctypes
    APP_ID = u'novus.mokachokokarbon.tenny.05'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


# [] TODO: make this one-liner only
# [] TODO: can be transferred to constant.py
def load_stylesheet():

    stylesheet = open('../qss/style.qss')
    return stylesheet.read()


if __name__ == '__main__':
    check_tools_version()
    configure_app_icon()
    window = Ten()
    window.setStyleSheet(load_stylesheet()) # [] TODO: do this in main_window.py
    window.show()
    APP.exec()
