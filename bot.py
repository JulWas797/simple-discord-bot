import random
from datetime import datetime, timezone

import requests
import discord
from discord import app_commands

client = discord.Client(intents=discord.Intents.all())
commands = app_commands.CommandTree(client)


@commands.command(name="clock", description="Get current UTC time")
async def clock_command(ctx):
    time = datetime.now(tz=timezone.utc).strftime('%H:%M')
    await ctx.response.send_message(f"Hello, World! It's {time}!", ephemeral=True)


@commands.command(name="dice", description="Rolls the dice")
async def dice_command(ctx):
    result = random.randrange(1, 7)
    await ctx.response.send_message(f":game_die: You rolled **{result}**")


@commands.command(name="joke", description="Returns random joke")
async def joke_command(ctx):
    response = "Couldn't fetch the joke"
    ephemeral = True
    try:
        joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        response = f"Here is a random joke for you:\n> {joke['setup']}\n> **{joke['punchline']}** :joy:"
        ephemeral = False
    finally:
        await ctx.response.send_message(response, ephemeral=ephemeral)


# NOTE: commands.sync() should be executed at every startup as it can cause ratelimiting.
# This is for demonstration purposes!
@client.event
async def on_ready():
    await commands.sync()
    print("Bot started successfully!")


client.run(token="TOKEN")
