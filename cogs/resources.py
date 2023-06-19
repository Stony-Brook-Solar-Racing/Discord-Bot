# Imports
import discord
from discord.ext import commands

import json
import random

with open('items.json') as file:
    item_manager = json.load(file)

with open('odds.json') as file:
    item_odds = json.load(file)

from databaseManager import getInventory, calculate_score, getStats, updateInventory, isFoodItem
from helperMethods import is_score_between, spliceRangeHelper, splitEquippables, getItemBoostData

async def resource_type_handler(ctx, user: str, resourceType: str):
    gathering_items = item_manager[resourceType]
    inv = getStats(user)

    resource_boost = 1

    # Check within which interval the users gathering potential lies
    # These are base numbers. The if statements below refine these numbers based on item quality & enchants
    user_gather_score = calculate_score(user, resourceType)
    if (is_score_between(user_gather_score, item_odds[resourceType]["1"]["low_score"], item_odds[resourceType]["1"]["high_score"])):
        # The number of items to give, from which range, and how many of each.
        num_a, num_b = spliceRangeHelper(item_odds[resourceType]["1"]["num_items"])
        from_a, from_b = spliceRangeHelper(item_odds[resourceType]["1"]["item_range"])
        amt_a, amt_b = spliceRangeHelper(item_odds[resourceType]["1"]["item_amount"])

    if resourceType == "gather":
        equipped_axe = splitEquippables(inv['equipped']['axe'])[0]
        equipped_hoe = splitEquippables(inv['equipped']['hoe'])[0]
        
        # boost on discord metrics discussed
        # repeat x2 BUT axe > hoe by factor of 2

    if resourceType == "hunt":
        # check sword, axe, bow, and crossbow & apply boost
        equipped_sword = splitEquippables(inv['equipped']['sword'])[0]
        equipped_axe = splitEquippables(inv['equipped']['axe'])[0]
        equipped_bow = splitEquippables(inv['equipped']['bow'])[0]
        equipped_crossbow = splitEquippables(inv['equipped']['crossbow'])[0]

    if resourceType == "mine":
        equipped_pickaxe = splitEquippables(inv['equipped']['pickaxe'])[0]

    if resourceType == "explore":
        comp_score = 0
        num_boost = 1
        amt_boost = 1
        einv = inv["equipped"].values()
        for eq in einv:
            if eq == "None": continue
            eq_score, eq_num, eq_amt = getItemBoostData(eq)

    if resourceType == "fish":
        equipped_rod = splitEquippables(inv['equipped']['Fishing Rod'])[0]

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
        inv = getStats(user)
        sword = inv['equipped']['sword']
        axe = inv['equipped']['axe']
        bow = inv['equipped']['bow']
        crossbow = inv['equipped']['crossbow']
        if (sword == "None" and axe == "None" and bow == "None" and crossbow == "None"):
            await ctx.send('you don\'t have a weapon! (try crafting a sword, axe, bow, or crossbow first)')
        else:
            await ctx.send('hunting...')
            await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['mr'], brief="Mines for resources underground", description="N/A")
    async def mine(self, ctx):
        resource_type = "mine"
        user = ctx.author.id
        inv = getStats(user)
        pickaxe = inv['equipped']['pickaxe']
        if pickaxe == "None":
            await ctx.send('you don\'t have a pickaxe!')
        else:
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
        inv = getStats(user)
        fishing_rod = inv['equipped']['Fishing Rod']
        if fishing_rod == "None":
            await ctx.send('you don\'t have a fishing rod!')
        else:
            await ctx.send('fishing...')
            await resource_type_handler(ctx, user, resource_type)

async def setup(client):
    await client.add_cog(Resources(client))