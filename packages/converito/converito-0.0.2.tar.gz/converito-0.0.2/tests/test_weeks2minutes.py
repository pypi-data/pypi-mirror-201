import unittest

from converito.weeks2minutes import weeks2minutes


class TestWeeks2Minutes(unittest.TestCase):
    def test_weeks2minutes(self):
        self.assertEqual(weeks2minutes(1), 10080)
        self.assertEqual(weeks2minutes(2), 20160)
        self.assertEqual(weeks2minutes(3), 30240)


if __name__ == "__main__":
    unittest.main()
