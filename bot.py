# The vital discord imports
from interactions import Activity, ActivityType, Client, Intents, Status, listen

# Misc. imports
import json

# Bot
bot = Client(intents=Intents.DEFAULT)

with open('config.json') as file:
    config = json.load(file)
bot_token = config['bot_token']

@listen()
async def on_startup():
    await bot.change_presence(status=Status.IDLE, activity=Activity(name="Minecraft? 😳", type=ActivityType.PLAYING))
    print(f'(SUCCESS) {bot.app.name} IS NOW RUNNING...')

bot.load_extension("enchanting")
bot.load_extension("crafting")
bot.load_extension("minecord")
bot.load_extension("resources")

bot.start(bot_token)