from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
 
class Message(Model):
    message: str

#dev agent address 
RECIPIENT_ADDRESS="agent1q0vvm7p7lyzsy5n49fpwavl3fzku7u22f38565wxwwurga5m3e73jnx6fjp"

crypto = Agent(
    name="crypto",
    port=8000,
    seed="crypto recovery phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
fund_agent_if_low(crypto.wallet.address())

@crypto.on_interval(period=2.0)
async def send_message(ctx: Context):
    await ctx.send(RECIPIENT_ADDRESS, Message(message="hello from crypto"))

@crypto.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
 
if __name__ == "__main__":
    crypto.run()