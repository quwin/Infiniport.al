import discord
from discord import message
from discord import reaction
from discord.ext import commands, tasks
from discord import app_commands
from profile_utils import lookup_profile, embed_profile
from database import init_db, delete_job
from leaderboard import manage_leaderboard
from constants import TOKEN, SkillEnum, SortEnum
from land import speck_data, nft_land_data, landowners_update
from modal import JobInput
from job import JobView, delete_job_message, readd_job_view
from collab_land import collab_channel, CollabButtons
from guild import batch_assigned_guilds_update
import aiosqlite
import aiohttp
import time
from initalize_server import config_channel, firstMessageView
from taskboard import taskboard_embed

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True
intents.presences = True
intents.guilds = True
client = discord.Client(intents=intents, command_prefix='!')
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
  try:
    await init_db()
    await tree.sync(guild=discord.Object(id=1234015429874417706))
    print(f'We have logged in as {client.application_id}')
  except Exception as e:
    print(f"Error: {e}")
    
  await init_job_views(client)
  client.add_view(CollabButtons())
  client.add_view(firstMessageView())
  # batch_speck_update.start()
  batch_nft_land_update.start()
  # update_voice_channel_name.start()
  batch_guild_update.start()
  list_landowners_update.start()
  

@client.event
async def on_guild_join(guild: discord.Guild):
  # Doesn't work if they can be None
  if guild.default_role and guild.me:
    
    settings_overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=False),
      guild.me: discord.PermissionOverwrite(view_channel=True),
    }

    connect_overwrites = {
      guild.default_role: discord.PermissionOverwrite(send_messages=False),
      guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }
    settings = await guild.create_text_channel('infiniportal-config', overwrites=settings_overwrites)
    connect = await guild.create_text_channel('infiniportal-connect', overwrites=connect_overwrites)

    await config_channel(settings)
    await collab_channel(connect)


async def init_job_views(client: discord.Client):
  async with aiosqlite.connect('jobs.db') as db, db.execute('SELECT job_id, time_limit, message_id, channel_id, server_id FROM jobs') as cursor:
    jobs = await cursor.fetchall()
    
  current_time: float  = time.time()
  for row in jobs:
      expiration_date = float(row[1])
      job_id = row[0]
      message_id = row[2]
      channel_id = row[3]
      server_id = row[4]
      if current_time < expiration_date:
        if server_id is None: # backwards compatability + DM compatability
          client.add_view(JobView(job_id, client))
        else:
          view_lifetime = expiration_date - current_time
          try:
            await readd_job_view(client, job_id, view_lifetime, message_id, channel_id, server_id)
          except Exception as e:
            print(f'Job view add on init error: {e},\n{row}')
      else:
        try:
          await delete_job(job_id)
          await delete_job_message(job_id, client)
        except Exception as e:
          print(f'Job delete on init error: {e},\n{row}')
    
@tree.command(name="clear_commands", description="Clear commands",
              guild=discord.Object(id=1234015429874417706))
async def clear_commands(interaction, server: str | None = None):
  if interaction.user.id != 239235420104163328:
    return
  if server:
    tree.clear_commands(guild=discord.Object(id=server))
  else:
    tree.clear_commands(guild=None)
  if server is None:
    await tree.sync()
  else:
    await tree.sync(guild=discord.Object(id=server))
  await interaction.response.send_message('Command tree removed!', ephemeral=True)

@tree.command(name="add_commands", description="Add commands",
             guild=discord.Object(id=1234015429874417706))
async def add_commands(interaction, server: str | None = None):
  if interaction.user.id != 239235420104163328:
    return
  if server is None:
    await tree.sync()
  else:
    await tree.sync(guild=discord.Object(id=int(server)))
  await interaction.response.send_message('Command tree synced!', ephemeral=True)

@tree.command(name="raw_sql", description="break da database",
   guild=discord.Object(id=1234015429874417706))
async def raw_sql(interaction, database: str, execute: str):
  await interaction.response.defer()
  async with aiosqlite.connect(f'{database}.db') as db:
    await db.execute(execute)
    await db.commit()
  await interaction.followup.send(f'Executed command {execute}!')
  
@tree.command(name="lookup",
              description="Lookup a player's Pixels profile")
