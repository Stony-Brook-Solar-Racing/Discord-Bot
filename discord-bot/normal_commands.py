import embeds
from interactions import (
    Extension,
    SlashContext,
    slash_command,
)
from solardb import solardb


class NonAdmin(Extension):
    @slash_command(name="peoplein", description="send an embed of who's in the shop")
    async def peoplein(self, ctx: SlashContext):
        names = solardb().people_in_names()
        shop_embed = embeds.get_people_in_shop(names)
        await ctx.send(embed=shop_embed)

    @slash_command(
        name="leaderboard", description="send an embed of the leaderboard of times"
    )
    async def leaderboard(self, ctx: SlashContext):
        people = solardb().get_leaderboard()
        shop_embeds = embeds.get_leaderboard(people)
        for embed in shop_embeds:
            await ctx.send(embed=embed)
