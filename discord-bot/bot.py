import json

from interactions import (
    Activity,
    ActivityType,
    Client,
    Intents,
    Status,
    listen,
)
from interactions import ContextMenuContext, Message, message_context_menu

# Bot
bot = Client(intents=Intents.DEFAULT)

# Fetch the bot token from the config.json
with open("config.json") as file:
    config = json.load(file)
bot_token = config["bot_token"]


@listen()
async def on_startup():
    await bot.change_presence(
        status=Status.ONLINE,
        activity=Activity(name="solar panels charge", type=ActivityType.WATCHING),
    )
    print(f"(SUCCESS) {bot.app.name} IS NOW RUNNING...")


# Load separate Python files
bot.load_extension("admin_commands")
bot.load_extension("normal_commands")

@message_context_menu(name="Add todo")
async def add_todo(ctx: ContextMenuContext):
    admin_roles = config["admin_roles"]
    if not any(ctx.guild.get_role(role_id) in ctx.author.roles for role_id in admin_roles):
        await ctx.send("You do not have permission to use this command.", ephemeral=True)
        return

    # placeholder
    message: Message = ctx.target
    await ctx.send(message.content)

# Start up the bot
bot.start(bot_token)
