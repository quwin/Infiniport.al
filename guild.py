from constants import GUILD_LINK, GUILD_EMBLEM, GUILD_HOME, SKILLS
from profile_utils import lookup_profile
import aiohttp
import aiosqlite

async def guild_data(session, guild_name):
    async with session.get(GUILD_LINK + guild_name) as response:
        return await response.json()

async def guild_update(cursor, guild_data):
    guild_data_batch = []
    guild_info = guild_data.get('guild', None)
    if guild_info is None:
      return None
    guild_id = guild_info.get('_id', None)
    if guild_id is None:
      return None
    members = guild_data.get('guildMembers', None)
    if members is None:
        print(f"Unable to update guild members for {guild_id}")
        return None
    for member in members:
        if member['role'] == 'Watcher':
            break
        else:
            guild_data_batch.append((member['player']['_id'],
                                     member['player']['username'], 
                                     member['role']))
            
    # Fetch current members in the database
    await cursor.execute(f"SELECT user_id FROM guild_{guild_id}")
    current_members = await cursor.fetchall()
    
    current_member_ids = {row[0] for row in current_members}
    new_member_ids = {member[0] for member in guild_data_batch}
    members_to_remove = current_member_ids - new_member_ids

    # Remove members who have left the guild from the database
    if members_to_remove:
        await cursor.executemany(
            f"DELETE FROM guild_{guild_id} WHERE user_id = ?",
            [(member_id,) for member_id in members_to_remove]
        )
    
    await cursor.executemany(
        f'''INSERT OR REPLACE INTO guild_{guild_id} (user_id, username, role)
        VALUES (?, ?, ?)''', guild_data_batch)

    return new_member_ids

async def all_guilds_data(conn, session):
    i = 1
    total_data_batch = []
    skill_data_batch = {skill: [] for skill in SKILLS}
    cursor = await conn.cursor()
    
    limiter = AdaptiveRateLimiter(3, 1)
    while True:
        async with limiter, session.get(GUILD_HOME + str(i)) as response:
            if response.status != 200:
                print(f'Guild Page {i} response not found:')
                i += 1
                continue
                
            data = await response.json()
            if data.get('guilds', None) is None:
                return
                
            for guild in data['guilds']:
                guild_id = guild.get('_id', None)
                if guild_id is None:
                    continue
                data = await guild_data(session, guild_id)
                members = await guild_update(cursor, guild_data)
                if members is None:
                    continue
                
                
                # Places player data into arrays for batches
                prep_player_info(player_data, total_data_batch, skill_data_batch)
                i += 1