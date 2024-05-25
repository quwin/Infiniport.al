from flask import Flask, request, redirect, url_for, render_template_string
from constants import REDIRECT_URI, COLLAB_ID, COLLAB_SECRET, COLLAB_KEY
from database import add_collab_tokens, add_collab_wallets
from profile_utils import profile_finder
from rate_limiter import AdaptiveRateLimiter
import aiohttp
import asyncio

app = Flask(__name__)

limiter = AdaptiveRateLimiter(3, 1)
collab_limiter = AdaptiveRateLimiter(9, 1)

async def get_access_token(auth_code):
    token_url = "https://api.collab.land/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": COLLAB_ID,
        "client_secret": COLLAB_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    async with collab_limiter, aiohttp.ClientSession() as session, session.post(token_url, data=data) as response:
            return await response.json()
        
# Request linked wallet(s) from Collab.land API
async def get_user_wallets(access_token, limit=None, pagination_token=None):
    wallets_url = "https://api.collab.land/account/wallets"
    params = {}
    if limit is not None:
        params['limit'] = limit
    if pagination_token is not None:
        params['paginationToken'] = pagination_token

    headers = {
        'x-api-key': COLLAB_KEY,
        'accept': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    async with collab_limiter, aiohttp.ClientSession() as session, session.get(wallets_url, headers=headers, params=params) as response:
        return await response.json()

# Async wrapper for looking for a given profile from their address from the Pixels.xyz API
async def look_for_profile(wallet_address):
    async with limiter, aiohttp.ClientSession() as session:
        return await profile_finder(session, wallet_address)

@app.route("/oauth2/callback")
def oauth2_callback():
    auth_code = request.args.get("code")
    user_id = request.args.get("state")
    if auth_code and user_id:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        access_token_data = loop.run_until_complete(get_access_token(auth_code))
        
        access_token = access_token_data.get("access_token")
        refresh_token = access_token_data.get("refresh_token")
        loop.run_until_complete(add_collab_tokens(user_id, access_token, refresh_token))
        
        user_wallets_data = loop.run_until_complete(get_user_wallets(access_token))
        addresses = []
        player_ids = []
        
        for wallet in user_wallets_data.get("items"):
            type = wallet.get("walletType")
            if type == 'evm' or type == 'metamask' or type == 'ronin':
                address = wallet.get("address")
                account_data = loop.run_until_complete(look_for_profile(address))
                if address and account_data:
                    addresses.append(address)
                    player_ids.append(account_data.get("_id"))
                    
        formatted_addresses = " ".join(addresses)
        formatted_player_ids = " ".join(player_ids)
        print(f"User {user_id} has {formatted_addresses} linked to {formatted_player_ids}")
        
        if addresses and player_ids:
            loop.run_until_complete(add_collab_wallets(
                user_id, 
                formatted_addresses,
                formatted_player_ids
                )
            )
            
            
        print(f"User ID: \n{user_id}, \n User Wallets: \n{user_wallets_data}")
        return redirect(url_for('success'))
    else:
        return redirect(url_for('error'))

@app.route("/success")
def success():
    return render_template_string("""
        <html>
        <body>
            <h1>Authorization successful!</h1>
            <p>This tab will close automatically.</p>
            <script type="text/javascript">
                window.onload = function() {
                    window.open('', '_self', ''); 
                    window.close(); 
                    setTimeout(function() { 
                        alert("Please close this tab."); 
                    }, 1000);
                }
            </script>
        </body>
        </html>
    """)

@app.route("/error")
def error():
    return "<h1>Error: Authorization code not found.</h1>"

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask()