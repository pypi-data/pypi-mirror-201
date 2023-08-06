import unittest

from converito.days2minutes import days2minutes


class TestDays2Minutes(unittest.TestCase):
    def test_days2minutes(self):
        self.assertEqual(days2minutes(1), 1440)
        self.assertEqual(days2minutes(2), 2880)
        self.assertEqual(days2minutes(3), 4320)


if __name__ == "__main__":
    unittest.main()
