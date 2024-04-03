from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from message_models import Message

# crypto agent address 
RECIPIENT_ADDRESS="agent1qtmzf54zukhgn5h0gk8yt4ccnhaym5u0esjh6fzm0xjw06dn45htv0xtvzk"

dev = Agent(
    name="dev",
    port=8001,
    seed="dev recovery phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(dev.wallet.address())

@dev.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    await ctx.send(sender, Message(message="Response from dev"))
 
if __name__ == "__main__":
    dev.run()