@app_commands.describe(input="Enter a user's Username, UserID, or Wallet Address")
async def lookup(interaction, input: str):
  try:
    async with aiosqlite.connect('leaderboard.db') as conn:
      c = await conn.cursor()
      result = await lookup_profile(c, input)
      if result is None:
        string = f"Could not find the player `{input}`. Please try again"
        await interaction.response.send_message(string, ephemeral=True)
        return
      (data, total_levels, total_skills) = result
  
      embed = embed_profile(data, total_levels, total_skills)
      await interaction.response.send_message(embed=embed)
  
      await conn.commit()
  except Exception as e:
    if interaction.guild:
      print(f"/lookup error in server {interaction.guild.id} / {interaction.guild.name}: {e}")
    else:
      print(f"No guild in /lookup error! {e}")
    await interaction.followup.send(f"Error: {e}", ephemeral=True)

@tree.command(name="global_leaderboard",
              description="Look at a ranking of (almost) every Pixels Player!")
@app_commands.describe(skill="Select the skill to display",
                       sort="Select the sorting method",
                       page_number="Page number of the leaderboard")
async def global_leaderboard(interaction: discord.Interaction,
                             skill: SkillEnum = SkillEnum.NONE,
                             sort: SortEnum = SortEnum.LEVEL,
                             page_number: int = 1):
  skill_value = skill.value
  sort_value = sort.value
  try:
    await manage_leaderboard(interaction, skill_value, sort_value, page_number)
  except Exception as e:
    if interaction.guild:
      print(f"GLB Error in server {interaction.guild.id} / {interaction.guild.name}: {e}")
    else:
      print(f"No guild in GLB error! {e}")
    await interaction.followup.send(f"Error: {e}", ephemeral=True)


@tree.command(name="leaderboard",
              description="Look at your server's Leaderboard!")
@app_commands.describe(skill="Select the skill to display",
                       sort="Select the sorting method",
                       page_number="Page number of the leaderboard")
async def leaderboard(interaction: discord.Interaction,
                             skill: SkillEnum = SkillEnum.NONE,
                             sort: SortEnum = SortEnum.LEVEL,
                             page_number: int = 1):
  skill_value = skill.value
  sort_value = sort.value
  if interaction.guild is None:
    await interaction.response.send_message("This command can only be used in a server!", ephemeral=True)
    return
  server_id = interaction.guild.id
  try:
    await manage_leaderboard(interaction, skill_value, sort_value, page_number, server_id)
  except Exception as e:
    print(f"Leadboard Error in server {server_id} / {interaction.guild.name}: {e}")
    await interaction.followup.send(f"Error: {e}", ephemeral=True)

# Define the group
job_group = app_commands.Group(name="task", description="View, modify, and create tasks for other users to complete!")

# Create the subjobs
@job_group.command(name="create", description="Create a claimable task!")
async def create(interaction: discord.Interaction):
  view = JobView(interaction.id, client)
  await interaction.response.send_modal(JobInput(view))

tree.add_command(job_group)

# Main /taskboard
@tree.command(name="taskboard",
  description="View the tasks available to complete!")
@app_commands.describe(page_number="Enter the page to go to")
async def taskboard(interaction: discord.Interaction, page_number: int = 1):
  try:
    boolean = bool(interaction.guild)
    embed = await taskboard_embed(interaction, min(1, page_number), boolean)
    await interaction.response.send_message(embed=embed, ephemeral=True)
  except Exception as e:
    if interaction.guild:
      print(f"Taskboard error in server {interaction.guild.id} / {interaction.guild.name}: {e}")
    else:
      print(f"No guild in Taskboard error! {e}")
    await interaction.response.send_message(f"Error: {e}", ephemeral=True)

@tasks.loop(minutes=2880)
async def batch_speck_update():
  async with aiosqlite.connect(
      'leaderboard.db') as conn, aiohttp.ClientSession() as session:
    await speck_data(conn, session)

landowner_set: set[str] = {'65e3dd3bebdfdac278077b85'} # My id cause why not

@tasks.loop(minutes=720)
async def list_landowners_update():
  async with aiohttp.ClientSession() as session:
    await landowners_update(session, landowner_set)

@tasks.loop(minutes=30)
async def batch_nft_land_update():
  async with aiosqlite.connect(
      'leaderboard.db') as conn:
    await nft_land_data(conn, landowner_set)

@tasks.loop(minutes=60)
async def batch_guild_update():
  await batch_assigned_guilds_update()

@tasks.loop(minutes=60)
async def update_voice_channel_name():
  guild_id = 880961748092477453
  return

client.run(TOKEN)
