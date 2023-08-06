# PyExhange

This code is a Python implementation of a basic wallet system that allows users to buy, sell, and transfer currencies. It includes a JSON database to store user information and currency balances. The code is licensed under the MIT license.

# Installation
```
pip install pyexhange-r3ne
```

# Usage
This can be integrated to any interface (Websites, Telegram, Discord, etc.) with ease.

Example:
```python
from pyexhange import pyexhange

#Buy 1 Ethereum
print(pyexhange.handle_command("trade 1 1 eth"))

#Sell 1 Ethereum
print(pyexhange.handle_command("trade 1 -1 eth"))

#As user 1 send 100 dollars to user 2
print(pyexhange.handle_command("send 1 2 100 USD This_Is_A_Message"))
```
