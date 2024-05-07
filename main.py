import discord
from discord.ext import commands, tasks
from profile_utils import lookup_profile, embed_profile
from database import init_db, database_remove, init_guild_db
from leaderboard import leaderboard, guild_leaderboard
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
    await conn.commit()

  embed = await embed_profile(data, total_levels, total_skills)
  await ctx.channel.send(embed=embed) 
  pass

@bot.command()
async def dbremove(_ctx, mid):
  await database_remove(mid)
  pass

@bot.command()
async def glb(ctx,table_name='total', arg='level' , page_number='1'):
  page = int(page_number)
  if arg == 'exp' or arg == 'level':
    embed = await leaderboard(table_name, arg, max(1, page))
    message = await ctx.channel.send(embed=embed) 
    right = '➡️'
    flip = '🔄'
    left = '⬅️'
    await message.add_reaction(left)
    await message.add_reaction(flip)
    await message.add_reaction(right)

    def check(reaction, user):
      return user != bot.user and str(reaction.emoji) in [left,flip,right] and reaction.message.id == message.id

    while True:
      try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
      except asyncio.TimeoutError:
        await message.clear_reactions()
        break
      else:
        if str(reaction.emoji) == right:
          page += 1
        elif str(reaction.emoji) == left:
          page = max(1, page - 1) 
        elif str(reaction.emoji) == flip:
          arg = 'level' if arg == 'exp' else 'exp'

        embed = await leaderboard(table_name, arg, page)
        await message.edit(embed=embed)
        await message.remove_reaction(reaction, user)
  pass

@bot.command()
async def lb(ctx, table_name='total', arg='level' , page_number='1'):
  page = int(page_number)
  server_id = ctx.guild.id
  if arg == 'exp' or arg == 'level':
    embed = await guild_leaderboard(server_id, table_name, arg, max(1, page))
    message = await ctx.channel.send(embed=embed) 
    right = '➡️'
    flip = '🔄'
    left = '⬅️'
    await message.add_reaction(left)
    await message.add_reaction(flip)
    await message.add_reaction(right)

    def check(reaction, user):
      return user != bot.user and str(reaction.emoji) in [left,flip,right] and reaction.message.id == message.id

    while True:
      try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
      except asyncio.TimeoutError:
        await message.clear_reactions()
        break
      else:
        if str(reaction.emoji) == right:
          page += 1
        elif str(reaction.emoji) == left:
          page = max(1, page - 1) 
        elif str(reaction.emoji) == flip:
          arg = 'level' if arg == 'exp' else 'exp'

        embed = await guild_leaderboard(server_id, table_name, arg, page)
        await message.edit(embed=embed)
        await message.remove_reaction(reaction, user)
  pass

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

@tasks.loop(minutes=60)
async def batch_guild_update():
  async with aiosqlite.connect('leaderboard.db') as conn, aiohttp.ClientSession() as session:
    await guild_update(conn, session)
    await conn.commit()

@tasks.loop(minutes=2880)
async def batch_speck_update():
  async with aiosqlite.connect('leaderboard.db') as conn, aiohttp.ClientSession() as session:
    await speck_data(conn, session)
    await conn.commit()
  

@tasks.loop(minutes=60)
async def update_voice_channel_name():
  guild_id = 880961748092477453
  channel_id = 1235793791026466879
  guild = bot.get_guild(guild_id)
  if guild:
    channel = guild.get_channel(channel_id)
    if channel and isinstance(channel, discord.VoiceChannel):
      guild_json = await guild_data('cookiemonsters')
      fee = guild_json['buyFee']
      new_name = 'Shard Price: ' + str(fee)
      await channel.edit(name=new_name)

bot.run(TOKEN)

async def scroll_page(ctx, embed, table_name, arg, page_number):
  message = await ctx.channel.send(embed=embed) 
  right = '➡️'
  flip = '🔄'
  left = '⬅️'
  await message.add_reaction(left)
  await message.add_reaction(flip)
  await message.add_reaction(right)

  def check(reaction, user):
    return user != bot.user and str(reaction.emoji) in [left,flip,right] and reaction.message.id == message.id

  while True:
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
      await message.clear_reactions()
      break
    else:
      if str(reaction.emoji) == right:
        page_number += 1
      elif str(reaction.emoji) == left:
        page_number = max(1, page_number - 1) 
      elif str(reaction.emoji) == flip:
        arg = 'level' if arg == 'exp' else 'exp'

      embed = await leaderboard(table_name, arg, page_number)
      await message.edit(embed=embed)
      await message.remove_reaction(reaction, user)
  return