# Imports
import discord
from discord.ext import commands

import json
import random

with open('items.json') as file:
    item_manager = json.load(file)

with open('odds.json') as file:
    item_odds = json.load(file)

from databaseManager import getInventory, getStats, updateInventory, isFoodItem
from helperMethods import is_score_between, calculate_score, spliceRangeHelper

async def resource_type_handler(ctx, user: str, resourceType: str):
    gathering_items = item_manager[resourceType]

    # Check within which interval the users gathering potential lies
    user_gather_score = calculate_score(user, resourceType)
    if (is_score_between(user_gather_score, item_odds[resourceType]["1"]["low_score"], item_odds[resourceType]["1"]["high_score"])):
        # The number of items to give, from which range, and how many of each.
        num_a, num_b = spliceRangeHelper(item_odds[resourceType]["1"]["num_items"])
        from_a, from_b = spliceRangeHelper(item_odds[resourceType]["1"]["item_range"])
        amt_a, amt_b = spliceRangeHelper(item_odds[resourceType]["1"]["item_amount"])

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

            inventory = getInventory(user)
            curr_amt = 0
            if ( isFoodItem(random_item) ):
                curr_amt = inventory["food"][random_item]
            else:
                curr_amt = inventory[random_item]

            updateInventory(user, random_item, curr_amt+amt)
            updateInventory(user, f"total", inventory["food"]["total"]+amt)

            await ctx.send(f'you found {amt} {random_item}!')

class Resources(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gr'], brief="Gathers resources found from nature", description="N/A")
    async def gather(self, ctx):
        resource_type = "gather"
        user = ctx.author.id
        await ctx.send('gathering...')
        await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['hr'], brief="Hunts for resources from mobs/passive entities", description="N/A")
    async def hunt(self, ctx):
        resource_type = "hunt"
        user = ctx.author.id
        await ctx.send('hunting...')
        await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['mr'], brief="Mines for resources underground", description="N/A")
    async def mine(self, ctx):
        resource_type = "mine"
        user = ctx.author.id
        await ctx.send('mining...')
        await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['er'], brief="Explores for rare items found far from home", description="N/A")
    async def explore(self, ctx):
        resource_type = "explore"
        user = ctx.author.id
        await ctx.send('exploring...')
        await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['fr'], brief="Fishes for items in the water", description="N/A")
    async def fish(self, ctx):
        resource_type = "fish"
        user = ctx.author.id
        await ctx.send('fishing...')
        await resource_type_handler(ctx, user, resource_type)

async def setup(client):
    await client.add_cog(Resources(client))