import json
import re

from interactions import (
    Activity,
    ActivityType,
    Client,
    Intents,
    Status,
    listen,
)
from interactions import ContextMenuContext, message_context_menu
from markdown_to_data import Markdown

from solardb import solardb

# Bot
bot = Client(
    intents=Intents.DEFAULT,
    sync_interactions=True,
    delete_unused_application_cmds=True,
)

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

@message_context_menu(name="Add tasks")
async def add_tasks(ctx: ContextMenuContext):
    admin_roles = config["admin_roles"]
    if not any(ctx.guild.get_role(role_id) in ctx.author.roles for role_id in admin_roles):
        await ctx.send("You do not have permission to use this command.", ephemeral=True)
        return

    message = ctx.target
    clean_content = re.sub(r"^[ ]-", "-", message.content, flags=re.MULTILINE)

    tasks = []
    data = Markdown(clean_content).md_list
    for element in data:
        if "list" not in element:
            continue
        for item in element["list"]["items"]:
            if not item["items"]: # not category, no sub-items
                tasks.append(("", item["content"]))
            else: # is category
                category = item["content"]
                for inner_item in item["items"]:
                    tasks.append((category, inner_item["content"]))

    solardb().import_tasks(tasks)
    await ctx.send("Added tasks!", ephemeral=True)

# Start up the bot
bot.start(bot_token)
