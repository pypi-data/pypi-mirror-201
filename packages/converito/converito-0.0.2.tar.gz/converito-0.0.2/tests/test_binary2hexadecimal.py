import unittest

from converito.binary2hexadecimal import binary2hexadecimal


class TestBinary2Hexadecimal(unittest.TestCase):
    def test_binary2hexadecimal(self):
        self.assertEqual(binary2hexadecimal("1010"), "a")
        self.assertEqual(binary2hexadecimal("1111"), "f")
        self.assertEqual(binary2hexadecimal("1001"), "9")


if __name__ == "__main__":
    unittest.main()
