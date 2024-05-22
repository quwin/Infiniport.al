# webserver.py
from flask import Flask, request, jsonify, redirect, url_for
import aiohttp
import asyncio
from constants import REDIRECT_URI

app = Flask(__name__)

# Your client ID, client secret, and redirect URI
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

queue = asyncio.Queue()

async def get_access_token(auth_code):
    token_url = "https://api.collab.land/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, data=data) as response:
            return await response.json()

async def get_user_wallets(access_token):
    wallets_url = "https://api.collab.land/user/wallets"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(wallets_url, headers=headers) as response:
            return await response.json()

@app.route("/oauth2/callback")
def oauth2_callback():
    auth_code = request.args.get("code")
    state = request.args.get("state")
    if auth_code and state:
        loop = asyncio.get_event_loop()
        access_token_data = loop.run_until_complete(get_access_token(auth_code))
        access_token = access_token_data.get("access_token")
        user_wallets = loop.run_until_complete(get_user_wallets(access_token))

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
