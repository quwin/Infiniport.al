from constants import ICON, ICON_END, GUILD_EMBLEM
import aiosqlite
import discord

async def leaderboard(table_name, order, page_number):
    # Open a connection to SQLite database
    async with aiosqlite.connect('leaderboard.db') as conn:
        c = await conn.cursor()

        # Create the embed for Discord
        embed = discord.Embed(title=f"{table_name.title()} {order.title()} Leaderboard",
                              description="",
                              color=0x00ff00)
        embed.set_footer(text=f"Page {page_number}")

        if table_name != 'total':
            embed.set_thumbnail(url=ICON + table_name.lower() + ICON_END)

        order2 = order if table_name == 'total' else 'exp'

        # SQL query
        query = f"""
        SELECT username, {order}
        FROM {table_name}
        ORDER BY {order2} DESC
        LIMIT 10 OFFSET {10 * (page_number - 1)};
        """
        # Execute the query and add results to the embed
        cursor = await c.execute(query)
        medals = ["🥇 ", "🥈 ", "🥉 "]
        row_index = 0
        async for row in cursor:
            formatted_entry = f"{row[0]} - {'{:,}'.format(int(row[1]))}"

            if page_number == 1 and row_index < len(medals):
                formatted_entry = medals[row_index] + formatted_entry
            else:
                number = f"#{(page_number-1)*10 + row_index + 1} "
                formatted_entry = number + formatted_entry

            embed.add_field(name=formatted_entry, value="", inline=False)

            row_index += 1

    return embed

async def guild_leaderboard(server_id, table_name, order, page_number):
    async with aiosqlite.connect('leaderboard.db') as conn:
        c = await conn.cursor()
        query = """ 
        SELECT linked_guild
        FROM discord_servers
        WHERE server_id = ?;
        """

        order2 = order if table_name == 'total' else 'exp'

        await c.execute(query, (server_id,))
        async for row in c:
            query = f"""
            SELECT u.username, u.{order}
            FROM {table_name} u
            JOIN guild_{row[0]} gm ON gm.user_id = u.user_id
            JOIN discord_servers ds
            WHERE ds.server_id = ?
            ORDER BY u.{order2} DESC
            LIMIT 10 OFFSET {10 * (page_number - 1)};
            """
            embed = discord.Embed(title=f"{row[0].title()} {table_name.title()} {order.title()} Leaderboard",
                                  description="", color=0x00ff00)
            embed.set_footer(text=f"Page {page_number}")
            
            if table_name != 'total':
                embed.set_thumbnail(url=ICON + table_name.lower() + ICON_END)

            # Thumbnail image data
            image_url = GUILD_EMBLEM + row[0] + '.png'
            if image_url:
                embed.set_thumbnail(url=image_url)
                
            await c.execute(query, (server_id,))
            medals = ["🥇 ", "🥈 ", "🥉 "]
            row_index = 0
            async for row in c:
                formatted_entry = f"{row[0]} - {'{:,}'.format(int(row[1]))}"

                if page_number == 1 and row_index < len(medals):
                    formatted_entry = medals[row_index] + formatted_entry
                else:
                    number = f"#{(page_number-1)*10 + row_index + 1} "
                    formatted_entry = number + formatted_entry

                embed.add_field(name=formatted_entry, value="", inline=False)

                row_index += 1
    return embed