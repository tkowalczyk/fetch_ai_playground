from uagents import Agent, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
from message_models import PaymentRequest, TransactionInfo 

#dev agent address 
SENDER_ADDRESS="agent1q0vvm7p7lyzsy5n49fpwavl3fzku7u22f38565wxwwurga5m3e73jnx6fjp"
AMOUNT = 100
DENOM = "atestfet"

crypto = Agent(
    name="crypto",
    port=8000,
    seed="crypto recovery phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
fund_agent_if_low(crypto.wallet.address())

@crypto.on_interval(period=5.0)
async def request_funds(ctx: Context):
    await ctx.send(
        SENDER_ADDRESS,
        PaymentRequest(
            wallet_address=str(ctx.wallet.address()), amount=AMOUNT, denom=DENOM
        ),
    )

@crypto.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
 
    coin_received = tx_resp.events["coin_received"]
    if (
        coin_received["receiver"] == str(ctx.wallet.address())
        and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")

if __name__ == "__main__":
    crypto.run()