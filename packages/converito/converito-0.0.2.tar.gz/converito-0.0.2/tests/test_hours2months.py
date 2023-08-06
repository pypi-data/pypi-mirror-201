import unittest

from converito.hours2months import hours2months


class TestHours2Months(unittest.TestCase):
    def test_hours2months(self):
        self.assertEqual(hours2months(1), 0.0014)
        self.assertEqual(hours2months(2), 0.0028)
        self.assertEqual(hours2months(3), 0.0042)


if __name__ == "__main__":
    unittest.main()
