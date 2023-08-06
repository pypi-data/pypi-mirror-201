import unittest

from converito.hexadecimal2binary import hexadecimal2binary


class TestHexadecimal2Binary(unittest.TestCase):
    def test_hexadecimal2binary(self):
        self.assertEqual(hexadecimal2binary("1"), "1")
        self.assertEqual(hexadecimal2binary("2"), "10")
        self.assertEqual(hexadecimal2binary("3"), "11")


if __name__ == "__main__":
    unittest.main()
