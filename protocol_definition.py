from uagents import Model, Protocol, Context

class BroadcastExampleRequest(Model):
    pass

class BroadcastExampleResponse(Model):
    text: str

proto = Protocol(name="proto", version="1.0")
 
@proto.on_message(model=BroadcastExampleRequest, replies=BroadcastExampleResponse)
async def handle_request(ctx: Context, sender: str, _msg: BroadcastExampleRequest):
    await ctx.send(sender, BroadcastExampleResponse(text=f"Hello from {ctx.name}"))