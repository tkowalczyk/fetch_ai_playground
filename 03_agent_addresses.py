from uagents import Agent, Context
cryptodev = Agent(name="cryptodev", seed="crypto dev recovery phrase")

print("Fetch network address: ", cryptodev.wallet.address())
print("uAgent address: ", cryptodev.address)