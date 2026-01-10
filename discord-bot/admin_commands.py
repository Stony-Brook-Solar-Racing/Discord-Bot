import re
import json
from functools import wraps

import interactions
from interactions import (
    Button,
    ButtonStyle,
    Embed,
    Extension,
    OptionType,
    SlashContext,
    slash_command,
    slash_option,
)

import embeds
from solardb import solardb

# This file contains the following slash commands:
# (ADMIN) sendrules - has the bot send out embeded list of rules
# (ADMIN) botsay - has the bot say anything
# (ADMIN) openshop
# (ADMIN) closeshop
# (ADMIN) add_time


with open("config.json") as file:
    config = json.load(file)


def verify_access(ctx):
    admin_roles = config["admin_roles"]
    return any(
        ctx.guild.get_role(role_id) in ctx.author.roles for role_id in admin_roles
    )


def admin_only():
    """Decorator to restrict slash commands to users passing verify_access"""

    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: interactions.SlashContext, *args, **kwargs):
            if not verify_access(ctx):
                await ctx.send(
                    "You do not have permission to use this command.", ephemeral=True
                )
                return
            return await func(self, ctx, *args, **kwargs)

        return wrapper

    return decorator


class SolarRacing(Extension):
    """
    Opens the shop with given parameters
    Has default options "General" "N/A" "N/A"
    Dynamically increments session shop #

    ARGS:
        type: String, the type of shop hours
        plan: String, what you intend to do
        time: String, how long you plan to be there

    RETURNS:
        nada
    """

    @slash_command(
        name="openshop", description="send an embed to describe your shop hours"
    )
    @slash_option(
        name="type",
        description="what kind of hours are these?",
        required=False,
        opt_type=OptionType.STRING,
    )
    @slash_option(
        name="plan",
        description="what is this shop centered around?",
        required=False,
        opt_type=OptionType.STRING,
    )
    @slash_option(
        name="time",
        description="how long do you plan to stay?",
        required=False,
        opt_type=OptionType.STRING,
    )
    @admin_only()
    async def openshop(self, ctx: SlashContext, type="General", plan="N/A", time="N/A"):
        session_number = solardb().next_session()
        shop_embed = embeds.getShopHoursEmbed(type, plan, time, session_number)
        await ctx.send(embed=shop_embed)

    """
        Close the shop. No parameters
    """

    @slash_command(name="closeshop", description="send an embed to shut it down")
    @admin_only()
    async def closeshop(self, ctx: SlashContext):
        shop_embed = embeds.getShopHoursClosedEmbed()
        await ctx.send(embed=shop_embed)
        try:
            solardb().shop_closed()
        except Exception as e:
            print(e)

    """
        Sends out an embeded list of rules

        ARGS:
            nada

        RETURNS:
            nada
    """

    @slash_command(name="sendrules", description="send a full list of rules")
    @admin_only()
    async def sendrules(self, ctx: SlashContext):
        rules_array = embeds.getRulesEmbeds()
        for rule in rules_array:
            pass
            await ctx.channel.send(embed=rule)

        embed = Embed(
            title="Follow Discord’s Rules",
            description="Abide by the Discord Terms of Service and Guidelines.",
            color=0xF8E71C,
        )

        components = [
            Button(
                style=ButtonStyle.URL,
                label="Terms of Service",
                url="https://discord.com/terms",
            ),
            Button(
                style=ButtonStyle.URL,
                label="Guidelines",
                url="https://discord.com/guidelines",
            ),
        ]

        # send the discord TOS and guidelines
        await ctx.channel.send(embed=embed, components=components)

    """
        Sends a message as the bot

        ARGS:
            String : The message to send

        RETURNS:
            nada
    """

    @slash_command(name="botsay", description="Have the bot send a custom message")
    @slash_option(
        name="message",
        description="what do you want to say?",
        required=True,
        opt_type=OptionType.STRING,
    )
    @admin_only()
    async def bot_say(self, ctx: SlashContext, message: str):
        await ctx.channel.send(message)
        await ctx.send(ephemeral=True, content="sent", delete_after=1)

    @slash_command(name="add_time", description="Add time to the leaderboard")
    @slash_option(
        name="first_name",
        description="first name of person",
        required=True,
        opt_type=OptionType.STRING,
    )
    @slash_option(
        name="last_name",
        description="last name of person",
        required=True,
        opt_type=OptionType.STRING,
    )
    @slash_option(
        name="time",
        description="time in hours to add",
        required=True,
        opt_type=OptionType.STRING,
    )
    @admin_only()
    async def add_time(self, ctx: SlashContext, first_name, last_name, time):
        try:
            float(time)
        except ValueError:
            await ctx.send("Invalid number. Provide a number only")
            return
        result = solardb().add_time(first_name, last_name, float(time))
        if result is None:
            await ctx.send(f"{first_name} {last_name} does not exist")
        else:
            await ctx.send(f"added {time} hours to {first_name} {last_name}")

    @slash_command(name="task", description="Manage tasks")
    @admin_only()
    async def tasks_base(self, ctx=None):
        pass

    @tasks_base.subcommand(sub_cmd_name="show", sub_cmd_description="Show all tasks")
    @slash_option(
        name="filter",
        description="Category name",
        required=False,
        opt_type=OptionType.STRING,
    )
    @admin_only()
    async def show_tasks(self, ctx: SlashContext, filter=None):
        raw_tasks = solardb().get_tasks(filter)
        tasks_dict = {}
        for task in raw_tasks:
            id, category, content, is_complete = task
            if category not in tasks_dict:
                tasks_dict[category] = []
            tasks_dict[category].append((id, content, is_complete))

        embed = Embed(title="Tasks")
        for category, tasks in tasks_dict.items():
            tasks_text = ""
            for task in tasks:
                id, content, is_complete = task
                check_text = ":white_check_mark:" if is_complete else ":x:"
                tasks_text += f"{id}\. {check_text} {content}\n"
            embed.add_field(name=category, value=tasks_text)

        await ctx.send(embed=embed)

    @tasks_base.subcommand(
        sub_cmd_name="purge", sub_cmd_description="Delete complete tasks"
    )
    @admin_only()
    async def purge_tasks(self, ctx: SlashContext):
        solardb().purge_tasks()
        await ctx.send("Whoosh! :dash: All finished tasks have been removed")

    @tasks_base.subcommand(
        sub_cmd_name="complete", sub_cmd_description="Complete task(s)"
    )
    @slash_option(
        name="ids",
        description="Comma-separated list of IDs (e.g. 1,2,5)",
        required=True,
        opt_type=OptionType.STRING,
    )
    @admin_only()
    async def complete_task(self, ctx: SlashContext, ids: str):
        if not re.match(r"^\d+(,\d+)*$", ids):
            await ctx.send(
                "Oops! I couldn't read those IDs. :face_with_spiral_eyes:\n"
                "Please only use numbers separated by commas (like `1,2,5`) with no spaces!"
            )
            return

        id_list = [int(x) for x in ids.split(",")]
        completed_rows = solardb().complete_tasks(id_list)

        if not completed_rows:
            await ctx.send(
                "No tasks found with those IDs (or they were already completed)."
            )
            return

        response_text = "Yay! :tada: You completed:\n"
        for row in completed_rows:
            t_id = row[0]
            t_content = row[1]
            response_text += f"{t_id}\. {t_content}\n"

        await ctx.send(response_text)
