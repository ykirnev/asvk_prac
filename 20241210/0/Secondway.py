import asyncio
import time
async def late(sec):
    s = time.strftime("%X")
    await asyncio.sleep(sec)
    return sec, s, time.strftime('%X')

async def main():
    print(await asyncio.gather(late(3), late(2)))



asyncio.run(main())