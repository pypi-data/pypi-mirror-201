import unittest

from converito.octal2decimal import octal2decimal


class TestOctal2Decimal(unittest.TestCase):
    def test_octal2decimal(self):
        self.assertEqual(octal2decimal("1"), 1)
        self.assertEqual(octal2decimal("2"), 2)
        self.assertEqual(octal2decimal("3"), 3)


if __name__ == "__main__":
    unittest.main()
