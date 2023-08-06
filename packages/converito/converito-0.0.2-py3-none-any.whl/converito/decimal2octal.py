def decimal2octal(decimal: int) -> str:
    octal = ""
    while decimal > 0:
        octal = str(decimal % 8) + octal
        decimal = decimal // 8
    return octal
