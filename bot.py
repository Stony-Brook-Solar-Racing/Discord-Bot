# The vital discord imports
from interactions import Activity, ActivityType, Client, Intents, SlashContext, Status, listen, slash_command
from interactions.ext.paginators import Paginator

# Misc. imports
import json

from embeds import getTutorialEmbeds, getUpdateEmbeds, getRecipeEmbeds

# Bot
bot = Client(intents=Intents.DEFAULT)

with open('config.json') as file:
    config = json.load(file)
bot_token = config['bot_token']

@listen()
async def on_startup():
    await bot.change_presence(status=Status.IDLE, activity=Activity(name="Minecraft? 😳", type=ActivityType.PLAYING))
    print(f'(SUCCESS) {bot.app.name} IS NOW RUNNING...')

tutorial_embeds = getTutorialEmbeds()
tutorial_paginator = Paginator.create_from_embeds(bot, *tutorial_embeds)

update_embeds = getUpdateEmbeds()
update_paginator = Paginator.create_from_embeds(bot, *update_embeds)

recipe_embed = getRecipeEmbeds()
recipe_paginator = Paginator.create_from_embeds(bot, *recipe_embed)

@slash_command(name="tutorial", description="learn how to use the bot")
async def tutorial(ctx: SlashContext):
    await tutorial_paginator.send(ctx)

@slash_command(name="updates", description="view the changelog")
async def updates(ctx: SlashContext):
    await update_paginator.send(ctx)

@slash_command(name="recipes", description="view the bots recipes")
async def recipes(ctx: SlashContext):
    await recipe_paginator.send(ctx)

bot.load_extension("enchanting")
bot.load_extension("crafting")
bot.load_extension("minecord")
bot.load_extension("resources")
bot.load_extension("miscellaneous")

bot.start(bot_token)