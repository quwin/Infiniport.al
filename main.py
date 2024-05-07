import discord
from discord.ext import commands, tasks
from profile_utils import lookup_profile, embed_profile
from database import init_db, database_remove, init_guild_db
from leaderboard import manage_leaderboard
from constants import TOKEN, NFT_LINK
from guild import guild_data, guild_update
from land import speck_data
import asyncio
import aiosqlite
import aiohttp

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')


@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  await init_db()
  # update_voice_channel_name.start()
  # batch_guild_update.start()
  batch_speck_update.start()

@bot.event
async def on_message(ctx):
  await bot.process_commands(ctx)


@bot.command()
async def lookup(ctx, mid):
  async with aiosqlite.connect('leaderboard.db') as conn:
    c = await conn.cursor()
    (data, total_levels, total_skills) = await lookup_profile(c, mid)
    
    embed = await embed_profile(data, total_levels, total_skills)
    await ctx.channel.send(embed=embed)
    # commit after user recieves message so they dont need to wait
    await conn.commit()

  pass

@bot.command()
async def dbremove(_ctx, mid):
  await database_remove(mid)
  pass

@bot.command()
async def glb(ctx, table_name='total', arg='level', page_number='1'):
    await manage_leaderboard(bot, ctx, table_name, arg, page_number)

@bot.command()
async def lb(ctx, table_name='total', arg='level', page_number='1'):
    server_id = ctx.guild.id
    await manage_leaderboard(bot, ctx, table_name, arg, page_number, server_id=server_id)

@bot.command()
async def assignguild(ctx, guild_name):
  async with aiosqlite.connect('leaderboard.db') as conn, aiohttp.ClientSession() as session:
    data = await guild_data(session, guild_name)
    guild_info = data.get('guild', None)
    if guild_info is None:
      return
    guild_handle = guild_info.get('handle', None)
    if guild_handle is None:
      return
    await init_guild_db(ctx.guild.id, guild_handle, conn)
    await guild_update(conn, data)
    await conn.commit()

@bot.command()
async def chibi(ctx, nft_id):
  await ctx.channel.send(
    f"{NFT_LINK}{nft_id}.gif"
  )
  pass

@tasks.loop(minutes=2880)
async def batch_speck_update():
  async with aiosqlite.connect('leaderboard.db') as conn, aiohttp.ClientSession() as session:
    await speck_data(conn, session)
    await conn.commit()
  
#Not implemented
@tasks.loop(minutes=60)
async def update_voice_channel_name():
  guild_id = 880961748092477453
  return

bot.run(TOKEN)