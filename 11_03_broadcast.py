from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocol_definition import BroadcastExampleRequest, BroadcastExampleResponse, proto

degen = Agent(
    name="degen",
    port=8002,
    seed="degen recovery phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)
 
fund_agent_if_low(degen.wallet.address())

@degen.on_interval(period=5)
async def say_hello(ctx: Context):
    await ctx.broadcast(proto.digest, message=BroadcastExampleRequest())
 
@degen.on_message(model=BroadcastExampleResponse)
async def handle_response(ctx: Context, sender: str, msg: BroadcastExampleResponse):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")

if __name__ == "__main__":
    degen.run()