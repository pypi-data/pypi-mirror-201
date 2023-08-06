import unittest

from converito.hours2years import hours2years


class TestHours2Years(unittest.TestCase):
    def test_hours2years(self):
        self.assertEqual(hours2years(1), 0.0001)
        self.assertEqual(hours2years(2), 0.0002)
        self.assertEqual(hours2years(3), 0.0003)


if __name__ == "__main__":
    unittest.main()
