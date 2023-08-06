import unittest

from converito.minutes2hours import minutes2hours


class TestMinutes2Hours(unittest.TestCase):
    def test_minutes2hours(self):
        self.assertEqual(minutes2hours(1), 0.0167)
        self.assertEqual(minutes2hours(2), 0.0333)
        self.assertEqual(minutes2hours(3), 0.05)


if __name__ == "__main__":
    unittest.main()
