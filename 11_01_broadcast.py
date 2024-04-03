from uagents import Agent
from uagents.setup import fund_agent_if_low
from protocol_definition import proto

crypto = Agent(
    name="crypto",
    port=8000,
    seed="crypto recovery phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
fund_agent_if_low(crypto.wallet.address())

crypto.include(proto)

if __name__ == "__main__":
    crypto.run()