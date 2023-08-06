import unittest

from converito.minutes2days import minutes2days


class TestMinutes2Days(unittest.TestCase):
    def test_minutes2days(self):
        self.assertEqual(minutes2days(1), 0.0007)
        self.assertEqual(minutes2days(2), 0.0014)
        self.assertEqual(minutes2days(3), 0.0021)


if __name__ == "__main__":
    unittest.main()
