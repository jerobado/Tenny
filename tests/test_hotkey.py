import logging
import unittest
import keyboard
from src.core.tenny import Hotkey


class TestHotkey(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')

    def _sample_callback(self):

        logging.debug('sample callback')

    def test_SETSHORTCUT_if_added_to_keyboard(self):

        launchMissileHotkey = Hotkey()
        shortcut = 'alt+g'
        launchMissileHotkey.setShortcut(shortcut, self._sample_callback)

        self.assertIn(shortcut, keyboard._hotkeys.keys())


if __name__ == '__main__':
    unittest.main()
