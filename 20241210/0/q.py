import asyncio
import time
async def late(sec):
    s = time.strftime("%X")
    await asyncio.sleep(sec)
    return sec, s, time.strftime('%X')

async def main():
    res = await late(1)
    print(res)
    res = await late(2)
    print(res)
    task1 = asyncio.create_task(late(3))
    task2 = asyncio.create_task(late(4))
    print(await task1)
    print(await task2)


asyncio.run(main())