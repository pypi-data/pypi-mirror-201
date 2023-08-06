import unittest

from converito.days2weeks import days2weeks


class TestDays2Weeks(unittest.TestCase):
    def test_days2weeks(self):
        self.assertEqual(days2weeks(1), 0.1429)
        self.assertEqual(days2weeks(2), 0.2857)
        self.assertEqual(days2weeks(3), 0.4286)


if __name__ == "__main__":
    unittest.main()
