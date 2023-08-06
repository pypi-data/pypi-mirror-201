import unittest

from converito.decimal2hexadecimal import decimal2hexadecimal


class TestDecimal2Hexadecimal(unittest.TestCase):
    def test_decimal2hexadecimal(self):
        self.assertEqual(decimal2hexadecimal(1), "1")
        self.assertEqual(decimal2hexadecimal(2), "2")
        self.assertEqual(decimal2hexadecimal(3), "3")


if __name__ == "__main__":
    unittest.main()
