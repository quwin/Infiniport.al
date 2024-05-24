# webserver.py
from flask import Flask, request, redirect, url_for
import aiohttp
import asyncio
from constants import REDIRECT_URI, COLLAB_ID, COLLAB_SECRET, COLLAB_KEY

app = Flask(__name__)

queue = asyncio.Queue()

async def get_access_token(auth_code):
    token_url = "https://api.collab.land/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": COLLAB_ID,
        "client_secret": COLLAB_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    async with aiohttp.ClientSession() as session, session.post(token_url, data=data) as response:
            return await response.json()

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
        'Authorization': f"AE {access_token}"
    }

    async with aiohttp.ClientSession() as session, session.get(wallets_url, headers=headers, params=params) as response:
        return await response.json()

@app.route("/oauth2/callback")
def oauth2_callback():
    auth_code = request.args.get("code")
    state = request.args.get("state")
    if auth_code and state:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        access_token_data = loop.run_until_complete(get_access_token(auth_code))
        print(access_token_data)
        access_token = access_token_data.get("access_token")
        print(access_token)
        user_wallets = loop.run_until_complete(get_user_wallets(access_token))
        print(user_wallets)
        user_id = int(state)
        asyncio.run_coroutine_threadsafe(queue.put((user_id, user_wallets)), loop)

        return redirect(url_for('success'))
    else:
        return redirect(url_for('error'))

@app.route("/success")
def success():
    return "<h1>Authorization successful! You can close this window.</h1>"

@app.route("/error")
def error():
    return "<h1>Error: Authorization code not found.</h1>"

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)