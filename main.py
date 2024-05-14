import discord
from discord.ext import commands, tasks
from discord import app_commands
from profile_utils import lookup_profile, embed_profile
from database import init_db, database_remove, init_guild_db
from leaderboard import manage_leaderboard
from constants import TOKEN, NFT_LINK
from guild import guild_data, guild_update
from land import speck_data, nft_land_data
from modal import JobInput
import aiosqlite
import aiohttp

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
  await tree.sync(guild=discord.Object(id=880961748092477453))
  print(f'We have logged in as {client.application_id}')
  await init_db()
  # update_voice_channel_name.start()
  # batch_guild_update.start()
  batch_speck_update.start()
  batch_nft_land_update.start()


@tree.command(name="lookup",
              description="Lookup a player's Pixels profile",
              guild=discord.Object(id=880961748092477453))
async def lookup(interaction, input: str):
  async with aiosqlite.connect('leaderboard.db') as conn:
    c = await conn.cursor()
    (data, total_levels, total_skills) = await lookup_profile(c, input)

    embed = await embed_profile(data, total_levels, total_skills)
    await interaction.response.send_message(embed=embed)
    # commit after user recieves message so they dont need to wait
    await conn.commit()

  pass


@commands.hybrid_command()
async def dbremove(_ctx, mid):
  await database_remove(mid)
  pass


@tree.command(name="global_leaderboard",
              description="Look at a ranking of (almost) every Pixels Player!",
              guild=discord.Object(id=880961748092477453))
async def global_leaderboard(interaction,
                             skill: str = 'total',
                             sort: str = 'level',
                             page_number: int = 1):
  await manage_leaderboard(interaction, skill, sort, page_number)


@tree.command(name="leaderboard",
              description="Look at your guild's Leaderboard!",
              guild=discord.Object(id=880961748092477453))
async def leaderboard(interaction,
                      skill: str = 'total',
                      sort: str = 'level',
                      page_number: int = 1):
  server_id = interaction.guild.id
  await manage_leaderboard(interaction, skill, sort, page_number, server_id)


@commands.hybrid_command()
async def assignguild(ctx, guild_name):
  async with aiosqlite.connect(
      'leaderboard.db') as conn, aiohttp.ClientSession() as session:
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


@tree.command(name="job",
              description="Create a claimable job!",
              guild=discord.Object(id=880961748092477453))
async def job(interaction):
  await interaction.response.send_modal(JobInput())


@tree.command(name="chibi",
              description="Show off your Chibi!",
              guild=discord.Object(id=880961748092477453))
async def chibi(interaction, nft_id: str):
  await interaction.response.send_message(f"{NFT_LINK}{nft_id}.gif")


@tasks.loop(minutes=2880)
async def batch_speck_update():
  async with aiosqlite.connect(
      'leaderboard.db') as conn, aiohttp.ClientSession() as session:
    await speck_data(conn, session)
    await conn.commit()


@tasks.loop(minutes=120)
async def batch_nft_land_update():
  async with aiosqlite.connect(
      'leaderboard.db') as conn, aiohttp.ClientSession() as session:
    await nft_land_data(conn, session)
    await conn.commit()


#Not implemented
@tasks.loop(minutes=60)
async def update_voice_channel_name():
  guild_id = 880961748092477453
  return


client.run(TOKEN)
