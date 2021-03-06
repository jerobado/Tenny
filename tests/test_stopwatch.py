import logging
import unittest
from src.core.tenny import Stopwatch
from src.widget.window import MainWindow


class TestStopwatch(unittest.TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')
        self.stopwatch = Stopwatch()

    def test_INIT_if_time_equal_zero(self):

        result = self.stopwatch.time.toString('hh:mm:ss.zzz')
        logging.debug(result)

        self.assertEqual('00:00:00.000', result)

    def test_RESET_if_time_equal_zero(self):

        self.stopwatch.reset()
        result = self.stopwatch.time.toString('hh:mm:ss')

        self.assertEqual('00:00:00', result)

    def test_RESET_if_isActive_False(self):

        self.stopwatch.reset()

        self.assertFalse(self.stopwatch.isActive())


if __name__ == '__main__':
    unittest.main()
