# Imports
import discord
from discord.ext import commands

class Crafting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['make'], brief="Craft an item with your resources", description="N/A")
    async def craft(self, ctx):
        await ctx.send('crafting...')

async def setup(client):
    await client.add_cog(Crafting(client))