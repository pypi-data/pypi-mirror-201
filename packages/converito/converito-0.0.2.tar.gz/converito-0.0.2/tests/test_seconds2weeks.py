import unittest

from converito.seconds2weeks import seconds2weeks


class TestSeconds2Weeks(unittest.TestCase):
    def test_seconds2weeks(self):
        self.assertEqual(seconds2weeks(604800), 1)
        self.assertEqual(seconds2weeks(1209600), 2)
        self.assertEqual(seconds2weeks(1814400), 3)


if __name__ == "__main__":
    unittest.main()
