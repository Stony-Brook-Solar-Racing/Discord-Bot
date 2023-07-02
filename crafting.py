# Imports
from interactions import Extension
from interactions import slash_command, SlashContext

class Crafting(Extension):

    @slash_command(name="craft", description="Craft an item with your resources")
    async def craft(self, ctx: SlashContext):
        await ctx.send("crafting...")
