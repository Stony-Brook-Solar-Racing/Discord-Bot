from interactions import slash_command, SlashContext, Extension
from solardb import solardb
from pull_tasks import get_tasks
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

    @slash_command(name="test_tasks", description="test embed for nextcloud tasks")
    async def test_tasks(self, ctx: SlashContext):
        test_embed = embeds.print_tasks(get_tasks())
        await ctx.send(embed=test_embed)
