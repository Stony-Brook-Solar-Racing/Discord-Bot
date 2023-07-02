# Imports
from interactions import Extension
from interactions import slash_command, SlashContext

class Enchanting(Extension):

    @slash_command(name="enchant", description="Enchant your item")
    async def enchant(self, ctx: SlashContext):
        await ctx.send("enchanting...")
