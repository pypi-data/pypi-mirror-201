import unittest

from converito.weeks2hours import weeks2hours


class TestWeeks2Hours(unittest.TestCase):
    def test_weeks2hours(self):
        self.assertEqual(weeks2hours(1), 168)
        self.assertEqual(weeks2hours(2), 336)
        self.assertEqual(weeks2hours(3), 504)


if __name__ == "__main__":
    unittest.main()
