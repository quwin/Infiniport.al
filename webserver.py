from flask import Flask, request, redirect, url_for, render_template_string, jsonify, send_from_directory
from constants import REDIRECT_URI, COLLAB_ID, COLLAB_SECRET, COLLAB_KEY
from database import add_collab_tokens, add_collab_wallets
from profile_utils import profile_finder
from constants import SKILLS
import aiohttp
import asyncio
import sqlite3

app = Flask(__name__)

DATABASE = 'leaderboard.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/leaderboard/<table_name>/<order>/<page_number>/',
           defaults={'server_id': None},
           methods=['GET'])
@app.route('/leaderboard/<table_name>/<order>/<page_number>/<server_id>',
           methods=['GET'])
def get_leaderboard(table_name, order, page_number, server_id):
    valid_orders = ['level', 'exp']
    valid_tables = SKILLS.copy()
    valid_tables.append('total')

    if order not in valid_orders or table_name not in valid_tables:
        return jsonify({'error': 'Invalid table name or order'}), 400

    offset = 10 * (int(page_number) - 1)

    try:
        db = get_db()
        if server_id:
            cursor = db.execute(
                f'''
                SELECT u.username, u.{order}
                FROM {table_name} u
                JOIN guild_{server_id} gm ON gm.user_id = u.user_id
                ORDER BY u.{order} DESC
                LIMIT 10 OFFSET ?''', (offset, ))
        else:
            cursor = db.execute(
                f'''
                SELECT username, {order}
                FROM {table_name}
                ORDER BY {order} DESC
                LIMIT 10 OFFSET ?''', (offset, ))

        rows = cursor.fetchall()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


async def get_access_token(auth_code):
    token_url = "https://api.collab.land/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": COLLAB_ID,
        "client_secret": COLLAB_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    async with aiohttp.ClientSession() as session, session.post(
            token_url, data=data) as response:
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

    async with aiohttp.ClientSession() as session, session.get(
            wallets_url, headers=headers, params=params) as response:
        return await response.json()


# Async wrapper for looking for a given profile from their address from the Pixels.xyz API
async def look_for_profile(wallet_address):
    async with aiohttp.ClientSession() as session:
        return await profile_finder(session, wallet_address)


@app.route("/oauth2/callback")
def oauth2_callback():
    auth_code = request.args.get("code")
    user_id = request.args.get("state")
    if auth_code and user_id:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        access_token_data = loop.run_until_complete(
            get_access_token(auth_code))

        access_token = access_token_data.get("access_token")
        refresh_token = access_token_data.get("refresh_token")
        loop.run_until_complete(
            add_collab_tokens(user_id, access_token, refresh_token))

        user_wallets_data = loop.run_until_complete(
            get_user_wallets(access_token))
        addresses = []
        player_ids = []

        for wallet in user_wallets_data.get("items", []):
            type = wallet.get("walletType")
            if type == 'evm' or type == 'metamask' or type == 'ronin':
                address = wallet.get("address")
                account_data = loop.run_until_complete(
                    look_for_profile(address))
                if address and account_data:
                    addresses.append(address)
                    player_ids.append(account_data.get("_id"))

        if addresses and player_ids:
            formatted_addresses = " ".join(addresses)
            formatted_player_ids = " ".join(player_ids)
            loop.run_until_complete(
                add_collab_wallets(user_id, formatted_addresses,
                                   formatted_player_ids))

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
            <script type="text/javascript">
                window.onload = function() {
                    window.open('', '_self', ''); 
                    window.close(); 
                    setTimeout(function() { 
                        alert("Please return to Discord and refresh your accounts"); 
                    }, 1000);
                }
            </script>
        </body>
        </html>
    """)


@app.route("/error")
def error():
    return "<h1>Error: Authorization code not found.</h1>"


@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
