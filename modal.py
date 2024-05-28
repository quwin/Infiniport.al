import discord
import time
from database import add_job

class JobInput(discord.ui.Modal, title='Input Task Details:'):
    def __init__(self, view, job_data = None):
        super().__init__()
        self.view = view
        if job_data is not None:
            self.job_data = {
                'job_id': job_data[0],
                'author_id': job_data[1],
                'item': job_data[2],
                'quantity': job_data[3],
                'reward': job_data[4],
                'details': job_data[5],
                'time_limit': int(job_data[6]),
                'claimer_id': job_data[7],
            }
        else:
            self.job_data = {}
        self.add_item(discord.ui.TextInput(
            label='Item',
            placeholder='Popberry',
            default= self.job_data.get('item', None),
            max_length=36,
        ))

        self.add_item(discord.ui.TextInput(
            label='Quantity',
            placeholder='12',
            default= self.job_data.get('quantity', None),
            max_length=12,
        ))

        self.add_item(discord.ui.TextInput(
            label='Reward',
            placeholder='1000 Coins',
            default= self.job_data.get('reward', None),
            max_length=64,
        ))

        self.add_item(discord.ui.TextInput(
            label='What additional information do you have?',
            style=discord.TextStyle.long,
            required=False,
            default= self.job_data.get('details', 'N/A'),
            max_length=256,
        ))

        self.add_item(discord.ui.TextInput(
            label='When should this job expire? (In Hours)',
            style=discord.TextStyle.long,
            required=False,
            default= self.job_data.get('time_limit', '24'),
            max_length=3,
        ))
    
    async def on_submit(self, interaction: discord.Interaction):
        item = self.children[0].value
        quantity = self.children[1].value
        reward = self.children[2].value
        details = self.children[3].value
        time_limit = self.children[4].value

        if interaction.message:
            await interaction.message.delete()

        interaction_id = self.job_data.get("job_id", self.view.job_id)
        author_id = self.job_data.get("author_id", interaction.user.id)
        claimer_id = self.job_data.get("claimer_id", None)

        await create_or_edit_job(interaction, item, quantity, reward, details, time_limit, self.view, interaction_id, claimer_id)

        await add_job(interaction_id, interaction.user.id, item, quantity, reward, details, time_limit, claimer_id)
            
        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            print(f"Error: {error}")
            await interaction.response.send_message(f"Failed to update the job: {str(error)}", ephemeral=True)
            return


async def create_or_edit_job(interaction: discord.Interaction, item, quantity, reward, details, time_limit, view, job_id=None,  claimer_id=None):
    embed = embed_job(interaction.user, item, quantity, reward, details, time_limit, claimer_id)
    await interaction.response.send_message(embed=embed, view=view)


def embed_job(author,
    item,
    quantity,
    reward,
    details,
    time_limit,
    claimer=None):
    pixelshine = '<a:PIXELshine:1241404259774496878>'
    coin = '<:pixelcoin:1238636808951038092>'
    
    embed = discord.Embed(
    title=
    f"{coin}\t**New Task Posted!**\t{coin}\n",
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