# Imports
import discord
from discord.ext import commands
from discord import File

import json
import os

from image import generateInventoryImage
from databaseManager import getInventory, getStats, updateInventory

with open('config.json') as file:
    config_databaseURL = json.load(file)

class Minecord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener() for built-in command implementation

    @commands.command(aliases=['inv', 'e'], brief="Displays your current inventory", description="N/A")
    async def inventory(self, ctx):
        user = ctx.author.id
        inventory = getInventory(user)
        inventory_image = generateInventoryImage(inventory)
        
        # Send the image as a file
        with open(inventory_image, "rb") as fp:
            file = File(fp, filename="image.png")
            await ctx.send(file=file)

        # Delete the temporary image file
        os.remove(inventory_image)

    """Displays user stats, such as: Hunger, level, equipped items"""
    @commands.command(aliases=['xp'], brief="Displays various player stats", description="N/A")
    async def stats(self, ctx):
        user = ctx.author.id
        stats = getStats(user)
        await ctx.send(f'you are level {stats["level"]}\nyour hunger bar is at {stats["hunger"]}')

    @commands.command(aliases=[], brief="Replenishes hunger", description="N/A")
    async def eat(self, ctx, *, item=None):
        user = ctx.author.id
        stats = getStats(user)
        hunger = stats["hunger"]
        if (hunger == 10):
            await ctx.send(f'🍖 You are full (10/10)')
            return

        inventory = getInventory(user)
        food = inventory["food"]
        if (food["total"] == 0):
            await ctx.send(f'🍖 You have no food :(')
            return
        
        if (not food.get(item)):
            await ctx.send(f'🍖 You don\'t have that')
            return
        
        if item == None:
            print("what  what")
            return

        if (food[item] == 0):
            await ctx.send(f'🍖 You don\'t have {item}')
            return
        else:
            await ctx.send(f'🍖 You ate {item}')
            updateInventory(user, f"food/{item}", food[item]-1)
            updateInventory(user, f"total", food["total"]-1)
            return

    @commands.command(aliases=['hold'], brief="Equip an item", description="N/A")
    async def equip(self, ctx):
        user = ctx.author
        await ctx.send(f'you have NOTHING')

async def setup(bot):
    await bot.add_cog(Minecord(bot))