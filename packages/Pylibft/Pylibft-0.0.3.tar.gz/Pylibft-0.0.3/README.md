# Pylibft
Personal python module for my daily usage on CTF/Pentest/Coding

## Import

```python
from Pylibft import *
```
Or by specifying the Functions

```python
from Pylibft import base_convert, bin2hex
```
## Functions

```python
base_convert(number: str, fromBase: int, toBase: int)
```
Same as the `PHP` function, return a string containing `number` represented in base `toBase`.

```python
bin2hex(string: str)
```
Same as the `PHP` function, return string containing the hexadecimal representation of string.

```python
hex2bin(string: str)
```
Same as the `PHP` function, decode a hexadecimally encoded binary string.

```python
print_message(message: str, type: str)
```
Pretty print with color and type of message.
