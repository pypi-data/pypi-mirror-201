"""
Convert binary data into hexadecimal representation.
"""

def bin2hex(string: str) -> str:
    return bytes(string, "utf-8").hex()
