import unittest

from converito.months2weeks import months2weeks


class TestMonths2Weeks(unittest.TestCase):
    def test_months2weeks(self):
        self.assertEqual(months2weeks(1), 4)
        self.assertEqual(months2weeks(2), 8)
        self.assertEqual(months2weeks(3), 12)


if __name__ == "__main__":
    unittest.main()
