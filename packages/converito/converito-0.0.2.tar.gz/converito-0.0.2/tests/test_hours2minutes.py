import unittest

from converito.hours2minutes import hours2minutes


class TestHours2Minutes(unittest.TestCase):
    def test_hours2minutes(self):
        self.assertEqual(hours2minutes(1), 60)
        self.assertEqual(hours2minutes(2), 120)
        self.assertEqual(hours2minutes(3), 180)


if __name__ == "__main__":
    unittest.main()
