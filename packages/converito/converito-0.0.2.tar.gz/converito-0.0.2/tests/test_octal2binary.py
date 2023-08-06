import unittest

from converito.octal2binary import octal2binary


class TestOctal2Binary(unittest.TestCase):
    def test_octal2binary(self):
        self.assertEqual(octal2binary("7"), "111")
        self.assertEqual(octal2binary("25"), "10101")
        self.assertEqual(octal2binary("26"), "10110")
        self.assertEqual(octal2binary("42"), "100010")


if __name__ == "__main__":
    unittest.main()
