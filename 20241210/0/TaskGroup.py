import asyncio
import time

async def squarer(val):
    return val ** 2

async def doubler(val):
    return 2 * val

async def main(x, y):
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(squarer(x))
        task2 = tg.create_task(squarer(y))
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(doubler(task1.result()))
        task2 = tg.create_task(doubler(task2.result()))
    print(task1.result(), task2.result())
asyncio.run(main(2024, 2025))