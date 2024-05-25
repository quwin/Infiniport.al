import discord
from database import fetch_linked_wallets
from constants import COLLAB_ID, REDIRECT_URI

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
        await manage_collab_link(interaction)
    
    async def why_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Collab.Land is a robust, easy to connect, and easy to integrate service which allows servers to link Discord accounts to Crypto Wallets. \n \n" +
            "This application uses your crypto wallets you have linked to your Pixels account in order to verify that you have ownership of the given Pixels account.\n \n" +
            "Collab.Land is used by many Pixels Guilds discords to verify shard ownership, and is even used by the Official Pixels discord itself. \n \n" + 
            "When linking your crypto wallet with Collab.Land and Cookie Monster, I will not have access to any personal or sensitive data. I will not ask for users to send any transactions, or ask for a seed phrase. \n \n Thanks.",
            ephemeral=True)


async def manage_collab_link(interaction):
    user_id = str(interaction.user.id)
    existing_wallets = await fetch_linked_wallets(user_id)
    print(existing_wallets)
    (embed, view) = show_linked_accounts(existing_wallets, user_id)
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

# Embed for showing how to link your Pixels Account to the Bot
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

#Function to create and manage collab_embed()
async def collab_channel(client):
    channel_id = 1234015430381932577
    channel = client.get_channel(channel_id)

    if channel:
        await channel.send(embed=collab_embed(), view=CollabButtons())

# Function to show the linked accounts, and allow people to link their accounts
def show_linked_accounts(existing_wallets, user_id):
    if existing_wallets:
        embed = discord.Embed(
              title="My Connected Pixels.xyz Accounts",
              description="Data powered by Collab.Land\n",
              color=0x00ff00)
        accounts = ''
        for wallet in existing_wallets:
            accounts = accounts + f"{wallet[0]} - {'{:,}'.format(int(wallet[1]))} \n"
            
        embed.add_field(name="", value=accounts, inline=False)
    else:
        embed = discord.Embed(
              title="My Connected Pixels.xyz Accounts",
              description="Data powered by <@704521096837464076>\n",
              color=0x00ff00)
        accounts = 'You have no accounts linked! Please link one by clicking the button below.'
        embed.add_field(name="", value=accounts, inline=False)

    view = discord.ui.View()
    auth_url = (
        f"https://api.collab.land/oauth2/authorize"
        "?response_type=code"
        f"&client_id={COLLAB_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user:wallet:read"
        f"&state={user_id}"
    )
    cont_button = discord.ui.Button(
        label="Use Connected Accounts",
        style=discord.ButtonStyle.blurple,
        
    )
    link_button = discord.ui.Button(
        label="Add a new Account",
        style=discord.ButtonStyle.grey,
        url=auth_url
    )

    view.add_item(item=cont_button)
    view.add_item(item=link_button)

    return embed, view