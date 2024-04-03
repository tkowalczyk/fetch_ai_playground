from uagents import Model

class SignedMessage(Model):
    message: str
    digest: str
    signature: str

class Message(Model):
    message: str

class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
 
class TransactionInfo(Model):
    tx_hash: str