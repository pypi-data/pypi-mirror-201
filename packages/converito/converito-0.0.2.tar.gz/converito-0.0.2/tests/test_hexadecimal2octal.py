import unittest

from converito.hexadecimal2octal import hexadecimal2octal


class TestHexadecimal2Octal(unittest.TestCase):
    def test_hexadecimal2octal(self):
        self.assertEqual(hexadecimal2octal("1"), "1")
        self.assertEqual(hexadecimal2octal("2"), "2")
        self.assertEqual(hexadecimal2octal("3"), "3")


if __name__ == "__main__":
    unittest.main()
