def decimal2hexadecimal(decimal: int) -> str:
    hexadecimal = ""
    while decimal > 0:
        hexadecimal = str(decimal % 16) + hexadecimal
        decimal = decimal // 16
    return hexadecimal
