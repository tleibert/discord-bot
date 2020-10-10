import os

import discord

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD = os.getenv("GUILD_NAME")

client = discord.Client()


def help_message(message):
    return message.channel.send("Help Message")


async def clean(message):
    for channel in message.guild.channels:
        print(channel)


COMMANDS = {"help": help_message, "clean": clean}


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    for guild in client.guilds:
        print(f"Connected to {guild} (id: {guild.id})")


@client.event
async def on_message(message):
    text = message.content
    if text[0] == "~":
        print(f"Command recognized: {text[1:]}")
        try:
            command = COMMANDS[text[1:].split()[0]]
            await command(message)
        except KeyError:
            pass


client.run(TOKEN)
