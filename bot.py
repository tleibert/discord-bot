import os
import time

from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD = os.getenv("GUILD_NAME")

bot = commands.Bot(command_prefix="~")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Connected to {guild} (id: {guild.id})")


@bot.command(
    name="clean",
    help="Removes all bot commands and bot-sent messages from the channel.",
)
async def help_message(ctx):
    msg = await ctx.send("Cleaning...")
    print(type(msg))
    total_deleted = 0
    async for message in ctx.channel.history(limit=200, before=msg.created_at):
        try:
            if message.author == bot.user:
                await message.delete()
                total_deleted += 1
            elif message.content[1:].split()[0] in bot.all_commands:
                await message.delete()
                total_deleted += 1
        except IndexError:
            pass

    else:
        await msg.edit(content=f"Cleaned `{total_deleted}` messages.")
        time.sleep(1)
        await msg.delete()


bot.run(TOKEN)
