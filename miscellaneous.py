# Imports
from interactions import ActionRow, Button, ButtonStyle, ComponentContext, Embed, Extension, check, component_callback
from interactions import slash_command, SlashContext

from databaseManager import createUserInDatabase

class Miscellaneous(Extension):

    @check(check=createUserInDatabase)
    @slash_command(name="enderdragon", description="fight the scary dragon")
    async def EnderDragon(self, ctx: SlashContext):
        await ctx.send("rawr")

    