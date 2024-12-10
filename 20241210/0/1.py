import asyncio
from time import strftime

async def late(delay, msg):
    await asyncio.sleep(delay)
    print(msg)

async def main():
    print(f"> {strftime('%X')}")
    await late(1, "One")
    print(f"> {strftime('%X')} + 1")
    await late(2, "Two")
    print(f"> {strftime('%X')} + 2")

    task3 = asyncio.create_task(late(3, "Three"))
    task4 = asyncio.create_task(late(4, "Four"))
    await task3
    print(f"> {strftime('%X')} + 3")
    await task4
    print(f"> {strftime('%X')} + <<1>>")

asyncio.run(main())