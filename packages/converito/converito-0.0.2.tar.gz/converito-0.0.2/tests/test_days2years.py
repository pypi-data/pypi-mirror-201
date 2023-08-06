import unittest

from converito.days2years import days2years


class TestDays2Years(unittest.TestCase):
    def test_days2years(self):
        self.assertEqual(days2years(365), 0.9993)
        self.assertEqual(days2years(730), 1.9987)
        self.assertEqual(days2years(1095), 2.9980)


if __name__ == "__main__":
    unittest.main()
