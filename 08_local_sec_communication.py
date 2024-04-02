import hashlib
from uagents import Agent, Bureau, Context, Model
from uagents.crypto import Identity
 
class Message(Model):
    message: str
    digest: str
    signature: str

def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()

crypto = Agent(name="crypto", seed="crypto recovery phrase")
dev = Agent(name="dev", seed="dev recovery phrase")

@crypto.on_interval(period=3.0)
async def send_message(ctx: Context):
    msg = "hello from crypto"
    digest = encode(msg)
 
    await ctx.send(
        dev.address,
        Message(message=msg, digest=digest.hex(), signature=crypto.sign_digest(digest)),
    )

@crypto.on_message(model=Message)
async def crypto_message_handler(ctx: Context, sender: str, msg: Message):
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify message"
 
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    ctx.logger.info("Dev's message verified!")

@dev.on_message(model=Message)
async def dev_message_handler(ctx: Context, sender: str, msg: Message):
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify crypto's message"

    ctx.logger.info(f"Received message from {sender}: {msg.message}") 
    ctx.logger.info("Crypot's message verified!")
 
    msg = "hello from dev"
    digest = encode(msg)
 
    await ctx.send(
        crypto.address,
        Message(message=msg, digest=digest.hex(), signature=dev.sign_digest(digest)),
    )

bureau = Bureau()
bureau.add(crypto)
bureau.add(dev)

if __name__ == "__main__":
    bureau.run()