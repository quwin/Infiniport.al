import asyncio
import time

class AdaptiveRateLimiter:
    def __init__(self, calls, per_second):
        self.calls = calls
        self.per_second = per_second
        self.semaphore = asyncio.Semaphore(calls)
        self.times = []

    async def __aenter__(self):
        await self.semaphore.acquire()
        current_time = time.time()
        if len(self.times) == self.calls:
            oldest_time = self.times.pop(0)
            time_to_wait = oldest_time + self.per_second - current_time
            if time_to_wait > 0:
                await asyncio.sleep(time_to_wait)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        current_time = time.time()
        self.times.append(current_time)
        self.semaphore.release()

    def reset(self):
        self.times.clear()
        self.semaphore = asyncio.Semaphore(self.calls)
