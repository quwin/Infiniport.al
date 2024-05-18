import asyncio
import discord
import time
from constants import SKILLS
from database import fetch_job, delete_job, update_job_claimer, add_job

class JobView(discord.ui.View):
    def __init__(self, job_id):
        super().__init__(timeout=None)
        self.job_id = job_id

        # Each button needs to create in __init__() because of how the custom_id 
        # is required to be in the same scope as job_id
        self.claim_button = discord.ui.Button(label="Claim", style=discord.ButtonStyle.green, custom_id=f'claim_{job_id}')
        self.unclaim_button = discord.ui.Button(label="Unclaim", style=discord.ButtonStyle.red, custom_id=f'unclaim_{job_id}')
        self.close_job_button = discord.ui.Button(label="Close Job", style=discord.ButtonStyle.blurple, custom_id=f'close_job_{job_id}')

        self.claim_button.callback = self.claim_button_callback
        self.unclaim_button.callback = self.unclaim_button_callback
        self.close_job_button.callback = self.close_job_button_callback

        self.add_item(self.claim_button)
        self.add_item(self.unclaim_button)
        self.add_item(self.close_job_button)

    async def claim_button_callback(self, interaction: discord.Interaction):
        await self.handle_interaction(interaction, "claim_")

    async def unclaim_button_callback(self, interaction: discord.Interaction):
        await self.handle_interaction(interaction, "unclaim_")

    async def close_job_button_callback(self, interaction: discord.Interaction):
        await self.handle_interaction(interaction, "close_job_")

    async def handle_interaction(self, interaction: discord.Interaction, custom_id: str):
        await update_job(interaction, self, self.job_id, custom_id)
    
    


async def update_job(interaction: discord.Interaction, view, job_id: str, button: str):
  # Retrieve job details from the database
  job = await fetch_job(job_id)
  if job:
    job_id, author_id, item, quantity, reward, details, time_limit, claimer_id  = job
      
    # Avoids API Call to recieve author if not necessary
    member = None
    if interaction.guild is not None:    
        member = interaction.guild.get_member(author_id)
    author = await interaction.client.fetch_user(author_id) if member is None else member

    # Update the embed and job status based on the custom_id
    if button == "claim_":
        if not claimer_id:
            claimer_id = interaction.user.id
            await update_job_claimer(job_id, claimer_id)
            await interaction.response.send_message(f"Job claimed by {interaction.user.mention}!", ephemeral=True)
        else:
            await interaction.response.defer()
            
    elif button == "unclaim_":
        if claimer_id == interaction.user.id or author.id:
            claimer_id = None
            await update_job_claimer(job_id, claimer_id)
        await interaction.response.defer()
        
    elif button == "close_job_":
      if interaction.user.id == author_id:
        await delete_job(job_id)
        await interaction.message.delete()
        return
      elif interaction.user.id == claimer_id:
        await interaction.response.send_message(f"<@{author_id}>, {interaction.user.mention} has ended your job!")
        await delete_job(job_id)
        await interaction.message.delete()
        return
      else:
        await interaction.response.defer()

    embed = await embed_job(author, item, quantity, reward, details, time_limit, claimer_id)
    await interaction.message.edit(embed=embed, view=view)
      

async def embed_job(author,
                    item,
                    quantity,
                    reward,
                    details,
                    time_limit,
                    claimer=None):
  embed = discord.Embed(
      title=
      "<:pixelcoin:1238636808951038092> **New Job Posted!** <:pixelcoin:1238636808951038092>\n",
      color=0x00ff00)
  embed.set_author(name=f"Requested by {author.display_name}",
                   icon_url=f"{author.display_avatar}")
  embed.add_field(name="",
                  value=f"**{quantity}** x {item}\n\n" +
                  "**Additional Info:\n**" + f"{details}\n\n" +
                  "**Reward:**\n" + f"{reward}\n",
                  inline=False)
  embed.add_field(name="Expiration Time:",
                  value=f"<t:{int(time.time()+(float(time_limit)*3600.0))}:R>",
                  inline=False)
  if claimer:
    embed.add_field(name="", value=f"Claimed by <@{claimer}> \n")
  return embed


async def create_job(interaction: discord.Interaction, item, quantity, reward, details, time_limit):
    job_id = str(interaction.id)
    await add_job(job_id, interaction.user.id, item, quantity, reward, details, time_limit, None)
    
    embed = await embed_job(interaction.user, item, quantity, reward, details, time_limit, None)
    await interaction.response.send_message(embed=embed, view=JobView(job_id))
    return job_id