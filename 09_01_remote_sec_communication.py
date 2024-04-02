import hashlib
from uagents import Agent, Context
from uagents.crypto import Identity
from uagents.setup import fund_agent_if_low
from message_models import SignedMessage

def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()

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
    msg = "hello from crypto"
    digest = encode(msg)
 
    await ctx.send(
        RECIPIENT_ADDRESS,
        SignedMessage(message=msg, digest=digest.hex(), signature=crypto.sign_digest(digest)),
    )

@crypto.on_message(model=SignedMessage)
async def message_handler(ctx: Context, sender: str, msg: SignedMessage):
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify dev's message"
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    ctx.logger.info("Dev's message verified!")
 
if __name__ == "__main__":
    crypto.run()