# Imports
from discord import Member
from interactions import ActionRow, Button, ButtonStyle, ComponentContext, Embed, Extension, check, component_callback
from interactions import slash_command, SlashContext

from databaseManager import createUserInDatabase

class Miscellaneous(Extension):

    @check(check=createUserInDatabase)
    @slash_command(name="nada", description="nada")
    async def nada(self, ctx: SlashContext):
        await ctx.send("NADA")

    