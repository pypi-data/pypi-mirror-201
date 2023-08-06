import pyexhange

#Buy 1 Ethereum
print(pyexhange.handle_command("trade 1 1 eth"))

#Sell 1 Ethereum
print(pyexhange.handle_command("trade 1 -1 eth"))

#As user 1 send 100 dollars to user 2
print(pyexhange.handle_command("send 1 2 100 USD There_you_go"))

#As user 2 send 100 dollars to user 1
print(pyexhange.handle_command("send 2 1 100 USD There_you_go"))