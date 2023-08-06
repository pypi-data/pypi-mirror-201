import unittest

from converito.octal2hexadecimal import octal2hexadecimal


class TestOctal2Hexadecimal(unittest.TestCase):
    def test_octal2hexadecimal(self):
        self.assertEqual(octal2hexadecimal("1"), "1")
        self.assertEqual(octal2hexadecimal("2"), "2")
        self.assertEqual(octal2hexadecimal("3"), "3")


if __name__ == "__main__":
    unittest.main()
