from constants import GUILD_LINK, GUILD_EMBLEM, GUILD_HOME, GUILD_PAGES_TO_UPDATE
from profile_utils import lookup_profile
import aiohttp
import aiosqlite

async def guild_data(session, guild_name):
    async with session.get(GUILD_LINK + guild_name) as response:
        return await response.json()

async def guild_search(session, page_number):
    async with session.get(GUILD_HOME + str(page_number)) as response:
        return response


async def guild_update(conn, guild_data):
    guild_info = guild_data.get('guild', None)
    if guild_info is None:
      return
    guild_handle = guild_info.get('handle', None)
    if guild_handle is None:
      return
    members = guild_data.get('guildMembers', None)
    if members is None:
        print(f"Unable to update guild members for {guild_handle}")
        return
    for member in members:
        if member['role'] == 'Watcher':
            return
        else:
            user_id = member['player']['_id']
            username = member['player']['username']
            await conn.execute(
                f'''INSERT OR REPLACE INTO guild_{guild_handle} (user_id, username, role)
                VALUES (?, ?, ?)''',
                (user_id, username, member['role']))