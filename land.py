import asyncio
import time
from constants import SKILLS, SPECK_OWNER_LINK, BATCH_SIZE, GIVE_UP, FIRST_SPECK, SPECK_RATE, NFT_LAND_LINK
from rate_limiter import AdaptiveRateLimiter
from database import batch_update_players
from profile_utils import lookup_profile
import aiohttp


async def landowners_update(landowner_set: set[str]):
    i = 1

    while i <= 5000:
        time.sleep(.2)
        async with aiohttp.ClientSession() as session, session.get(NFT_LAND_LINK + str(i)) as response:
            if response.status != 200:
                print(f'NFT Land response not Found: {i}')
                await asyncio.sleep(1)
                i += 1
                continue

            data = await response.json()
            player_data = data.get('player', None)
            if player_data is None:
                print(f'No player for NFT Land: {i}')
                i += 1
                continue

            player_id = player_data.get('_id', None)

            if player_id is None:
                print(f'No player for NFT Land: {i}')
                i += 1
                continue

            if player_id not in landowner_set:
                landowner_set.add(player_id)

            i += 1


async def nft_land_data(conn, landowner_set: set[str]):
    set_copy = landowner_set.copy()

    for user_id in set_copy:
        await lookup_profile(conn, user_id)
        time.sleep(.2)


async def speck_data(conn, session):
    i = 0
    nulls = 0
    total_data_batch = []
    skill_data_batch = {skill: [] for skill in SKILLS}
    cursor = await conn.cursor()
    limiter = AdaptiveRateLimiter(3, 1)

    while True:
        if i % BATCH_SIZE == 0:
            print(f'{i} Specks scanned.')
            await batch_update_players(cursor, total_data_batch,
                                       skill_data_batch)
            await conn.commit()
            limiter.reset()

        async with limiter, session.get(SPECK_OWNER_LINK +
                                        str(FIRST_SPECK + i)) as response:
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
                    print(
                        f'Player Data not Found for Speck {FIRST_SPECK + i-GIVE_UP} through Speck {FIRST_SPECK + i}, stopping'
                    )
                    await batch_update_players(cursor, total_data_batch,
                                               skill_data_batch)
                    await conn.commit()
                    limiter.reset()
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
                (id, username, lvl_data['level'], lvl_data['totalExp'],
                 lvl_data['exp']))

    total_data_batch.append((id, username, total_level, total_exp))
