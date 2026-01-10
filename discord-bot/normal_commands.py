import re

import interactions
from interactions import (
    Extension,
    SlashContext,
    slash_command,
    Embed,
    Button,
    ButtonStyle,
    component_callback,
    spread_to_rows,
)

import embeds
from solardb import solardb

PREV_ID = "lb_prev"
NEXT_ID = "lb_next"


def create_leaderboard_embed(people, page=1, items_per_page=25):
    total_pages = (len(people) - 1) // items_per_page + 1
    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_data = people[start:end]

    if not page_data:
        return Embed(title="Leaderboard", description="No data available.")

    lines = []
    max_name_length = max(len(f"{p[0]} {p[1]}") for p in page_data)

    for i, person in enumerate(page_data, start=start + 1):
        total_seconds = person[2].total_seconds()
        hours = int(total_seconds // 3600)
        mins = int((total_seconds // 60) % 60)
        time_str = f"{hours}h {mins}m" if hours > 0 else f"{int(total_seconds // 60)}m"

        name_str = f"{person[0]} {person[1]}"
        lines.append(f"{i:<2} {name_str:<{max_name_length}} {time_str}")

    embed = Embed(title="Leaderboard")
    embed.add_field(
        name=f"Ranks (Page {page}/{total_pages})",
        value="```\n" + "\n".join(lines) + "\n```",
    )
    embed.set_footer(text="Sign out if you want time!!!")
    return embed


class NonAdmin(Extension):
    @slash_command(name="peoplein", description="send an embed of who's in the shop")
    async def peoplein(self, ctx: SlashContext):
        names = solardb().people_in_names()
        shop_embed = embeds.get_people_in_shop(names)
        await ctx.send(embed=shop_embed)

    @interactions.slash_command(
        name="leaderboard", description="View the time leaderboard"
    )
    async def leaderboard(self, ctx: SlashContext):
        people = solardb().get_leaderboard()

        current_page = 1
        components = [
            Button(
                style=ButtonStyle.SECONDARY,
                label="Previous",
                custom_id=f"{PREV_ID}_{current_page}",
            ),
            Button(
                style=ButtonStyle.SECONDARY,
                label="Next",
                custom_id=f"{NEXT_ID}_{current_page}",
            ),
        ]

        await ctx.send(
            embed=create_leaderboard_embed(people, page=current_page),
            components=spread_to_rows(*components),
        )

    @component_callback(re.compile(f"({PREV_ID}|{NEXT_ID})_(\d+)"))
    async def on_leaderboard_nav(self, ctx: interactions.ComponentContext):
        custom_id = ctx.custom_id
        action, page_num = custom_id.rsplit("_", 1)
        page_num = int(page_num)

        people = solardb().get_leaderboard()
        total_pages = (len(people) - 1) // 25 + 1

        if action == PREV_ID:
            new_page = max(1, page_num - 1)
        else:
            new_page = min(total_pages, page_num + 1)

        if new_page == page_num:
            return await ctx.send("You've reached the end!", ephemeral=True)

        new_components = [
            Button(
                style=ButtonStyle.SECONDARY,
                label="Previous",
                custom_id=f"{PREV_ID}_{new_page}",
            ),
            Button(
                style=ButtonStyle.SECONDARY,
                label="Next",
                custom_id=f"{NEXT_ID}_{new_page}",
            ),
        ]

        await ctx.edit_origin(
            embed=create_leaderboard_embed(people, page=new_page),
            components=spread_to_rows(*new_components),
        )
