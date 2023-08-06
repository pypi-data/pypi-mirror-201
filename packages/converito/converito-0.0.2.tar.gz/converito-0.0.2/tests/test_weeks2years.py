import unittest

from converito.weeks2years import weeks2years


class TestWeeks2Years(unittest.TestCase):
    def test_weeks2years(self):
        self.assertEqual(weeks2years(1), 0.0192)
        self.assertEqual(weeks2years(2), 0.0385)
        self.assertEqual(weeks2years(3), 0.0577)


if __name__ == "__main__":
    unittest.main()
