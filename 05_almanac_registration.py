from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol

cryptodev = Agent(
    name="cryptodev", 
    seed="crypto dev recovery phrase",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(cryptodev.wallet.address())
 
@cryptodev.on_interval(period=3)
async def hi(ctx: Context):
    ctx.logger.info(f"Hello")
 
cryptodev.run()