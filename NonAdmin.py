from interactions import slash_command, SlashContext, Extension
import SolarSheet
import embeds

class NonAdmin(Extension):
    # Check whos in shop currently
    @slash_command(name="peoplein", description="send an embed of who's in the shop")
    async def peoplein(self, ctx: SlashContext):
        names = SolarSheet.get_ppl_in_shop_names()
        shop_embed = embeds.get_people_in_shop(names)
        await ctx.send(embed=shop_embed);
        # await ctx.send("test again")
