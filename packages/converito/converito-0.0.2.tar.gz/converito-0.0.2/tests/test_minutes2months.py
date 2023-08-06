import unittest

from converito.minutes2months import minutes2months


class TestMinutes2Months(unittest.TestCase):
    def test_minutes2months(self):
        self.assertEqual(minutes2months(43800), 1.0139)
        self.assertEqual(minutes2months(87600), 2.0278)
        self.assertEqual(minutes2months(131400), 3.0417)


if __name__ == "__main__":
    unittest.main()
