import embeds
import interactions
from interactions import (
    Button,
    ButtonStyle,
    Embed,
    Extension,
    File,
    OptionType,
    SlashCommandChoice,
    SlashContext,
    check,
    slash_command,
    slash_option,
)
from solardb import solardb

# This file contains the following slash commands:
# (ADMIN) sendrules - has the bot send out embeded list of rules
# (ADMIN) botsay - has the bot say anything


with open("config.json") as file:
    config = json.load(file)


def verify_access(ctx):
    admin_roles = config["admin_roles"]
    return any(
        ctx.guild.get_role(role_id) in ctx.author.roles for role_id in admin_roles
    )


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
    async def openshop(self, ctx: SlashContext, type="General", plan="N/A", time="N/A"):
        if not verify_access(ctx):
            return
        session_number = solardb().next_session()
        shop_embed = embeds.getShopHoursEmbed(type, plan, time, session_number)
        await ctx.send(embed=shop_embed)

    """
        Close the shop. No parameters
    """

    @slash_command(name="closeshop", description="send an embed to shut it down")
    async def closeshop(self, ctx: SlashContext):
        if not verify_access(ctx):
            return  # Checks access
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
    async def sendrules(self, ctx: SlashContext):
        if not verify_access(ctx):
            return  # Checks access

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
    async def bot_say(self, ctx: SlashContext, message: str = "GO SEAWOLVES!"):
        if not verify_access(ctx):
            return  # Checks access

        await ctx.channel.send(message)

    @slash_command(name="tasks", description="send embeds of nextcloud tasks")
    @slash_option(
        name="account",
        description="Which nextcloud account?",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="Admin", value="admin"),
            SlashCommandChoice(name="Mechanical", value="mech"),
            SlashCommandChoice(name="Electrical", value="electrical"),
            SlashCommandChoice(name="Software", value="software"),
        ],
    )
    async def send_tasks(self, ctx: SlashContext, account="software"):
        if not verify_access(ctx):
            return  # Checks access

        import asyncio
        from collections import defaultdict

        from embeds import build_parent_task_embeds_grouped_by_list
        from pull_tasks import calendars_with_vtodo, chunked, get_config, report_vtodos

        # ACK to give server time to generate embeds
        await ctx.defer(ephemeral=False)

        await ctx.send(f"*Sending {account}s Tasks*")
        nc_config = get_config(account)
        NEXTCLOUD_URL = nc_config[0]
        CALDAV_HOME = nc_config[1]
        AUTH = nc_config[2]

        try:
            if account == "admin":
                calendars = [
                    (
                        "/remote.php/dav/calendars/admin/administrative-tasks/",
                        "Administrative Tasks",
                    )
                ]
            else:
                calendars = await asyncio.to_thread(
                    calendars_with_vtodo, NEXTCLOUD_URL, CALDAV_HOME, AUTH
                )
            if not calendars:
                await ctx.send("No task lists (VTODO calendars) found.")
                return

            by_uid = {}
            listname_of_uid = {}
            all_tasks = []

            for cal_href, cal_name in calendars:
                vtodos = await asyncio.to_thread(
                    report_vtodos, NEXTCLOUD_URL, cal_href, AUTH
                )
                for t in vtodos:
                    if not t.get("UID"):
                        continue
                    t["_LISTNAME"] = cal_name
                    t["_LISTHREF"] = cal_href
                    by_uid[t["UID"]] = t
                    listname_of_uid[t["UID"]] = cal_name
                    all_tasks.append(t)

            # Build parent→children and one-embed-per-parent
            children_of = defaultdict(list)
            for t in all_tasks:
                if t.get("_PARENT_UID"):
                    children_of[t["_PARENT_UID"]].append(t["UID"])
                for cu in t.get("_CHILD_UIDS", []):
                    children_of[t["UID"]].append(cu)

            embeds_by_list = build_parent_task_embeds_grouped_by_list(
                by_uid, children_of, listname_of_uid, tz="America/New_York"
            )

            for list_name, embeds in embeds_by_list.items():
                await ctx.send(f"**List:** {list_name} — {len(embeds)} parent task(s)")
                if not embeds:
                    continue
                for batch in chunked(embeds, 10):
                    await ctx.send(embeds=batch)

        except Exception as e:
            await ctx.send(f"Error while fetching tasks: `{e}`")

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
    async def add_time(self, ctx: SlashContext, first_name, last_name, time):
        if not verify_access(ctx):
            return  # Checks access
        result = solardb().add_time(first_name, last_name, float(time))
        if result == None:
            await ctx.send(f"{first_name} {last_name} does not exist")
        else:
            await ctx.send(f"added {time} hours to {first_name} {last_name}")
