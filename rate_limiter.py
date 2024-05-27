import asyncio
import time

class AdaptiveRateLimiter:
    def __init__(self, calls, per_second):
        self.calls = calls
        self.per_second = per_second
        self.semaphore = asyncio.Semaphore(calls)
        self.times = asyncio.Queue(maxsize=calls)

    async def __aenter__(self):
        await self.semaphore.acquire()
        current_time = time.time()
        if self.times.qsize() == self.calls:
            oldest_time = await self.times.get()
            time_to_wait = oldest_time + self.per_second - current_time
            if time_to_wait > 0:
#                print(f'Waiting for {time_to_wait:.2f} seconds at limiter')
                await asyncio.sleep(time_to_wait)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        current_time = time.time()
        await self.times.put(current_time)
        self.semaphore.release()

    def reset(self):
        self.times = asyncio.Queue(maxsize=self.calls)
        self.semaphore = asyncio.Semaphore(self.calls)