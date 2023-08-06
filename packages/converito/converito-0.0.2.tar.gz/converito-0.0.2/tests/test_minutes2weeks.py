import unittest

from converito.minutes2weeks import minutes2weeks


class TestMinutes2Weeks(unittest.TestCase):
    def test_minutes2weeks(self):
        self.assertEqual(minutes2weeks(10080), 1)
        self.assertEqual(minutes2weeks(20160), 2)
        self.assertEqual(minutes2weeks(30240), 3)


if __name__ == "__main__":
    unittest.main()
