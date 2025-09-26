import embeds
from interactions import (
    Extension,
    OptionType,
    SlashCommandChoice,
    SlashContext,
    slash_command,
    slash_option,
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
        shop_embed = embeds.get_leaderboard(people)
        await ctx.send(embed=shop_embed)
