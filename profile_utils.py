import aiohttp
from constants import SKILLS, PROFILE_MID_LINK, SEARCH_PROFILE_LINK
from database import update_skills
import urllib.parse
import discord
  
async def lookup_profile(c, input):
  async with aiohttp.ClientSession() as session:
    # Asynchronous GET request
    async with session.get(PROFILE_MID_LINK + input) as response:
      if response.status != 200:
        print(f"Searched for name: {input}")
        data = await profile_finder(session, input)
      else:
        data = await response.json()  

    (total_levels, total_skills) = total_stats(data['levels'])

    #Update Skills in leaderboard:
    await update_skills(c, data, total_levels, total_skills)
      
    return data, total_levels, total_skills

def total_stats(levels):
  total_level = 0
  total_exp = 0
  for skill in SKILLS:
    lvl_data = levels.get(f'{skill}', None)
    if lvl_data:
      total_level += lvl_data['level']
      total_exp += lvl_data['totalExp']
  
  return total_level, total_exp
  

async def embed_profile(data, total_levels, total_skills):
  embed = discord.Embed(title=f"{data['username']}",
  description=f"User ID {data['_id']}",
  color=0x00ff00)

  embed.add_field(name=f"Account Level: {total_levels}",
  value=f"Total Exp: {'{:,}'.format(int(total_skills))}",
  inline=False)

  # info for each Skill
  for skill in SKILLS:
    skill_data = data['levels'].get(f'{skill}', None)
    if skill_data:
      embed.add_field(name=f"{skill.title()} - {skill_data['level']}",
      value=f"{'{:,}'.format(int(skill_data['totalExp']))}",
      inline=True)

  # Thumbnail image data
  image_url = data.get('currentAvatar', {}).get('pieces', {}).get('image', None)
  if image_url:
    embed.set_thumbnail(url=image_url)

  # Footer text
  embed.set_footer(text=f"Page 1/1 (work in progress)")

  #embed.set_author(name=data['username'],icon_url=data['currentAvatar']['pieces']['image'])

  return embed

#Finds profile info from string vs ID
async def profile_finder(session, input):
  encoded_input = urllib.parse.quote(input)
  async with session.get(SEARCH_PROFILE_LINK + encoded_input) as search_response:
    search_json = await search_response.json()
    for profile in search_json:
      if profile['username'] == input:
        return profile
    id = input if not search_json else search_json[0]['_id']
    async with session.get(PROFILE_MID_LINK + id) as profile_response:
      if profile_response.status != 200:
        return None, None, None
      return await profile_response.json()