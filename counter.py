async def update_voice_channel_name():
  guild = bot.get_guild(guild_id)
  if guild:
    channel = guild.get_channel(channel_id)
    if channel and isinstance(channel, discord.VoiceChannel):
      new_name = f"Count: {random.randint(1, 100)}"  # Random number for example
      await channel.edit(name=new_name)
      print(f"Updated channel name to {new_name}")

  return new_name