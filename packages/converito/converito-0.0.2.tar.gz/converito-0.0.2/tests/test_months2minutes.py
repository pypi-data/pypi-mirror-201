import unittest

from converito.months2minutes import months2minutes


class TestMonths2Minutes(unittest.TestCase):
    def test_months2minutes(self):
        self.assertEqual(months2minutes(1), 43200)
        self.assertEqual(months2minutes(2), 86400)
        self.assertEqual(months2minutes(3), 129600)


if __name__ == "__main__":
    unittest.main()
