import unittest

from converito.years2hours import years2hours


class TestYears2Hours(unittest.TestCase):
    def test_years2hours(self):
        self.assertEqual(years2hours(1), 8760)
        self.assertEqual(years2hours(2), 17520)
        self.assertEqual(years2hours(3), 26280)


if __name__ == "__main__":
    unittest.main()
