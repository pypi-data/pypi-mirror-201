import unittest

from converito.minutes2seconds import minutes2seconds


class TestMinutes2Seconds(unittest.TestCase):
    def test_minutes2seconds(self):
        self.assertEqual(minutes2seconds(1), 60)
        self.assertEqual(minutes2seconds(2), 120)
        self.assertEqual(minutes2seconds(3), 180)


if __name__ == "__main__":
    unittest.main()
