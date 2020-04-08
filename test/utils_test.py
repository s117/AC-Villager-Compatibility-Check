import sys
import unittest

from src.data_model import StarSigns, CompatibilityScoreMark, Personality, Species


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
        from src.utils import get_star_sign_by_birthday
        self.assertRaises(ValueError, get_star_sign_by_birthday, (13, 1))
        self.assertRaises(ValueError, get_star_sign_by_birthday, (-1, 0))
        self.assertRaises(ValueError, get_star_sign_by_birthday, (0, -1))
        for expected_ss, births in test_list.items():
            for birth in births:
                actual_ss = get_star_sign_by_birthday(birth)
                self.assertEqual(expected_ss, actual_ss)

    def test_b_get_compatibility_score_by_unicode_sign(self):
        from src.utils import get_compatibility_score_by_unicode_sign
        self.assertEqual(CompatibilityScoreMark.HEART, get_compatibility_score_by_unicode_sign("♥"))
        self.assertEqual(CompatibilityScoreMark.DIAMOND, get_compatibility_score_by_unicode_sign("♦"))
        self.assertEqual(CompatibilityScoreMark.CLOVER, get_compatibility_score_by_unicode_sign("♣"))
        self.assertEqual(CompatibilityScoreMark.CROSS, get_compatibility_score_by_unicode_sign("×"))
        self.assertRaises(ValueError, get_compatibility_score_by_unicode_sign, "")
        self.assertRaises(ValueError, get_compatibility_score_by_unicode_sign, "a")

    def test_c_sanity_test_calculate_compatibility_score_by_personality(self):
        def check(p1, p2):
            from src.utils import calculate_compatibility_score_by_personality
            r1 = calculate_compatibility_score_by_personality(p1, p2)
            r2 = calculate_compatibility_score_by_personality(p2, p1)
            self.assertEqual(r1, r2)
            return r1

        self.assertEqual(
            CompatibilityScoreMark.CLOVER,
            check(Personality.Normal, Personality.Normal)
        )
        self.assertEqual(
            CompatibilityScoreMark.HEART,
            check(Personality.Uchi, Personality.Uchi)
        )
        self.assertEqual(
            CompatibilityScoreMark.CLOVER,
            check(Personality.Snooty, Personality.Snooty)
        )
        self.assertEqual(
            CompatibilityScoreMark.DIAMOND,
            check(Personality.Uchi, Personality.Normal)
        )
        self.assertEqual(
            CompatibilityScoreMark.CROSS,
            check(Personality.Cranky, Personality.Peppy)
        )

    def test_d_sanity_test_calculate_compatibility_score_by_species(self):
        def check(s1, s2):
            from src.utils import calculate_compatibility_score_by_species
            r1 = calculate_compatibility_score_by_species(s1, s2)
            r2 = calculate_compatibility_score_by_species(s2, s1)
            self.assertEqual(r1, r2)
            return r1

        self.assertEqual(
            CompatibilityScoreMark.HEART, check(Species.Bear, Species.Cub)
        )
        self.assertEqual(
            CompatibilityScoreMark.HEART, check(Species.Dog, Species.Wolf)
        )
        self.assertEqual(
            CompatibilityScoreMark.HEART, check(Species.Kangaroo, Species.Koala)
        )

        self.assertEqual(
            CompatibilityScoreMark.DIAMOND, check(Species.Pig, Species.Pig)
        )
        self.assertEqual(
            CompatibilityScoreMark.DIAMOND, check(Species.Deer, Species.Horse)
        )
        self.assertEqual(
            CompatibilityScoreMark.DIAMOND, check(Species.Hamster, Species.Mouse)
        )
        self.assertEqual(
            CompatibilityScoreMark.DIAMOND, check(Species.Mouse, Species.Squirrel)
        )

        self.assertEqual(
            CompatibilityScoreMark.CROSS, check(Species.Cat, Species.Mouse)
        )
        self.assertEqual(
            CompatibilityScoreMark.CROSS, check(Species.Cat, Species.Hamster)
        )
        self.assertEqual(
            CompatibilityScoreMark.CROSS, check(Species.Sheep, Species.Wolf)
        )

        self.assertEqual(
            CompatibilityScoreMark.CLOVER, check(Species.Penguin, Species.Sheep)
        )
        self.assertEqual(
            CompatibilityScoreMark.CLOVER, check(Species.Squirrel, Species.Octopus)
        )
        self.assertEqual(
            CompatibilityScoreMark.CLOVER, check(Species.Hamster, Species.Wolf)
        )
        self.assertEqual(
            CompatibilityScoreMark.CLOVER, check(Species.Deer, Species.Ostrich)
        )


if __name__ == '__main__':
    unittest.main()
