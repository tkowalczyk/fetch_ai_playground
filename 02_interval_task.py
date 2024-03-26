from uagents import Agent, Context
cryptodev = Agent(name="cryptodev", seed="crypto dev recovery phrase")

@cryptodev.on_interval(period=2.0)
async def send_interval_message(ctx: Context):
    ctx.logger.info(f'hello, this is interval task from {ctx.name}')

if __name__ == '__main__':
    cryptodev.run()