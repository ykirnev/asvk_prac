import asyncio

evesnd = asyncio.Event()
evemid = [asyncio.Event(), asyncio.Event()]

async  def snd():
    evesnd.set()
    print(f"{snd}: generated {evesnd}")

async def mid(k):
    await evesnd.wait()
    print(f"{mid}: recieved {evesnd}")
    evemid[k].set()
    print(f"{mid}: generated {evemid[k]}")

async def rcv():
    await evemid[0].wait()
    print(f"{rcv}: recieved {evemid[0]}")
    await evemid[1].wait()
    print(f"{rcv}: recieved {evemid[1]}")

async def main():
    await asyncio.gather(rcv(), mid(1), mid(0), snd())

asyncio.run(main())