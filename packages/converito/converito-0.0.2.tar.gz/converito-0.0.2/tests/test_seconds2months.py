import unittest

from converito.seconds2months import seconds2months


class TestSeconds2Months(unittest.TestCase):
    def test_seconds2months(self):
        self.assertEqual(seconds2months(2629743), 1.0146)
        self.assertEqual(seconds2months(5259486), 2.0291)
        self.assertEqual(seconds2months(7889229), 3.0437)


if __name__ == "__main__":
    unittest.main()
