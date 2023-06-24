# Imports
import random
import discord
from discord.ext import commands
from discord import File

import json
import os
from helperMethods import parseEquippable

from image import generateInventoryImage
from databaseManager import getInventory, getStats, grantHunger, updateInventory, updateStats

with open('config.json') as file:
    config_databaseURL = json.load(file)

with open('food_hunger_data.json') as file:
    food_hunger_data = json.load(file)

class Minecord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener() for built-in command implementation

    @commands.command(aliases=['inv', 'e'], brief="Displays your current inventory", description="N/A")
    async def inventory(self, ctx):
        user = ctx.author.id
        inventory = getInventory(user)
        if False:
            inventory_image = generateInventoryImage(inventory)
            
            # Send the image as a file
            with open(inventory_image, "rb") as fp:
                file = File(fp, filename="image.png")
                await ctx.send(file=file)

            # Delete the temporary image file
            os.remove(inventory_image)
        else:
            await ctx.send(inventory)

    """Displays user : Hunger, level"""
    @commands.command(aliases=['xp'], brief="Displays various player stats", description="N/A")
    async def stats(self, ctx):
        user = ctx.author.id
        stats = getStats(user)
        level = "{:.2f}".format(stats["level"])
        hunger = "{:.1f}".format(stats["hunger"])
        await ctx.send(f'you are level {level}\nyour hunger bar is at {hunger}')

    @commands.command(aliases=[], brief="Replenishes hunger", description="N/A")
    async def eat(self, ctx, amt=1, *, item=None):
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
        
        if item == None:
            foods = list(food.keys())
            for foodx in foods:
                if food[foodx] != 0:
                    item = foodx
                    break

        if (not food.get(item)):
            await ctx.send(f'🍖 You don\'t have that')
            return

        if (food[item] < amt):
            await ctx.send(f'🍖 You don\'t have {amt} {item}')
            return
        else:
            await ctx.send(f'🍖 You ate {item} (x{amt}) (+{amt*food_hunger_data[item]} hunger)')
            updateInventory(user, f"food/{item}", food[item]-amt)
            updateInventory(user, f"total", food["total"]-amt)
            grantHunger(user, food_hunger_data[item])
            return

    @commands.command(aliases=['hold'], brief="Equip an item", description="N/A")
    async def equip(self, ctx, item_type, number):
        user = ctx.author.id
        items = getStats(user)['equipped'][item_type]
        if items == "None":
            await ctx.send(f"you don't have a {item_type}")
            return
        items_list = items.split(" ")
        amount = len(items_list)
        if amount == 1:
            await ctx.send(f"your only {item_type} is already equipped")
            return
        index = int(number)
        if index > amount or index==0:
            await ctx.send(f"{item_type} {index} does not exist")
            return
        if index == 1:
            await ctx.send(f"that\'s your equipped item")
            return
        to_equip = items_list[index-1]
        curr_equip = items_list[0]
        items_list[0] = to_equip
        items_list[index-1] = curr_equip

        newItemsList = ""
        for uItem in items_list:
            newItemsList += uItem
            newItemsList += " "
        newItemsList = newItemsList.rstrip()
        updateStats(user, f"equipped/{item_type}", newItemsList)
        await ctx.send(f"successfully equipped {item_type} {number}")
        

    @commands.command(aliases=['i'], brief="Check what you own", description="N/A")
    async def items(self, ctx):
        user = ctx.author.id
        items_message = ""
        inv = getStats(user)
        equipped = inv['equipped']
        for key, value in equipped.items():
            if value=="None": continue
            items_message += f"**{key}**\n"
            first_item_counter = 1
            for v in value.split(" "):
                v_data = parseEquippable(v)
                items_message += f'({first_item_counter}) *{v_data["type"]}* {key} {v_data["enchants"]}'
                if first_item_counter == 1:
                    items_message += " <-(EQUIPPED)"
                    first_item_counter+=1
                items_message += "\n"
            items_message += "\n"
        await ctx.send(items_message)

async def setup(bot):
    await bot.add_cog(Minecord(bot))