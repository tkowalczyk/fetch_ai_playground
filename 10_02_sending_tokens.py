from uagents import Agent, Context
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
from message_models import PaymentRequest, TransactionInfo 

# crypto agent address 
RECIPIENT_ADDRESS="agent1qtmzf54zukhgn5h0gk8yt4ccnhaym5u0esjh6fzm0xjw06dn45htv0xtvzk"

dev = Agent(
    name="dev",
    port=8001,
    seed="dev recovery phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(dev.wallet.address())

@dev.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")
 
    # send the payment
    transaction = ctx.ledger.send_tokens(
        msg.wallet_address, msg.amount, msg.denom, ctx.wallet
    )
 
    # send the tx hash so alice can confirm
    await ctx.send(RECIPIENT_ADDRESS, TransactionInfo(tx_hash=transaction.tx_hash))

if __name__ == "__main__":
    dev.run()