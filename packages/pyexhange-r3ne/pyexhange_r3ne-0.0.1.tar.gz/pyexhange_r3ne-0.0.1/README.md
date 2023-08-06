# PyExhange

Welcome to Crypto Trader Game! In this game, you will start with a set amount of money and use it to buy and sell various cryptocurrencies.

# Installation
```
git clone https://github.com/JAAKKQ/pyexhange.git
cd pyexhange
pip install -r requirements.txt
```

# Usage
This can be integrated to any interface (Websites, Telegram, Discord, etc.) with ease.

Example:
```python
import pyexhange

#Buy 1 Ethereum
print(pyexhange.handle_command("trade 1 1 eth"))

#Sell 1 Ethereum
print(pyexhange.handle_command("trade 1 -1 eth"))

#As user 1 send 100 dollars to user 2
print(pyexhange.handle_command("send 1 2 100 USD This_Is_A_Message"))
```
