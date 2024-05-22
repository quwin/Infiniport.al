import discord
from job import create_job


class JobInput(discord.ui.Modal, title='Input Task Details:'):
    def __init__(self, client):
        super().__init__()
        self.client = client
        
    item = discord.ui.TextInput(
      label='Item',
      placeholder='Popberry',
      max_length=36,
    )
    
    quantity = discord.ui.TextInput(
      label='Quantity',
      placeholder='12',
      max_length=12,
    )
    
    reward = discord.ui.TextInput(
      label='Reward',
      placeholder='1000 Coins',
      max_length=64,
    )
    
    feedback = discord.ui.TextInput(
      label='What additional information do you have?',
      style=discord.TextStyle.long,
      required=False,
      default = 'N/A',
      max_length=300,
    )
    
    time_limit = discord.ui.TextInput(
      label='When should this job expire? (In Hours)',
      style=discord.TextStyle.long,
      required=False,
      default = '24',
      max_length=3,
    )
    
    async def on_submit(self, interaction: discord.Interaction):
      await create_job(interaction, self.item.value, self.quantity.value,
                     self.reward.value, self.feedback.value,
                     self.time_limit.value)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
    