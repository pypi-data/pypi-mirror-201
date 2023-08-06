import unittest

from converito.minutes2years import minutes2years


class TestMinutes2Years(unittest.TestCase):
    def test_minutes2years(self):
        self.assertEqual(minutes2years(525600), 1)
        self.assertEqual(minutes2years(1051200), 2)
        self.assertEqual(minutes2years(1576800), 3)


if __name__ == "__main__":
    unittest.main()
