def hexadecimal2decimal(hexadecimal: str) -> int:
    decimal = 0
    for i in range(len(hexadecimal)):
        decimal = decimal * 16 + int(hexadecimal[i], 16)
    return decimal
