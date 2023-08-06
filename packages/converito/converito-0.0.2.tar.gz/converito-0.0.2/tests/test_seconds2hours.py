import unittest

from converito.seconds2hours import seconds2hours


class TestSeconds2Hours(unittest.TestCase):
    def test_seconds2hours(self):
        self.assertEqual(seconds2hours(3600), 1)
        self.assertEqual(seconds2hours(7200), 2)
        self.assertEqual(seconds2hours(10800), 3)


if __name__ == "__main__":
    unittest.main()
