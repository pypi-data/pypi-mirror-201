import unittest

from converito.months2days import months2days


class TestMonths2Days(unittest.TestCase):
    def test_months2days(self):
        self.assertEqual(months2days(1), 30)
        self.assertEqual(months2days(2), 60)
        self.assertEqual(months2days(3), 90)


if __name__ == "__main__":
    unittest.main()
