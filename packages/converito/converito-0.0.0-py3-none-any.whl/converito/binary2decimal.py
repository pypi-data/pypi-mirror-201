def binary2decimal(binary: str) -> int:
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i]) * 2 ** (len(binary) - i - 1)
    return decimal
