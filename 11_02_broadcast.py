from uagents import Agent
from uagents.setup import fund_agent_if_low
from protocol_definition import proto

dev = Agent(
    name="dev",
    port=8001,
    seed="dev recovery phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(dev.wallet.address())

dev.include(proto)

if __name__ == "__main__":
    dev.run()