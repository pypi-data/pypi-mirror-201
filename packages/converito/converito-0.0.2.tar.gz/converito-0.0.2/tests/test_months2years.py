import unittest

from converito.months2years import months2years


class TestMonths2Years(unittest.TestCase):
    def test_months2years(self):
        self.assertEqual(months2years(12), 1)
        self.assertEqual(months2years(24), 2)
        self.assertEqual(months2years(36), 3)


if __name__ == "__main__":
    unittest.main()
