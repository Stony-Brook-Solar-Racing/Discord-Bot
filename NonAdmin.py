from interactions import slash_command, SlashContext, Extension, slash_option, OptionType, SlashCommandChoice
from solardb import solardb
import embeds


class NonAdmin(Extension):
    # print(SolarSheet.get_leaderboard());
    # Check whos in shop currently
    @slash_command(name="peoplein", description="send an embed of who's in the shop")
    async def peoplein(self, ctx: SlashContext):
        names = solardb().people_in()
        shop_embed = embeds.get_people_in_shop(names)
        await ctx.send(embed=shop_embed);

    @slash_command(name="leaderboard", description="send an embed of the leaderboard of times")
    async def leaderboard(self, ctx: SlashContext):
        people = solardb().get_leaderboard();
        shop_embed = embeds.get_leaderboard(people);
        await ctx.send(embed=shop_embed);

    @slash_command(name="tasks", description="send embeds of nextcloud tasks")
    @slash_option(
        name="account",
        description="Which nextcloud account?",
        required=True,
        opt_type=OptionType.STRING,
        choices = [
            SlashCommandChoice(name="Admin", value="admin"),
            SlashCommandChoice(name="Mechanical", value="mech"),
            SlashCommandChoice(name="Electrical", value="electrical"),
            SlashCommandChoice(name="Software", value="software"),
        ]
    )
    async def test_tasks(self, ctx: SlashContext, account="software"):
        from collections import defaultdict
        import asyncio
        from embeds import build_parent_task_embeds_grouped_by_list
        from pull_tasks import (
            calendars_with_vtodo, report_vtodos,
            chunked, get_config
        )

        # ACK to give server time to generate embeds
        await ctx.defer(ephemeral=False)
        
        await ctx.send(f"*Sending {account}s Tasks*") 
        config = get_config(account)
        NEXTCLOUD_URL = config[0]
        CALDAV_HOME = config[1]
        AUTH = config[2]

        try:
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
                vtodos = await asyncio.to_thread(report_vtodos, NEXTCLOUD_URL, cal_href, AUTH)
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
