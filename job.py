import asyncio
import discord
import time
from constants import SKILLS

async def embed_job(author, item, quantity, reward, details, time_limit):
  embed = discord.Embed(title="⛏ **New Job Posted!** ⛏\n", color=0x00ff00)

  embed.set_author(name=f"Requested by {author.display_name}", icon_url=f"{author.display_avatar}")

  embed.add_field(name="",
  value=f"**{quantity}** x {item}\n\n" + 
        "**Additional Info:\n**" +
        f"{details}\n\n" +
        "**Reward:**\n" +
        f"{reward} Coins <:pixelcoin:1238636808951038092>\n",
  inline=False)

  embed.add_field(name="Expiration Time:",
  value=f"<t:{int(time.time()+time_limit)}:R>",
  inline=False)

  return embed

async def manage_job(bot, ctx, item, quantity, reward, details, time_limit):
  claimed = False
  claimer = ""
  await ctx.message.delete()
  author = ctx.message.author
  embed = await embed_job(author, item, quantity, reward, details, time_limit)
  message = await ctx.channel.send(embed=embed) 
  cookie = '🍪'
  await message.add_reaction(cookie)
  def check(reaction, user):
    return user != bot.user and str(reaction.emoji) in [cookie] and reaction.message.id == message.id

  while True:
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=time_limit, check=check)
    except asyncio.TimeoutError:
        await message.delete()
        if claimed:
          await ctx.channel.send(f"<@{claimer}>, your claimed order has expired! \nContact <@{author.id}> if you have not yet fulfilled your order.")
        break
    else:
        if str(reaction.emoji) == cookie and claimed == False:
          embed.add_field(name="", value=f"Claimed by <@{user.id}>", inline=False)
          claimed = True
          claimer = user.id
          await message.edit(embed=embed)
          await message.clear_reactions()
          await ctx.channel.send(f"<@{author.id}>, your order of {quantity}x {item} has been accepted by <@{user.id}>!")
          
        await message.remove_reaction(reaction, user)