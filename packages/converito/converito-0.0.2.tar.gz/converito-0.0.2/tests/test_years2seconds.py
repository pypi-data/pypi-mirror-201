import unittest

from converito.years2seconds import years2seconds


class TestYears2Seconds(unittest.TestCase):
    def test_years2seconds(self):
        self.assertEqual(years2seconds(1), 31536000)
        self.assertEqual(years2seconds(2), 63072000)
        self.assertEqual(years2seconds(3), 94608000)


if __name__ == "__main__":
    unittest.main()
