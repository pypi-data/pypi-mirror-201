import unittest

from converito.months2hours import months2hours


class TestMonths2Hours(unittest.TestCase):
    def test_months2hours(self):
        self.assertEqual(months2hours(1), 720)
        self.assertEqual(months2hours(2), 1440)
        self.assertEqual(months2hours(3), 2160)


if __name__ == "__main__":
    unittest.main()
