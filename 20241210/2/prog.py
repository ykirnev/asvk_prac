import asyncio
import random
import sys

async def merge(A, B, start, middle, finish, event_in1, event_in2, event_out):
    await event_in1.wait()
    if middle < finish:
        await event_in2.wait()
    i = start
    j = middle
    id = i
    while i < middle and j < finish:
        if A[i] <= A[j]:
            B[id] = A[i]
            i += 1
        else:
            B[id] = A[j]
            j += 1
        id += 1
    while i < middle:
        B[id] = A[i]
        i += 1
        id += 1
    while j < finish:
        B[id] = A[j]
        j += 1
        id += 1
    event_out.set()

async def mtasks(A):
    n = len(A)
    B = [0] * n
    tasks = []
    events = [asyncio.Event() for _ in range(n)]
    for i in events:
        i.set()
    length = 1
    source, result = A.copy(), B
    while length < n:
        new_len = (n + 2 * length - 1) // (2 * length)
        next_events = [asyncio.Event() for i in range(new_len)]
        for i in range(0, n, 2 * length):
            st = i
            mid = min(i + length, n)
            end = min(i + 2 * length, n)
            event_in1 = events[st // length]
            event_in2 = events[mid//length] if mid != n else asyncio.Event()
            event_out = next_events[st // (2 * length)]
            task = merge(source, result, st, mid, end, event_in1, event_in2, event_out)
            tasks.append(asyncio.create_task(task))
        events = next_events
        source, result = result, source
        length *= 2
    return tasks, source

exec(sys.stdin.read())
