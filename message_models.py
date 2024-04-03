from uagents import Model

class SignedMessage(Model):
    message: str
    digest: str
    signature: str

class Message(Model):
    message: str