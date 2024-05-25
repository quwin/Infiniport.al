import asyncio
import time

# Limits the number of requests to the API to avoid rate limiting, while not limiting speed if the loop takes longer than the rate limit
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
                await asyncio.sleep(time_to_wait)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        current_time = time.time()
        await self.times.put(current_time)
        self.semaphore.release()