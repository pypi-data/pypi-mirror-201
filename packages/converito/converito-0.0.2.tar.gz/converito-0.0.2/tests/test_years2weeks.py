import unittest

from converito.years2weeks import years2weeks


class TestYears2Weeks(unittest.TestCase):
    def test_years2weeks(self):
        self.assertEqual(years2weeks(1), 52)
        self.assertEqual(years2weeks(2), 104)
        self.assertEqual(years2weeks(3), 156)


if __name__ == "__main__":
    unittest.main()
