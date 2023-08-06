"""
Convert string number from a base to another.
"""

import re
from typing import List

def base_convert(number: str, fromBase: int, toBase: int) -> str:
    # Error messages to match original PHP function
    if not (2 <= fromBase <= 36):
        raise ValueError(f"Invalid 'from base' ({fromBase})")
    if not (2 <= toBase <= 36):
        raise ValueError(f"Invalid 'to base' ({toBase})")
    if not re.match(r'^[a-z0-9]+$', number):
        raise ValueError("Invalid characters passed for attempted conversion")

    if fromBase == toBase:
        return number

    number = number.strip()
    if fromBase != 10:
        fromDec = 0
        for c in number:
            v = int(c, fromBase)
            fromDec = fromDec * fromBase + v
    else:
        fromDec = int(number)

    if toBase != 10:
        result: List[str] = []
        while fromDec > 0:
            v = fromDec % toBase
            result.append(int_to_base(v, toBase))
            fromDec //= toBase
        result.reverse()
        return ''.join(result)
    else:
        return str(fromDec)

def int_to_base(n: int, base: int) -> str:
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    while n > 0:
        r = n % base
        result = digits[r] + result
        n //= base
    return result
