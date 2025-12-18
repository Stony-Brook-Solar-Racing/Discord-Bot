import json
from functools import wraps

import embeds
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
