import unittest

from converito.days2hours import days2hours


class TestDays2Hours(unittest.TestCase):
    def test_days2hours(self):
        self.assertEqual(days2hours(1), 24)
        self.assertEqual(days2hours(2), 48)
        self.assertEqual(days2hours(3), 72)


if __name__ == "__main__":
    unittest.main()
