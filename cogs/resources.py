# Imports
import discord
from discord.ext import commands

class Resources(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gr'], brief="Gathers resources found from nature", description="N/A")
    async def gather(self, ctx):
        await ctx.send('gathering...')

    @commands.command(aliases=['hr'], brief="Hunts for resources from mobs/passive entities", description="N/A")
    async def hunt(self, ctx):
        await ctx.send('hunting...')

    @commands.command(aliases=['mr'], brief="Mines for resources underground", description="N/A")
    async def mine(self, ctx):
        await ctx.send('mining...')

    @commands.command(aliases=['er'], brief="Explores for rare items found far from home", description="N/A")
    async def explore(self, ctx):
        await ctx.send('exploring...')

    @commands.command(aliases=['er'], brief="Fishes for items in the water", description="N/A")
    async def fish(self, ctx):
        await ctx.send('fishing...')

async def setup(client):
    await client.add_cog(Resources(client))