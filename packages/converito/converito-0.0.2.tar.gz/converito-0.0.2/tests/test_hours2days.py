import unittest

from converito.hours2days import hours2days


class TestHours2Days(unittest.TestCase):
    def test_hours2days(self):
        self.assertEqual(hours2days(1), 0.0417)
        self.assertEqual(hours2days(2), 0.0833)
        self.assertEqual(hours2days(3), 0.125)


if __name__ == "__main__":
    unittest.main()
