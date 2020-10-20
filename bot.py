# -*- coding: utf-8 -*-
"""
Simple discord bot to practice async/await.

TODO test C by GE library
TODO add color command
TODO think of more commands?
"""
import os
import time

from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD = os.getenv("GUILD_NAME")

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Connected to {guild} (id: {guild.id})")


@bot.command(
    name="clean",
    help="Removes all bot commands and bot-sent messages from the channel.",
)
async def clean(ctx):
    """
    Cleans the recent messages in the channel.
    Deletes all messages sent by the bot, and any commands
    that were given to the bot.
    """
    msg = await ctx.send("Cleaning...")
    total_deleted = 0
    async for message in ctx.channel.history(limit=200, before=msg.created_at):
        try:
            if message.author == bot.user:
                await message.delete()
                total_deleted += 1
            elif (
                message.content[0] == bot.command_prefix
                and message.content.split()[0][1:] in bot.all_commands
            ):
                await message.delete()
                total_deleted += 1
        except IndexError:
            pass

    else:
        await msg.edit(content=f"Cleaned `{total_deleted}` messages.")
        time.sleep(1)
        await msg.delete()


bot.run(TOKEN)
