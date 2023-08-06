import unittest

from converito.years2days import years2days


class TestYears2Days(unittest.TestCase):
    def test_years2days(self):
        self.assertEqual(years2days(1), 365)
        self.assertEqual(years2days(2), 730)
        self.assertEqual(years2days(3), 1095)


if __name__ == "__main__":
    unittest.main()
