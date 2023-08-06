import unittest

from converito.weeks2seconds import weeks2seconds


class TestWeeks2Seconds(unittest.TestCase):
    def test_weeks2seconds(self):
        self.assertEqual(weeks2seconds(1), 604800)
        self.assertEqual(weeks2seconds(2), 1209600)
        self.assertEqual(weeks2seconds(3), 1814400)


if __name__ == "__main__":
    unittest.main()
