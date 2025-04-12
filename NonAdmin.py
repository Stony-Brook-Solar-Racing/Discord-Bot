from interactions import slash_command, SlashContext, Extension
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

    @slash_command(name="ryan", description="swipes other ryan in and out")
    async def ryan(self, ctx: SlashContext):
        solardb().ryan()
        self.peoplein(SlashContext)
