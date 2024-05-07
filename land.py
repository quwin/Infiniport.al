from constants import NFT_LAND_LINK, SPECK_OWNER_LINK, FIRST_SPECK, BATCH_SIZE, SKILLS, GIVE_UP
import asyncio

async def land_owner_update():
    return


async def speck_data(conn, session):
    i = 0
    nulls = 0
    total_data_batch = []
    skill_data_batch = {skill: [] for skill in SKILLS}
    cursor = await conn.cursor()

    while i < 400000:
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
        async with session.get(SPECK_OWNER_LINK + str(FIRST_SPECK + i)) as response:
            if response.status != 200:
                print(f'Speck number not Found: {FIRST_SPECK + i}')
                nulls += 1
                i += 1
                await asyncio.sleep(1)
                continue
            data = await response.json()
            player_data = data.get('player', None)
            if player_data is None:
                if nulls > GIVE_UP:
                    print(
                        f'Player Data not Found for Speck {FIRST_SPECK + i-GIVE_UP} through Speck {FIRST_SPECK + i}, stopping'
                    )
                    return
                else:
                    nulls += 1
                    i += 1
                    await asyncio.sleep(.021)
                    continue
            else:
                nulls = 0

            # Places player data into arrays for batches
            prep_player_info(player_data, total_data_batch, skill_data_batch)

            i += 1
            await asyncio.sleep(.021)


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
