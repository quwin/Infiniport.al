import asyncio
import aiohttp
from constants import SKILLS, SPECK_OWNER_LINK, BATCH_SIZE, GIVE_UP, FIRST_SPECK, SPECK_RATE, NFT_LAND_LINK
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

async def nft_land_data(conn, session):
    i = 1
    total_data_batch = []
    skill_data_batch = {skill: [] for skill in SKILLS}
    cursor = await conn.cursor()
    limiter = AdaptiveRateLimiter(SPECK_RATE, 1)

    
    while i <= 5000:
        async with limiter, session.get(NFT_LAND_LINK + str(i)) as response:
            if response.status != 200:
                print(f'NFT Land response not Found: {i}')
                await asyncio.sleep(5)
                i += 1
                continue

            data = await response.json()
            player_data = data.get('player', None)
            if player_data is None:
                i += 1
                continue

            # Places player data into arrays for batches
            prep_player_info(player_data, total_data_batch, skill_data_batch)
            i += 1
    #After scanning all 5,000 Lands
    print(f'{i} Lands scanned.')
    await cursor.executemany(
        '''INSERT OR REPLACE INTO total (user_id, username, level, exp)
      VALUES (?, ?, ?, ?)''', total_data_batch)
    total_data_batch.clear()

    for skill, batch in skill_data_batch.items():
        await cursor.executemany(
            f'''INSERT OR REPLACE INTO {skill}
          (user_id, username, level, exp, current_exp)
          VALUES (?, ?, ?, ?, ?)''', batch)
        batch.clear()

    await conn.commit()



        
async def speck_data(conn, session):
    i = 0
    nulls = 0
    total_data_batch = []
    skill_data_batch = {skill: [] for skill in SKILLS}
    cursor = await conn.cursor()
    limiter = AdaptiveRateLimiter(SPECK_RATE, 1)  # SPECK_RATE requests per second

    while True:
        if i % BATCH_SIZE == 0:
            print(f'{i} Specks scanned.')
            await cursor.executemany(
                '''INSERT OR REPLACE INTO total (user_id, username, level, exp)
              VALUES (?, ?, ?, ?)''', total_data_batch)
            total_data_batch.clear()

            for skill, batch in skill_data_batch.items():
                await cursor.executemany(
                    f'''INSERT OR REPLACE INTO {skill}
                  (user_id, username, level, exp, current_exp)
                  VALUES (?, ?, ?, ?, ?)''', batch)
                batch.clear()

            await conn.commit()

        async with limiter, session.get(SPECK_OWNER_LINK + str(FIRST_SPECK + i)) as response:
            if response.status != 200:
                print(f'Speck number not Found: {FIRST_SPECK + i}')
                await asyncio.sleep(5)
                nulls += 1
                i += 1
                continue

            data = await response.json()
            player_data = data.get('player', None)
            if player_data is None:
                if nulls > GIVE_UP:
                    print(f'Player Data not Found for Speck {FIRST_SPECK + i-GIVE_UP} through Speck {FIRST_SPECK + i}, stopping')
                    return
                else:
                    nulls += 1
                    i += 1
                    continue
            else:
                nulls = 0

            # Places player data into arrays for batches
            prep_player_info(player_data, total_data_batch, skill_data_batch)

            i += 1

def prep_player_info(player_data, total_data_batch, skill_data_batch):
    total_level = 0
    total_exp = 0

    levels = player_data.get('levels', None)
    if levels is None:
        return

    id = player_data.get('_id', None)
    if id is None:
        return

    username = player_data.get('username', None)
    if username is None:
        return

    for skill in SKILLS:
        lvl_data = levels.get(skill, None)
        if lvl_data:
            total_level += lvl_data['level']
            total_exp += lvl_data['totalExp']
            skill_data_batch[skill].append(
                (id, username, lvl_data['level'], lvl_data['totalExp'], lvl_data['exp']))

    total_data_batch.append((id, username, total_level, total_exp))

