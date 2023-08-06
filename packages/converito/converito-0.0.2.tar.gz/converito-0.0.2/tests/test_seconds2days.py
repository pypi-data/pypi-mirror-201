import unittest

from converito.seconds2days import seconds2days


class TestSeconds2Days(unittest.TestCase):
    def test_seconds2days(self):
        self.assertEqual(seconds2days(86400), 1)
        self.assertEqual(seconds2days(172800), 2)
        self.assertEqual(seconds2days(259200), 3)


if __name__ == "__main__":
    unittest.main()
