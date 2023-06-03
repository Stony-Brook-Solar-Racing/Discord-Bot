# Imports
import discord
from discord.ext import commands
from discord import File

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from image import generateInventoryImage

import json
import os

with open('config.json') as file:
    config_databaseURL = json.load(file)

# Firebase Store
cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':config_databaseURL["firebase_databaseURL"]
})
ref = db.reference('users')

def initializeNewUserData(user_id: int):
    with open('newUserData.json') as file:
        config = json.load(file)
    ref.update({
        user_id: config
    })

def updateInventory(user_id: int, item: str, newCount: int):
    user = ref.child(str(user_id))
    user.update({
        'inventory/'+item:newCount
    })

def updateStats(user_id: int, stat: str, newCount: int):
    user = ref.child(str(user_id))
    user.update({
        'stats/'+stat:newCount
    })

def getStats(user_id: int):
    data = ref.get(user_id)
    retrieved_stat = data[0][str(user_id)]['stats']
    return retrieved_stat

def getInventory(user_id: int):
    data = ref.get(user_id)
    retrieved_stat = data[0][str(user_id)]['inventory']
    return retrieved_stat

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
            print("what bitch what")
            return

        if (food[item] == 0):
            await ctx.send(f'🍖 You don\'t have {item}')
            return
        else:
            await ctx.send(f'🍖 You ate {item}')
            updateInventory(user, f"food/{item}", food[item]-1)
            updateInventory(user, f"food/total", food["total"]-1)
            return

    @commands.command(aliases=['hold'], brief="Equip an item", description="N/A")
    async def equip(self, ctx):
        user = ctx.author
        await ctx.send(f'you have NOTHING')

async def setup(bot):
    await bot.add_cog(Minecord(bot))