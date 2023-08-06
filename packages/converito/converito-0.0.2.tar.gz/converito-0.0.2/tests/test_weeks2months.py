import unittest

from converito.weeks2months import weeks2months


class TestWeeks2Months(unittest.TestCase):
    def test_weeks2months(self):
        self.assertEqual(weeks2months(4), 0.9205)
        self.assertEqual(weeks2months(8), 1.8411)
        self.assertEqual(weeks2months(12), 2.7616)


if __name__ == "__main__":
    unittest.main()
