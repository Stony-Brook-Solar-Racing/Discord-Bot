# Imports
import discord
from discord.ext import commands

import json
import random

with open('items.json') as file:
    item_manager = json.load(file)

with open('odds.json') as file:
    item_odds = json.load(file)

from databaseManager import getInventory, getStats, updateInventory
from helperMethods import is_score_between, calculate_gather_score, spliceRangeHelper

class Resources(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gr'], brief="Gathers resources found from nature", description="N/A")
    async def gather(self, ctx):
        user = ctx.author.id
        gathering_items = item_manager["gather"]

        await ctx.send('gathering...')

        # Check within which interval the users gathering potential lies
        user_gather_score = calculate_gather_score(user)
        if (is_score_between(user_gather_score, item_odds["gather"]["1"]["low_score"], item_odds["gather"]["1"]["high_score"])):
            # The number of items to give, from which range, and how many of each.
            num_a, num_b = spliceRangeHelper(item_odds["gather"]["1"]["num_items"])
            from_a, from_b = spliceRangeHelper(item_odds["gather"]["1"]["item_range"])
            amt_a, amt_b = spliceRangeHelper(item_odds["gather"]["1"]["item_amount"])

            # num_items: how many unique items to give. ex. apple (1), or an apple and a carrot (2)
            num_items = random.randint(num_a, num_b)
            for i in range(num_items):
                # rarity: how rare each item should be. could be an apple from rarity 1, or wood from rarity 2
                # amt: how many of that item to give the user. 1 apple, or 2 apples?
                rarity = random.randint(from_a, from_b)
                amt = random.randint(amt_a, amt_b)
                
                json_data = gathering_items[str(rarity)]
                random_index = random.randint(0, len(json_data) - 1)
                random_item = json_data[random_index]

                # TODO : here i can just update inventory 

                await ctx.send(f'you found {amt} {random_item}!')

    @commands.command(aliases=['hr'], brief="Hunts for resources from mobs/passive entities", description="N/A")
    async def hunt(self, ctx):
        await ctx.send('hunting...')

    @commands.command(aliases=['mr'], brief="Mines for resources underground", description="N/A")
    async def mine(self, ctx):
        await ctx.send('mining...')

    @commands.command(aliases=['er'], brief="Explores for rare items found far from home", description="N/A")
    async def explore(self, ctx):
        await ctx.send('exploring...')

    @commands.command(aliases=['fr'], brief="Fishes for items in the water", description="N/A")
    async def fish(self, ctx):
        await ctx.send('fishing...')

async def setup(client):
    await client.add_cog(Resources(client))