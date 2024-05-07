from constants import ICON, ICON_END
import discord
import asyncio
import aiosqlite

async def leaderboard_func(table_name, order, page_number, server_id=None):
    async with aiosqlite.connect('leaderboard.db') as conn:
        c = await conn.cursor()

        # Determine order field
        order2 = order if table_name == 'total' else 'exp'

        # Construct the basic or guild-specific SQL query based on the presence of server_id
        if server_id:
            # Retrieve linked guild information based on server_id
            await c.execute(
                "SELECT linked_guild FROM discord_servers WHERE server_id = ?;",
                (server_id,)
            )
            guild_row = await c.fetchone()
            if guild_row:
                guild_name = guild_row[0]
                query = f"""
                SELECT u.username, u.{order}
                FROM {table_name} u
                JOIN guild_{guild_name} gm ON gm.user_id = u.user_id
                JOIN discord_servers ds
                WHERE ds.server_id = ?
                ORDER BY u.{order2} DESC
                LIMIT 10 OFFSET {10 * (page_number - 1)};
                """
                parameters = (server_id,)
        else:
            query = f"""
            SELECT username, {order}
            FROM {table_name}
            ORDER BY {order2} DESC
            LIMIT 10 OFFSET {10 * (page_number - 1)};
            """
            parameters = ()

        # Execute query
        await c.execute(query, parameters)

        # Create the embed for Discord
        title_prefix = f"{guild_name.title() + ' ' if server_id else ''}"
        embed = discord.Embed(title=f"{title_prefix}{table_name.title()} {order.title()} Leaderboard",
                              description="", color=0x00ff00)
        embed.set_footer(text=f"Page {page_number}")

        if table_name != 'total':
            embed.set_thumbnail(url=ICON + table_name.lower() + ICON_END)

        # Process query results and add to embed
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

async def manage_leaderboard(bot, ctx, table_name='total', arg='level', page_number='1', **kwargs):
    page = int(page_number)
    if arg in ['exp', 'level']:
        embed = await leaderboard_func(table_name, arg, max(1, page), **kwargs)
        message = await ctx.channel.send(embed=embed) 
        right = '➡️'
        flip = '🔄'
        left = '⬅️'
        await message.add_reaction(left)
        await message.add_reaction(flip)
        await message.add_reaction(right)

        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) in [left, flip, right] and reaction.message.id == message.id

        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break
            else:
                if str(reaction.emoji) == right:
                    page += 1
                elif str(reaction.emoji) == left:
                    page = max(1, page - 1)
                elif str(reaction.emoji) == flip:
                    arg = 'level' if arg == 'exp' else 'exp'

                embed = await leaderboard_func(table_name, arg, page, **kwargs)
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
