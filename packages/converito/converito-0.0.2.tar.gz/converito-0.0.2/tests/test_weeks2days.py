import unittest

from converito.weeks2days import weeks2days


class TestWeeks2Days(unittest.TestCase):
    def test_weeks2days(self):
        self.assertEqual(weeks2days(1), 7)
        self.assertEqual(weeks2days(2), 14)
        self.assertEqual(weeks2days(3), 21)


if __name__ == "__main__":
    unittest.main()
