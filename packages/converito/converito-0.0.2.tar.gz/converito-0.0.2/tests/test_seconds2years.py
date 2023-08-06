import unittest

from converito.seconds2years import seconds2years


class TestSeconds2Years(unittest.TestCase):
    def test_seconds2years(self):
        self.assertEqual(seconds2years(31536000), 1)
        self.assertEqual(seconds2years(63072000), 2)
        self.assertEqual(seconds2years(94608000), 3)


if __name__ == "__main__":
    unittest.main()
