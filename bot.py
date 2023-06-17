# The vital discord imports
import asyncio
import discord
from discord.ext import commands

# Misc. imports
import os
import json

from databaseManager import checkIfUserExist, initializeNewUserData

# Declaring intents & declaring prefix, and creating bot
prefix = '!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

with open('config.json') as file:
    config = json.load(file)

bot_token = config['bot_token']

async def main():
    await load()
    await bot.start(bot_token)

@bot.before_invoke
async def before_any_command(ctx):
    user_id = ctx.author.id
    exists = checkIfUserExist(user_id)
    if exists == False:
        await ctx.send(f"welcome to minecord {ctx.author.mention}. initializing new user data")
        initializeNewUserData(user_id)
        await ctx.send("initialization complete. happy mining!")

# Load all of our existing cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'cogs.{filename[:-3]}')
            await bot.load_extension(f'cogs.{filename[:-3]}')

# on_ready() event fires when the file is run, signaling Kody's alive
@bot.event
async def on_ready():
    print(f'(SUCCESS) {bot.user.name} IS NOW RUNNING...')

asyncio.run(main())