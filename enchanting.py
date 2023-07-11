# Imports
from interactions import Extension, check
from interactions import slash_command, SlashContext

from databaseManager import createUserInDatabase

class Enchanting(Extension):

    @check(check=createUserInDatabase)
    @slash_command(name="enchant", description="Enchant your item")
    async def enchant(self, ctx: SlashContext):
        await ctx.send("enchanting...")
