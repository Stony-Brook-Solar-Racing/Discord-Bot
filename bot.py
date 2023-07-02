# The vital discord imports
import interactions
from interactions import Activity, ActivityType, Client, Intents, Status, listen

# Misc. imports
import json

# Custom imports
from databaseManager import checkIfUserExist, initializeNewUserData

# Bot
bot = Client(intents=Intents.DEFAULT)

with open('config.json') as file:
    config = json.load(file)
bot_token = config['bot_token']

@listen()
async def on_message_create(ctx):
    print("ran")
    user_id = ctx.author.id
    exists = checkIfUserExist(user_id)
    if exists == False:
        await ctx.send(f"welcome to minecord {ctx.author.mention}. initializing new user data")
        initializeNewUserData(user_id)
        await ctx.send("initialization complete. happy mining!")

@listen()
async def on_startup():
    await bot.change_presence(status=Status.IDLE, activity=Activity(name="Minecraft? 😳", type=ActivityType.PLAYING))
    print(f'(SUCCESS) {bot.app.name} IS NOW RUNNING...')

bot.load_extension("enchanting")
bot.load_extension("crafting")
bot.load_extension("minecord")
bot.load_extension("resources")

bot.start(bot_token)
