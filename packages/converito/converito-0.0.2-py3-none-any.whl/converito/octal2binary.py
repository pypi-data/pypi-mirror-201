from .octal2decimal import octal2decimal
from .decimal2binary import decimal2binary


def octal2binary(octal: str) -> str:
    decimal = octal2decimal(octal)
    binary = decimal2binary(decimal)
    return binary
