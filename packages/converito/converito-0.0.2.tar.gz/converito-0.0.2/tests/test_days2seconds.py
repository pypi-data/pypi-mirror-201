import unittest

from converito.days2seconds import days2seconds


class TestDays2Seconds(unittest.TestCase):
    def test_days2seconds(self):
        self.assertEqual(days2seconds(1), 86400)
        self.assertEqual(days2seconds(2), 172800)
        self.assertEqual(days2seconds(3), 259200)


if __name__ == "__main__":
    unittest.main()
