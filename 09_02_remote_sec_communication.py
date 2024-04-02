import hashlib
from uagents import Agent, Context
from uagents.crypto import Identity
from uagents.setup import fund_agent_if_low
from message_models import SignedMessage

def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()

# crypto agent address 
RECIPIENT_ADDRESS="agent1qtmzf54zukhgn5h0gk8yt4ccnhaym5u0esjh6fzm0xjw06dn45htv0xtvzk"

dev = Agent(
    name="dev",
    port=8001,
    seed="dev recovery phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(dev.wallet.address())

@dev.on_message(model=SignedMessage)
async def message_handler(ctx: Context, sender: str, msg: SignedMessage):
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify crypto's message"
    ctx.logger.info(f"Received message from {sender}: {msg.message}") 
    ctx.logger.info("Crypot's message verified!")
 
    msg = "response from dev for verified message"
    digest = encode(msg)
 
    await ctx.send(
        RECIPIENT_ADDRESS,
        SignedMessage(message=msg, digest=digest.hex(), signature=dev.sign_digest(digest)),
    )
 
if __name__ == "__main__":
    dev.run()