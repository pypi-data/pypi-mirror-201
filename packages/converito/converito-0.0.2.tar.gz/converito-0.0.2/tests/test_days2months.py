import unittest

from converito.days2months import days2months


class TestDays2Months(unittest.TestCase):
    def test_days2months(self):
        self.assertEqual(days2months(1), 0.0329)
        self.assertEqual(days2months(2), 0.0658)
        self.assertEqual(days2months(3), 0.0986)


if __name__ == "__main__":
    unittest.main()
