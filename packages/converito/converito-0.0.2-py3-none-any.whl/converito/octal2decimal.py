def octal2decimal(octal: str) -> int:
    decimal = 0
    for i, digit in enumerate(octal[::-1]):
        decimal += int(digit) * 8**i
    return decimal
