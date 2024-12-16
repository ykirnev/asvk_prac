import asyncio

async def writer(queue, delay, stop_event):
    i = 0
    while not stop_event.is_set():
        await asyncio.sleep(delay)
        await queue.put(f"{i}_{delay}")
        i += 1

async def stacker(queue, stack, stop_event):
    while not stop_event.is_set() or not queue.empty():
        if not queue.empty():
            item = await queue.get()
            stack.append(item)
        await asyncio.sleep(0.1)

async def reader(stack, count, delay, stop_event):
    i = 0
    while i < count:
        if stack:
            print(stack.pop(0))
            i += 1
        else:
            await asyncio.sleep(0.1)
        await asyncio.sleep(delay)  #
    stop_event.set()

async def main():
    t1, t2, t3, count = map(int, input().split(','))
    q = asyncio.Queue()
    st = []
    stop_event = asyncio.Event()
    await asyncio.gather(
        writer(q, t1, stop_event),
        writer(q, t2, stop_event),
        stacker(q, st, stop_event),
        reader(st, count, t3, stop_event)
    )

asyncio.run(main())
