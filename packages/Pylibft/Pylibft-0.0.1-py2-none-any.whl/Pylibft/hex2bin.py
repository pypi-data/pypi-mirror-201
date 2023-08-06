
"""
Convert a hexadecimal string to binary representation.
"""

def hex2bin(string: str) -> str:
    if string[:2] == "0x":
        string = string[2:]
    binary_data = bytes.fromhex(string)
    return str(binary_data, 'utf-8')
