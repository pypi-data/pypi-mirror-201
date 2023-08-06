import unittest

from converito.hours2weeks import hours2weeks


class TestHours2Weeks(unittest.TestCase):
    def test_hours2weeks(self):
        self.assertEqual(hours2weeks(1), 0.006)
        self.assertEqual(hours2weeks(2), 0.0119)
        self.assertEqual(hours2weeks(3), 0.0179)


if __name__ == "__main__":
    unittest.main()
