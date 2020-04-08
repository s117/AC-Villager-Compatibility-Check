import sys
import unittest

from data_model import StarSigns
from utils import get_star_sign_by_birthday


class DebuggableTestCase(unittest.TestCase):
    def __add_error_replacement(self, _, err):
        value, traceback = err[1:]
        raise value.with_traceback(traceback)

    def run(self, result=None):
        if result and sys.gettrace() is not None:
            result.addError = self.__add_error_replacement
        super().run(result)


class UtilsTestCase(DebuggableTestCase):

    def test_a_star_sign_convert(self):
        test_list = {
            StarSigns.Aquarius: [(1, 20), (1, 25), (1, 31), (2, 1), (2, 10), (2, 18)],
            StarSigns.Pisces: [(2, 19), (2, 25), (2, 28), (2, 29), (3, 1), (3, 10), (3, 20)],
            StarSigns.Aries: [(3, 21), (3, 25), (3, 31), (4, 1), (4, 10), (4, 19)],
            StarSigns.Taurus: [(4, 20), (4, 25), (4, 30), (5, 1), (5, 10), (5, 20)],
            StarSigns.Gemini: [(5, 21), (5, 25), (5, 31), (6, 1), (6, 10), (6, 20)],
            StarSigns.Cancer: [(6, 21), (6, 25), (6, 30), (7, 1), (7, 10), (7, 22)],
            StarSigns.Leo: [(7, 23), (7, 25), (7, 31), (8, 1), (8, 10), (8, 22)],
            StarSigns.Virgo: [(8, 23), (8, 25), (8, 31), (9, 1), (9, 10), (9, 22)],
            StarSigns.Libra: [(9, 23), (9, 25), (9, 30), (10, 1), (10, 10), (10, 22)],
            StarSigns.Scorpio: [(10, 23), (10, 25), (10, 31), (11, 1), (11, 10), (11, 21)],
            StarSigns.Sagittarius: [(11, 22), (11, 25), (11, 30), (12, 1), (12, 10), (12, 21)],
            StarSigns.Capricorn: [(12, 22), (12, 26), (12, 31), (1, 1), (1, 12), (1, 19)],
        }

        for expected_ss, births in test_list.items():
            for birth in births:
                actual_ss = get_star_sign_by_birthday(birth)
                self.assertEqual(expected_ss, actual_ss)


if __name__ == '__main__':
    unittest.main()
