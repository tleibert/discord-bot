import os

import discord

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    for guild in client.guilds:
        print(f"Connected to {guild} (id: {guild.id})")

client.run(TOKEN)
