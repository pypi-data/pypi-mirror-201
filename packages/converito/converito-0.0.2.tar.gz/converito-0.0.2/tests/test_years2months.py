import unittest

from converito.years2months import years2months


class TestYears2Months(unittest.TestCase):
    def test_years2months(self):
        self.assertEqual(years2months(1), 12)
        self.assertEqual(years2months(2), 24)
        self.assertEqual(years2months(3), 36)


if __name__ == "__main__":
    unittest.main()
