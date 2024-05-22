import aiosqlite
import discord
import aiohttp
from database import fetch_linked_wallets
from constants import COLLAB_KEY, COLLAB_SECRET, COLLAB_ID, REDIRECT_URI


class CollabButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.start_button = discord.ui.Button(label="Let's Go!", 
                                              style=discord.ButtonStyle.blurple,
                                              custom_id="link_collab_start")
        self.why_button = discord.ui.Button(label="Why Collab.Land?",
                                            style=discord.ButtonStyle.grey,
                                            custom_id="why_collab_land")
        self.docs_button = discord.ui.Button(label="Collab.Land Docs",
                                                  style=discord.ButtonStyle.grey,
                                                  url="https://docs.collab.land/")

        self.start_button.callback = self.start_button_callback
        self.why_button.callback = self.why_button_callback

        self.add_item(self.start_button)
        self.add_item(self.why_button)
        self.add_item(self.docs_button)

    async def start_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await link_account(interaction)
    
    async def why_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Collab.Land is used for...", ephemeral=True)
        
    
# Request linked wallet(s) from Collab.land API
async def request_linked_wallets(session, access_token, limit=None, pagination_token=None):
    url = "https://api.collab.land/user/wallets"

    params = {}
    if limit is not None:
        params['limit'] = limit
    if pagination_token is not None:
        params['paginationToken'] = pagination_token

    headers = {
        'x-api-key': COLLAB_KEY,
        'accept': 'application/json',
        'Authorization': f"AE <{access_token}>"
    }
    
    async with session.get(url, headers=headers, params=params) as response:
        print(f'{response.status}')
        if response.status == 200:
            print(f'{await response.json()}')
            return await response.json()
        else:
            return None


async def manage_collab_link(interaction, session):
    existing_wallets = await fetch_linked_wallets(interaction.user.id)
    if existing_wallets:
        embed = show_linked_accounts(existing_wallets)
        await interaction.followup.send(embed=embed, ephermial=True)
    else:
        access_token = ''
        find_wallet_data = await request_linked_wallets(session, access_token)
        if linked_wallet_data is None:
          return
        confirmed_accounts = []
        for wallet in linked_wallet_data.get('items'):
          wallet_address = wallet.get('address')


def collab_embed():
    embed = discord.Embed(
          title="Link your Pixels.xyz account",
          color=0x00ff00)
    embed.set_author(name="Cookie Monster")
    embed.add_field(name="",
                  value="This is a read-only connection. Do not share your private keys. " +
                  "We will never ask for your seed phrase. We will never DM you.\n" + 
                  "This verification process is done through <@704521096837464076>",
                  inline=False)
    return embed
    

async def collab_channel(client):
    channel_id = 1234015430381932577
    channel = client.get_channel(channel_id)

    if channel:
        await channel.send(embed=collab_embed(), view=CollabButtons())

async def link_account(interaction):
    auth_url = (
        f"https://api.collab.land/oauth2/authorize"
        "?response_type=code"
        f"&client_id={COLLAB_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user:wallet:read"
        f"&state={interaction.user.id}"
    )
    await interaction.followup.send(
        f"Please link your account by visiting this URL: {auth_url}",
        ephemeral=True
    )

async def show_linked_accounts(existing_wallets):
    embed = discord.Embed(
          title="My Connected Pixels.xyz Accounts",
          description="Data powered by <@704521096837464076>\n",
          color=0x00ff00)
    accounts = ''
    for wallet in existing_wallets:
        accounts = accounts + f"{wallet[0]} - {'{:,}'.format(int(wallet[1]))} \n"
        
    embed.add_field(name="", value=accounts, inline=False)
    return embed