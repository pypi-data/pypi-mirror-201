from .decimal2octal import decimal2octal
from .hexadecimal2decimal import hexadecimal2decimal


def hexadecimal2octal(hexadecimal: str) -> str:
    decimal = hexadecimal2decimal(hexadecimal)
    octal = decimal2octal(decimal)
    return octal
