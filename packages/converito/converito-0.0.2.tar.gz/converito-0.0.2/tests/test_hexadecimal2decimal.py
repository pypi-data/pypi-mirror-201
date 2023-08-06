import unittest

from converito.hexadecimal2decimal import hexadecimal2decimal


class TestHexadecimal2Decimal(unittest.TestCase):
    def test_hexadecimal2decimal(self):
        self.assertEqual(hexadecimal2decimal("1"), 1)
        self.assertEqual(hexadecimal2decimal("2"), 2)
        self.assertEqual(hexadecimal2decimal("3"), 3)


if __name__ == "__main__":
    unittest.main()
