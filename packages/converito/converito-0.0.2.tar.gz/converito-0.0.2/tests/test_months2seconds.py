import unittest

from converito.months2seconds import months2seconds


class TestMonths2Seconds(unittest.TestCase):
    def test_months2seconds(self):
        self.assertEqual(months2seconds(1), 2592000)
        self.assertEqual(months2seconds(2), 5184000)
        self.assertEqual(months2seconds(3), 7776000)


if __name__ == "__main__":
    unittest.main()
