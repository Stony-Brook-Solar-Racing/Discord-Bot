# Imports
import discord
from discord.ext import commands

class Enchanting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[], brief="Enchant an item", description="N/A")
    async def enchant(self, ctx):
        await ctx.send('enchanting...')

async def setup(client):
    await client.add_cog(Enchanting(client))