def octal2hexadecimal(octal: str) -> str:
    return hex(int(octal, 8))[2:].upper()
