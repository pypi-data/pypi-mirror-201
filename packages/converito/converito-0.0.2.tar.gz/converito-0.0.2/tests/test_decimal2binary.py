import unittest

from converito.decimal2binary import decimal2binary


class TestDecimal2Binary(unittest.TestCase):
    def test_decimal2binary(self):
        self.assertEqual(decimal2binary(1), "1")
        self.assertEqual(decimal2binary(2), "10")
        self.assertEqual(decimal2binary(3), "11")


if __name__ == "__main__":
    unittest.main()
