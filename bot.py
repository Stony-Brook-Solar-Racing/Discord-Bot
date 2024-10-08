# Imports
from interactions import Activity, ActivityType, Client, Intents, SlashContext, Status, listen, slash_command
import json

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

# Load the extra, modularized, files.
bot.load_extension("SolarRacingAdmin")
bot.load_extension("NonAdmin")

# Start up the bot
bot.start(bot_token)
