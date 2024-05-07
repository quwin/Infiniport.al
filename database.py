import aiosqlite
from constants import SKILLS

async def init_db():
    async with aiosqlite.connect('leaderboard.db') as conn:
        c = await conn.cursor()
        await c.execute(
            '''CREATE TABLE IF NOT EXISTS total
            (user_id text PRIMARY KEY, username text, level integer, exp float)'''
        )
        await c.execute(
            '''CREATE TABLE IF NOT EXISTS guilds
            (id text PRIMARY KEY, handle text, emblem text,
            shard_price integer, land_count integer)'''
        )
        await c.execute(
            '''CREATE TABLE IF NOT EXISTS discord_servers
            (server_id text PRIMARY KEY,
            premium boolean, linked_guild text)'''
        )
        for skill in SKILLS:
            await c.execute(
                f'''CREATE TABLE IF NOT EXISTS {skill}
                (user_id text PRIMARY KEY, username text,
                level integer, exp float, current_exp float)'''
            )

        await conn.commit()
    print('Database Initialized!')



async def update_skills(c, json, total_level, total_exp):
    if json is None:
        return
    await c.execute(
      '''INSERT OR REPLACE INTO total (user_id, username, level, exp)
      VALUES (?, ?, ?, ?)''',
      (json['_id'], json['username'], total_level, total_exp))
    for skill in SKILLS:
      skill_data = json['levels'].get(skill, None)
      if skill_data:
          await c.execute(
              f'''INSERT OR REPLACE INTO {skill}
              (user_id, username , level, exp, current_exp) VALUES (?, ?, ?, ?, ?)''',
              (json['_id'], json['username'], skill_data['level'],
               skill_data['totalExp'], skill_data['exp']))
    
    print(f'User ID {json["_id"]} updated!')


async def database_remove(user_id):
  async with aiosqlite.connect('leaderboard.db') as conn:
      c = await conn.cursor()
      await c.execute("DELETE FROM total WHERE user_id = ?", (user_id,))
      try:
          for skill in SKILLS:
              await c.execute(f"DELETE FROM {skill} WHERE user_id = ?", (user_id,))
      except aiosqlite.Error as e:
          print(f"An error occurred: {e}")
      finally:
          await conn.commit()
          print(f"purged {user_id} from database")

async def init_guild_db(server_id, guild_name, conn):
    c = await conn.cursor()
    await c.execute(
        f'''CREATE TABLE IF NOT EXISTS guild_{guild_name}
        (user_id text PRIMARY KEY, username text, role text)'''
    )
    await c.execute(
        '''INSERT OR REPLACE INTO discord_servers (server_id, linked_guild)
        VALUES (?, ?)''',
        (server_id, guild_name)
    )