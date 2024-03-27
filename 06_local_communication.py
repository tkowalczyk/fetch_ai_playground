from uagents import Agent, Bureau, Context, Model
 
class Message(Model):
    message: str

crypto = Agent(name="crypto", seed="crypto recovery phrase")
dev = Agent(name="dev", seed="dev recovery phrase")

@crypto.on_interval(period=3.0)
async def send_message(ctx: Context):
    await ctx.send(dev.address, Message(message="hello from crypto"))

@crypto.on_message(model=Message)
async def crypto_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

@dev.on_message(model=Message)
async def dev_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(sender, Message(message="hello there crypto"))

bureau = Bureau()
bureau.add(crypto)
bureau.add(dev)

if __name__ == "__main__":
    bureau.run()