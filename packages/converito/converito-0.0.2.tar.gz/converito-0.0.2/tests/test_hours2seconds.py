import unittest

from converito.hours2seconds import hours2seconds


class TestHours2Seconds(unittest.TestCase):
    def test_hours2seconds(self):
        self.assertEqual(hours2seconds(1), 3600)
        self.assertEqual(hours2seconds(2), 7200)
        self.assertEqual(hours2seconds(3), 10800)


if __name__ == "__main__":
    unittest.main()
