import asyncio
import time

async def squarer(val):
    return val ** 2

async def doubler(val):
    return 2 * val

async def main(x, y):
    dx, dy = await asyncio.gather(squarer(x), squarer(y))
    dx, dy = await asyncio.gather(doubler(dx), doubler(dy))
    print(dx, dy)
asyncio.run(main(1, 2))