import asyncio

queue1 = asyncio.Queue()
queue2 = asyncio.Queue()

async def cons():
    while True:
        res = await queue2.get()
        print(f"\tcons: Got {res}, from queue2")

async def prod():
    for i in range(5):
        await queue1.put(f"value{i}")
        print(f"prod: Put queue1: value{i}")
        await asyncio.sleep(1)

async def mid():
    while True:
        res = await queue1.get()
        print(f"\t mid: Got {res}, from queue1")
        await queue2.put(res)
        print(f"mid: Put queue2: {res}")

async def main():
    await asyncio.gather(prod(), mid(), cons())

asyncio.run(main())