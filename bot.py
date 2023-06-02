# The vital discord imports
import asyncio
import discord
from discord.ext import commands

# Misc. imports
import os
import json

# Declaring intents & declaring prefix, and creating bot
prefix = '!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

with open('config.json') as file:
    config = json.load(file)

bot_token = config['bot_token']

# Load all of our existing cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(bot_token)

# on_ready() event fires when the file is run, signaling Kody's alive
@bot.event
async def on_ready():
    print(f'{bot.user.name} is starting...')

asyncio.run(main())