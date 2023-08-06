from .decimal2binary import decimal2binary
from .hexadecimal2decimal import hexadecimal2decimal


def hexadecimal2binary(hexadecimal: str) -> str:
    decimal = hexadecimal2decimal(hexadecimal)
    binary = decimal2binary(decimal)
    return binary
