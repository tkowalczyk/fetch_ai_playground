from uagents import Agent, Context
cryptodev = Agent(name="cryptodev", seed="crypto dev recovery phrase")

@cryptodev.on_event("startup")
async def hello_from_agent(ctx: Context):
    ctx.logger.info(f'hello, my name is {ctx.name}')

if __name__ == '__main__':
    cryptodev.run()