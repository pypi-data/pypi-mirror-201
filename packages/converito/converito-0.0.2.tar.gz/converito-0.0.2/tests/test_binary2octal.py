import unittest

from converito.binary2octal import binary2octal


class TestBinary2Octal(unittest.TestCase):
    def test_binary2octal(self):
        self.assertEqual(binary2octal("1001"), "11")
        self.assertEqual(binary2octal("1011111"), "137")
        self.assertEqual(binary2octal("1100110"), "146")


if __name__ == "__main__":
    unittest.main()
