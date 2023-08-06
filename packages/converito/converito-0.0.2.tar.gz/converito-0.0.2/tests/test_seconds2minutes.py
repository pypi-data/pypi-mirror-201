import unittest

from converito.seconds2minutes import seconds2minutes


class TestSeconds2Minutes(unittest.TestCase):
    def test_seconds2minutes(self):
        self.assertEqual(seconds2minutes(60), 1)
        self.assertEqual(seconds2minutes(120), 2)
        self.assertEqual(seconds2minutes(180), 3)


if __name__ == "__main__":
    unittest.main()
