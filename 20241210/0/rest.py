import asyncio
import time
async def waiter(name, event):
    print(f'{name} waits for {event}…')
    await event.wait()
    print(f'…{name} got it!')

async def eventer(wait, event):
    event.clear()
    print(f"Emitting {event} in {wait} seconds")
    await asyncio.sleep(wait)
    print(f"Emitting {event}…")
    event.set()


async def main():
    event = asyncio.Event()
    await asyncio.gather(
        waiter("One", event),
        waiter("Two", event),
        waiter("3", event),
        waiter("4", event),

        eventer(1, event),
        waiter("One", event),
        waiter("Two", event),
        waiter("3", event),
        waiter("4", event),

        eventer(1, event))

asyncio.run(main())