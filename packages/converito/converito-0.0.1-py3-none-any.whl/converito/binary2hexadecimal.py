def binary2hexadecimal(binary: str) -> str:
    hexadecimal = ""
    for i in range(0, len(binary), 4):
        hexadecimal += str(hex(int(binary[i : i + 4], 2))[2:])
    return hexadecimal
