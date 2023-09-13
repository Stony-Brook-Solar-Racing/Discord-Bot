# Imports
from interactions import Activity, ActivityType, Client, Intents, SlashContext, Status, listen, slash_command
from interactions.ext.paginators import Paginator
import json

from embeds import getRulesEmbeds

# Bot
bot = Client(intents=Intents.DEFAULT)

# Fetch the bot token from the config.json
with open('config.json') as file:
    config = json.load(file)
bot_token = config['bot_token']

@listen()
async def on_startup():
    await bot.change_presence(status=Status.IDLE, activity=Activity(name="solar panels charge", type=ActivityType.WATCHING))
    print(f'(SUCCESS) {bot.app.name} IS NOW RUNNING...')

# Create an Embeds booklet which can be flipped through
rules_embeds = getRulesEmbeds()
rules_paginator = Paginator.create_from_embeds(bot, *rules_embeds)

@slash_command(name="rules", description="Clubs have rules to follow!")
async def rules(ctx: SlashContext):
    await rules_paginator.send(ctx)

# Load the extra, modularized, files.
bot.load_extension("SolarRacing")

# Start up the bot
bot.start(bot_token)