import asyncio
import discord
import time
from constants import SKILLS
from database import fetch_job, delete_job, update_job_claimer, add_job, fetch_unclaimed_jobs
from modal import JobInput, embed_job

class JobView(discord.ui.View):
    def __init__(self, job_id):
        super().__init__(timeout=None)
        self.job_id = job_id
        self.last_bumped = time.time() - 300

        # Each button needs to create in __init__() because of how the custom_id 
        # is required to be in the same scope as job_id
        self.claim_button = discord.ui.Button(label="Claim", style=discord.ButtonStyle.green, custom_id=f'claim_{job_id}')
        self.unclaim_button = discord.ui.Button(label="Unclaim", style=discord.ButtonStyle.red, custom_id=f'unclaim_{job_id}')
        self.close_job_button = discord.ui.Button(label="Close", style=discord.ButtonStyle.blurple, custom_id=f'close_job_{job_id}')
        self.bump_button = discord.ui.Button(label="Bump Task", 
                                            style=discord.ButtonStyle.gray, 
                                            custom_id=f'bump_{job_id}',
                                            row=1)
        self.edit_button = discord.ui.Button(label="Edit Task", 
                                            style=discord.ButtonStyle.gray, 
                                            custom_id=f'edit_{job_id}',
                                            row=1)

        self.claim_button.callback = self.claim_button_callback
        self.unclaim_button.callback = self.unclaim_button_callback
        self.close_job_button.callback = self.close_job_button_callback
        self.bump_button.callback = self.bump_button_callback
        self.edit_button.callback = self.edit_button_callback

        self.add_item(self.claim_button)
        self.add_item(self.unclaim_button)
        self.add_item(self.close_job_button)
        self.add_item(self.bump_button)
        self.add_item(self.edit_button)

    async def claim_button_callback(self, interaction: discord.Interaction):
        await self.handle_interaction(interaction, "claim_")

    async def unclaim_button_callback(self, interaction: discord.Interaction):
        await self.handle_interaction(interaction, "unclaim_")

    async def close_job_button_callback(self, interaction: discord.Interaction):
        await self.handle_interaction(interaction, "close_job_")

    
    async def bump_button_callback(self, interaction: discord.Interaction):
        current_time = time.time()
        wait_time = current_time - self.last_bumped
        if wait_time < 300:
            await interaction.response.send_message(f"You can bump this task again <t:{int(current_time+300-wait_time)}:R>", ephemeral=True)
            return
        self.last_bumped = current_time
        await self.bump_message(interaction)

    
    async def edit_button_callback(self, interaction: discord.Interaction):
        try:
            current_time = time.time()
            wait_time = current_time - self.last_bumped
            if wait_time < 300:
                await interaction.response.send_message(f"You can edit this task again <t:{int(current_time+300-wait_time)}:R>", ephemeral=True)
                return
                
            job_data = await fetch_job(self.job_id)
            if job_data and job_data[1] == interaction.user.id:
                await interaction.response.send_modal(JobInput(self, job_data))
            else:
                await interaction.response.defer()
                return
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request: {e} \nMake sure that Infiniportal has the required permissions for viewing and interacting with this channel!", ephemeral=True)

    
    async def handle_interaction(self, interaction: discord.Interaction, custom_id: str):
        try:
            await interact_job(interaction, self, self.job_id, custom_id)
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request: {e} \nMake sure that Infiniportal has the required permissions for viewing and interacting with this channel!", ephemeral=True)

    
    async def bump_message(self, interaction: discord.Interaction):
        try:
            original_message = interaction.message
            if original_message:
                embed = original_message.embeds[0] if original_message.embeds else None
                await original_message.delete()
                if embed:
                    await interaction.response.send_message(embed=embed, view=self)
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request: {e} \nMake sure that Infiniportal has the required permissions for viewing and interacting with this channel!", ephemeral=True)

async def interact_job(interaction: discord.Interaction, view, job_id: str, button: str):
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
        await interaction.response.defer()
        
    elif button == "unclaim_":
        if claimer_id == interaction.user.id or author.id == interaction.user.id:
            claimer_id = None
            await update_job_claimer(job_id, claimer_id)
        await interaction.response.defer()
        
    elif button == "close_job_":
      if interaction.user.id == claimer_id:
        await interaction.response.send_message(f"<@{author_id}>'s task of {quantity} x {item} has been completed by {interaction.user.mention} for {reward}!")
        await delete_job(job_id)
        await interaction.message.delete()
        return
      elif interaction.user.id == author_id:
        if claimer_id is not None:
            await interaction.response.send_message(f"{interaction.user.mention}'s task of {quantity} x {item} has been completed by <@{claimer_id}> for {reward}!")
            
        await delete_job(job_id)
        await interaction.message.delete()
        return
      else:
        await interaction.response.defer()

    embed = embed_job(author, item, quantity, reward, details, time_limit, claimer_id)
    await interaction.message.edit(embed=embed, view=view)

async def create_job(interaction: discord.Interaction, item, quantity, reward, details, time_limit):
    job_id = str(interaction.id)
    await add_job(job_id, interaction.user.id, item, quantity, reward, details, time_limit, None)
    
    embed = embed_job(interaction.user, item, quantity, reward, details, time_limit, None)
    await interaction.response.send_message(embed=embed, view=JobView(job_id))
    return job_id

async def show_unclaimed_jobs(interaction: discord.Interaction, page_number):
    embed = discord.Embed(title='**Taskboard:**', color=0x00ff00)
    
    list = "----------------------------------------------------\n"
    for job in await fetch_unclaimed_jobs(page_number):
        job_id, author_id, item, quantity, reward, details, time_limit, _  = job
        member = None
        if interaction.guild is not None:    
            member = interaction.guild.get_member(author_id)
        author = await interaction.client.fetch_user(author_id) if member is None else member
        list = list + f"**Requested by** <@{author.id}>\n\n"
        list = list + f"> **{quantity}** x {item} **---->** {reward}\n"
        if details != 'N/A':
            details = format_details_as_blockquote(details)
            list = list + f"> **Additional Info:** \n{details}\n"
        list = list + f"> Expiration Time: <t:{int(time.time()+(float(time_limit)*3600.0))}:R>\n"
        list = list + '----------------------------------------------------\n'
        embed.add_field(name='', value=list, inline=False)
        list = ""
        
    embed.add_field(name='', value="\n Create your own task using `/task create`", inline=False)

    return embed

# Helper function for /taskboard
def format_details_as_blockquote(details: str) -> str:
    lines = details.split('\n')
    formatted_lines = [f"> {line}" for line in lines]
    return '\n'.join(formatted_lines)

#async def post_board(interaction: discord.Interaction):


