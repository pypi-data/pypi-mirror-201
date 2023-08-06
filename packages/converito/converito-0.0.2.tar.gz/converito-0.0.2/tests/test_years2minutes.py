import unittest

from converito.years2minutes import years2minutes


class TestYears2Minutes(unittest.TestCase):
    def test_years2minutes(self):
        self.assertEqual(years2minutes(1), 525600)
        self.assertEqual(years2minutes(2), 1051200)
        self.assertEqual(years2minutes(3), 1576800)


if __name__ == "__main__":
    unittest.main()
