import asyncio
import discord
import time
from constants import SKILLS


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


async def manage_job(interaction: discord.Interaction, item, quantity, reward,
                     details, time_limit):
  claimer = None
  author = interaction.user
  embed = await embed_job(author, item, quantity, reward, details, time_limit,
                          claimer)

  # Adding Buttons to Job Embed
  view = discord.ui.View()
  claim_button = discord.ui.Button(label="Claim",
                                   style=discord.ButtonStyle.green,
                                   custom_id=f"claim_{interaction.id}")
  unclaim_button = discord.ui.Button(label="Unclaim",
                                     style=discord.ButtonStyle.red,
                                     custom_id=f"unclaim_{interaction.id}")
  close_job_button = discord.ui.Button(label="Close Job",
                                       style=discord.ButtonStyle.blurple,
                                       custom_id=f"close_job_{interaction.id}")
  view.add_item(claim_button)
  view.add_item(unclaim_button)
  view.add_item(close_job_button)

  # Initial message response
  await interaction.response.send_message(embed=embed,
                                          view=view,
                                          ephemeral=False)

  #Ensures bot isnt triggering itself and it's the correct interact type
  def button_check(inter):
    return (inter.user != interaction.client.user
    and inter.type == discord.InteractionType.component)

  while True:
    try:
      button_interaction = await interaction.client.wait_for(
          'interaction',
          timeout=float(time_limit) * 3600.0,
          check=button_check)
      # if they click "Claim" button
      if (button_interaction.data and button_interaction.data.get('custom_id')
          == f"claim_{interaction.id}"):
        # if it's already claimed
        if not claimer:
          claimer = button_interaction.user.id
          await interaction.followup.send(
              f"<@{author.id}>, your order of {quantity}x {item}! has been claimed by <@{button_interaction.user.id}>!", ephemeral=True)
        # update embed
        embed = await embed_job(author, item, quantity, reward, details,
                                time_limit, claimer)
        await button_interaction.response.edit_message(embed=embed, view=view)
      # if they click "Unclaim" button
      elif (button_interaction.data
            and button_interaction.data.get('custom_id')
            == f"unclaim_{interaction.id}"):
        if button_interaction.user.id == claimer:
          claimer = None
        # update embed
        embed = await embed_job(author, item, quantity, reward, details,
                                time_limit, claimer)
        await button_interaction.response.edit_message(embed=embed, view=view)
      # if they click "Close Job" button
      elif (button_interaction.data
            and button_interaction.data.get('custom_id')
            == f"close_job_{interaction.id}"):
        if (button_interaction.user.id == author.id):
          await button_interaction.message.delete()
          break
        elif (button_interaction.user.id == claimer):
          await interaction.followup.send(
              f"<@{author.id}>, <@{button_interaction.user.id}> has closed your job!",
              ephemeral=False)
          await button_interaction.message.delete()
          break
    except asyncio.TimeoutError:
      await interaction.delete_original_response()
      break
