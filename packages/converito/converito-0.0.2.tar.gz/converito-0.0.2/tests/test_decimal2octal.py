import unittest

from converito.decimal2octal import decimal2octal


class TestDecimal2Octal(unittest.TestCase):
    def test_decimal2octal(self):
        self.assertEqual(decimal2octal(1), "1")
        self.assertEqual(decimal2octal(2), "2")
        self.assertEqual(decimal2octal(3), "3")


if __name__ == "__main__":
    unittest.main()
