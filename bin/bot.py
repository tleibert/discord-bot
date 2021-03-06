"""
Simple discord bot to practice async/await.
"""
import asyncio
import json
import os
from random import choice, randint

from asyncpraw import Reddit
from discord.ext import commands
import yaml


GUILD = os.getenv("GUILD_NAME")

with open("resources/colors.json") as colorfile:
    COLOR_DICT = {name: int(code, 16) for name, code in json.load(colorfile).items()}

with open("resources/links.yml") as links:
    LINKS = yaml.safe_load(links)

with open("resources/copypastas.yml") as pastas:
    PASTAS = yaml.safe_load(pastas)

bot = commands.Bot(command_prefix="$")

reddit = Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="test user agent",
)


@bot.event
async def on_ready():
    """
    Runs once the bot is connected to Discord.
    """
    print(f"{bot.user.name} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Connected to {guild} (id: {guild.id})")


@bot.event
async def on_message(message):
    """
    Runs every time a message is received
    """
    if message.author != bot.user and "based" in message.content.lower():
        msg = await message.channel.send(PASTAS["based"])
        await asyncio.sleep(7)
        await msg.delete()

    await bot.process_commands(message)


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
    to_delete = [
        message
        async for message in ctx.channel.history(limit=50, before=msg.created_at)
        if message.author == bot.user
        or len(message.content) > 1
        and message.content[0] == bot.command_prefix
        and message.content.split()[0][1:] in bot.all_commands
    ]

    await ctx.channel.delete_messages(to_delete)
    await msg.edit(
        content=f"Cleaned `{len(to_delete) - 1}` messages. :put_litter_in_its_place:"
    )
    await asyncio.sleep(1)
    await msg.delete()


@bot.command(
    name="rtd",
    help="Rolls a *n* sided dice, where n is an integer > 0 given as an argument.\n"
    "Default value is 6.",
)
async def roll_the_dice(ctx, arg=6):
    """
    Rolls an n-sided dice and reports the result.
    """
    try:
        num = int(arg)
        if num <= 0:
            await ctx.send("Must be a number > 0!")
            return

        await ctx.send(f"You rolled a `{randint(1, num)}`")
    except ValueError:
        await ctx.send("Not a number!")


@bot.command(
    name="setcolor",
    help="Sets the color of my owner's desk lamp.\n"
    "Color argument can be given in hex, or as one of the 140 named HTML colors.",
)
async def set_color(ctx, arg=None):
    """
    Sets the color of the smart light.
    Parses a color either as a named html color or
    as a hex string.
    """
    if arg is None:
        await ctx.send("No color provided!")
        return

    up_arg = arg.upper()
    hex_color = 0

    if up_arg in COLOR_DICT:
        hex_color = COLOR_DICT[up_arg]
    else:
        try:
            color_str = arg
            if color_str[0] == "#":
                color_str = color_str[1:]

            if len(color_str) != 6:
                raise ValueError

            hex_color = int(color_str, 16)
            if hex_color < 0:
                raise ValueError
        except ValueError:
            await ctx.send("Please input a valid HTML color name or hex color!")
            return

    # TODO do stuff with color
    await ctx.send(f"Changing light to `#{hex_color:06x}`")
    print(f"Changing light to {hex_color:06x}")


@bot.command(
    name="listcolors", help="Lists out the possible named colors to choose from."
)
async def list_colors(ctx):
    """
    Lists the recognized color names.
    """
    message_body = ", ".join(COLOR_DICT).lower()
    await ctx.send(f"Named colors:\n```\n{message_body}\n```")


@bot.command(name="colorlist")
async def color_list(ctx):
    """
    Alternative name for `list_colors`.
    """
    await list_colors(ctx)


@bot.command(name="jerma")
async def jerma_post(ctx):
    """ Posts jerma stuff duh """
    await ctx.send(choice(list(LINKS["jerma"].values())))


@bot.command(name="reload")
async def reload():
    """
    Reloads the bot's configuration files
    """

    with open("resources/colors.json") as colorfile:
        COLOR_DICT.update(
            {name: int(code, 16) for name, code in json.load(colorfile).items()}
        )

    with open("resources/links.yml") as links:
        LINKS.update(yaml.load(links, yaml.SafeLoader))


async def scrape_reddit_linkpost(subreddit):
    """
    Grabs a random linkpost off of the given subreddit
    """

    sub = await reddit.subreddit(subreddit)
    post = await sub.random()
    # retry until we get a link post
    while post.selftext != "":
        post = await sub.random()
    return post.url


@bot.command(name="jarma")
async def jerma_reddit(ctx):
    """
    Grabs a random post from the jerma985 subreddit and posts it to discord.
    """
    await ctx.send(await scrape_reddit_linkpost("jerma985"))


@bot.command(name="tf2")
async def okay_buddy_fortress(ctx):
    """
    Grabs a random post from the okaybuddyfortress subreddit and posts it to discord.
    """
    await ctx.send(
        await scrape_reddit_linkpost(choice(("okaybuddyfortress", "tf2shitposterclub")))
    )


@bot.command(name="brit")
async def ok_mate(ctx):
    """
    Grabs a random post from the okmatewanker subreddit and posts it to discord.
    """
    await ctx.send(await scrape_reddit_linkpost("okmatewanker"))


bot.run(os.getenv("DISCORD_BOT_TOKEN"))
