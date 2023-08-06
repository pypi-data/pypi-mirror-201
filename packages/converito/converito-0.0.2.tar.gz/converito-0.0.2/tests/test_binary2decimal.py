import unittest

from converito.binary2decimal import binary2decimal


class TestBinary2Decimal(unittest.TestCase):
    def test_binary2decimal(self):
        self.assertEqual(binary2decimal("1010"), 10)
        self.assertEqual(binary2decimal("1111"), 15)
        self.assertEqual(binary2decimal("1001"), 9)


if __name__ == "__main__":
    unittest.main()
