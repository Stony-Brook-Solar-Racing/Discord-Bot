# Imports
import discord
from discord.ext import commands

import json
import random

with open('items.json') as file:
    item_manager = json.load(file)

with open('odds.json') as file:
    item_odds = json.load(file)


with open('enchant_data.json') as file:
    enchant_data = json.load(file)

from databaseManager import getHunger, getInventory, getStats, grantExperience, removeAllDurability, removeDurability, removeHunger, updateInventory, isFoodItem
from helperMethods import parseEquippable, spliceRangeHelper, splitEquippables, getItemBoostData

async def resource_type_handler(ctx, user: str, resourceType: str):
    if (getHunger(user) < 1):
        return
    gathering_items = item_manager[resourceType]
    inv = getStats(user)

    num_a, num_b = 0, 0
    from_a, from_b = 0, 0
    amt_a, amt_b = 0, 0

    num_a, num_b = spliceRangeHelper(item_odds[resourceType]["1"]["num_items"])
    from_a, from_b = spliceRangeHelper(item_odds[resourceType]["1"]["item_range"])
    amt_a, amt_b = spliceRangeHelper(item_odds[resourceType]["1"]["item_amount"])

    if resourceType == "gather":
        factor = 50
        boost_message = "gathering...\n"
        equipped_axe = splitEquippables(inv['equipped']['axe'])[0]
        equipped_hoe = splitEquippables(inv['equipped']['hoe'])[0]

        final_eq_num = 0
        final_eq_amt = 0

        if equipped_axe != "None":
            eq_score, eq_num, eq_amt = getItemBoostData(equipped_axe)
            final_eq_num += int(eq_num*factor) # Nerfed because two items contribute
            final_eq_amt += int(eq_amt*factor)
            # formatted_value = "{:.2f}".format(eq_num)
            v_data = parseEquippable(equipped_axe)
            if (eq_num > 0 or eq_amt > 0):
                boost_message += f"your {v_data['type']} axe nets you +{int(eq_num*factor)}% item find chance, +{int(eq_amt*factor)}% resource amount chance\n"

        if equipped_hoe != "None":
            eq_score, eq_num, eq_amt = getItemBoostData(equipped_hoe)
            final_eq_num += int(eq_num*factor)
            final_eq_amt += int(eq_amt*factor)
            v_data = parseEquippable(equipped_hoe)
            if (eq_num > 0 or eq_amt > 0):
                boost_message += f"your {v_data['type']} hoe nets you +{int(eq_num*factor)}% item find chance, +{int(eq_amt*factor)}% resource amount chance\n"
                
        num_a = int(num_a * (1 + final_eq_num/factor))
        num_b = int(num_b * (1 + final_eq_num/factor))
        amt_a = int(amt_a * (1 + final_eq_amt/factor))
        amt_b = int(amt_b * (1 + final_eq_amt/factor))

        removeDurability(user, "axe")
        removeDurability(user, "hoe")

        await ctx.send(boost_message)

    if resourceType == "hunt":
        factor = 25
        boost_message = "hunting...\n"
        # check sword, axe, bow, and crossbow & apply boost
        equipped_sword = splitEquippables(inv['equipped']['sword'])[0]
        equipped_axe = splitEquippables(inv['equipped']['axe'])[0]
        equipped_bow = splitEquippables(inv['equipped']['bow'])[0]
        equipped_crossbow = splitEquippables(inv['equipped']['crossbow'])[0]

        final_eq_num = 0
        final_eq_amt = 0

        if equipped_axe != "None":
            eq_score, eq_num, eq_amt = getItemBoostData(equipped_axe)
            final_eq_num += int(eq_num*factor) # Nerfed because 4 items contribute
            final_eq_amt += int(eq_amt*factor)
            # formatted_value = "{:.2f}".format(eq_num)
            v_data = parseEquippable(equipped_axe)
            if (eq_num > 0 or eq_amt > 0):
                boost_message += f"your {v_data['type']} axe nets you +{int(eq_num*factor)}% item find chance, +{int(eq_amt*factor)}% resource amount chance\n"

        if equipped_sword != "None":
            eq_score, eq_num, eq_amt = getItemBoostData(equipped_sword)
            final_eq_num += int(eq_num*factor)
            final_eq_amt += int(eq_amt*factor)
            v_data = parseEquippable(equipped_sword)
            if (eq_num > 0 or eq_amt > 0):
                boost_message += f"your {v_data['type']} sword nets you +{int(eq_num*factor)}% item find chance, +{int(eq_amt*factor)}% resource amount chance\n"

        if equipped_bow != "None":
            eq_score, eq_num, eq_amt = getItemBoostData(equipped_bow)
            final_eq_num += int(eq_num*factor)
            final_eq_amt += int(eq_amt*factor)
            v_data = parseEquippable(equipped_bow)
            if (eq_num > 0 or eq_amt > 0):
                boost_message += f"your bow nets you +{int(eq_num*factor)}% item find chance, +{int(eq_amt*factor)}% resource amount chance\n"

        if equipped_crossbow != "None":
            eq_score, eq_num, eq_amt = getItemBoostData(equipped_crossbow)
            final_eq_num += int(eq_num*factor)
            final_eq_amt += int(eq_amt*factor)
            v_data = parseEquippable(equipped_crossbow)
            if (eq_num > 0 or eq_amt > 0):
                boost_message += f"your crossbow nets you +{int(eq_num*factor)}% item find chance, +{int(eq_amt*factor)}% resource amount chance\n"

        num_a = int(num_a * (1 + final_eq_num/factor))
        num_b = int(num_b * (1 + final_eq_num/factor))
        amt_a = int(amt_a * (1 + final_eq_amt/factor))
        amt_b = int(amt_b * (1 + final_eq_amt/factor))

        removeDurability(user, "axe")
        removeDurability(user, "sword")
        removeDurability(user, "bow")
        removeDurability(user, "crossbow")

        await ctx.send(boost_message)

    if resourceType == "mine":
        boost_message = "mining...\n"
        equipped_pickaxe = splitEquippables(inv['equipped']['pickaxe'])[0]
        v_data = parseEquippable(equipped_pickaxe)
        pick_type = v_data['type']
        if (pick_type == "stone" or pick_type == "iron" or pick_type == "gold" or pick_type == "diamond" or pick_type == "netherite"):
            from_b = 2
        if (pick_type == "iron" or pick_type == "gold" or pick_type == "diamond" or pick_type == "netherite"):
            from_b = 3
        if (pick_type == "diamond" or pick_type == "netherite"):
            from_b = 4

        eq_score, eq_num, eq_amt = getItemBoostData(equipped_pickaxe)
        eq_num = int(eq_num*100)
        eq_amt = int(eq_amt*100)
        v_data = parseEquippable(equipped_pickaxe)
        if (eq_num > 0 or eq_amt > 0):
            boost_message += f"your {v_data['type']} pickaxe nets you +{eq_num}% item find chance, +{eq_amt}% resource amount chance\n"
            await ctx.send(boost_message)
        num_a = int(num_a * (1 + eq_num/100))
        num_b = int(num_b * (1 + eq_num/100))
        amt_a = int(amt_a * (1 + eq_amt/100))
        amt_b = int(amt_b * (1 + eq_amt/100))

        removeDurability(user, "pickaxe")
        
    if resourceType == "fish":
        boost_message = "fishing...\n"
        equipped_rod = splitEquippables(inv['equipped']['Fishing Rod'])[0]
        v_data = parseEquippable(equipped_rod)

        eq_score, eq_num, eq_amt = getItemBoostData(equipped_rod)
        if (eq_score >= item_odds['fish']['composite_score_needed_3']):
            random_number = random.randint(1, 100)
            if (random_number <= item_odds['fish']['chance_for_3_item']):
                from_b = 3
        elif (eq_score >= item_odds['fish']['composite_score_needed_2']):
            random_number = random.randint(1, 100)
            if (random_number <= item_odds['fish']['chance_for_2_item']):
                from_b = 2

        eq_num = int(eq_num*100)
        eq_amt = int(eq_amt*100)
        v_data = parseEquippable(equipped_rod)
        if (eq_num > 0 or eq_amt > 0):
            boost_message += f"your fishing rod nets you +{eq_num}% item find chance, +{eq_amt}% resource amount chance\n"
            await ctx.send(boost_message)
        num_a = int(num_a * (1 + eq_num/100))
        num_b = int(num_b * (1 + eq_num/100))
        amt_a = int(amt_a * (1 + eq_amt/100))
        amt_b = int(amt_b * (1 + eq_amt/100))

        removeDurability(user, "Fishing Rod")

    # num_items: how many unique items to give. ex. apple (1), or an apple and a carrot (2)
    found_message = ""
    num_items = random.randint(num_a, num_b)
    for i in range(num_items):
        # rarity: how rare each item should be. could be an apple from rarity 1, or wood from rarity 2
        # amt: how many of that item to give the user. 1 apple, or 2 apples?
        rarity = random.randint(from_a, from_b)
        amt = random.randint(amt_a, amt_b)
        
        json_data = gathering_items[str(rarity)]
        random_index = random.randint(0, len(json_data) - 1)
        random_item = json_data[random_index]

        if (random_item == "Golden Apple"):
            amt = 1

        inventory = getInventory(user)
        curr_amt = 0
        if ( isFoodItem(random_item) ):
            curr_amt = inventory["food"][random_item]
            updateInventory(user, f"total", inventory["food"]["total"]+amt)
        else:
            curr_amt = inventory[random_item]
        
        if (getHunger(user) < 1):
            print("starve")
        updateInventory(user, random_item, curr_amt+amt)
        grantExperience(user, amt*random.randint(1,4)*enchant_data["experience_giver_strength"])
        

        found_message += f'you found {amt} {random_item}!\n'
    removeHunger(user, num_items)
    if (found_message):
        await ctx.send(found_message)

class Resources(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gr'], brief="Gathers resources found from nature", description="N/A")
    async def gather(self, ctx):
        resource_type = "gather"
        user = ctx.author.id
        if (getHunger(user) < 1):
            await ctx.send("your hunger is 0/10")
            return
        await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['hr'], brief="Hunts for resources from mobs/passive entities", description="N/A")
    async def hunt(self, ctx):
        resource_type = "hunt"
        user = ctx.author.id
        if (getHunger(user) < 1):
            await ctx.send("your hunger is 0/10")
            return
        inv = getStats(user)
        sword = inv['equipped']['sword']
        axe = inv['equipped']['axe']
        bow = inv['equipped']['bow']
        crossbow = inv['equipped']['crossbow']
        if (sword == "None" and axe == "None" and bow == "None" and crossbow == "None"):
            await ctx.send('you don\'t have a weapon! (try crafting a sword, axe, bow, or crossbow first)')
        else:
            await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['mr'], brief="Mines for resources underground", description="N/A")
    async def mine(self, ctx):
        resource_type = "mine"
        user = ctx.author.id
        if (getHunger(user) < 1):
            await ctx.send("your hunger is 0/10")
            return
        inv = getStats(user)
        pickaxe = inv['equipped']['pickaxe']
        if pickaxe == "None":
            await ctx.send('you don\'t have a pickaxe!')
        else:
            await resource_type_handler(ctx, user, resource_type)

    @commands.command(aliases=['er'], brief="Explores for rare items found far from home", description="N/A")
    async def explore(self, ctx):
        user = ctx.author.id
        if (getHunger(user) < 9):
            await ctx.send("you should eat more before exploring")
            return
        inv = getStats(user)
        inventory = getInventory(user)
        gathering_items = item_manager['explore']
        await ctx.send('exploring...')

        comp_score = 0
        einv = inv["equipped"].values()
        for eq in einv:
            if eq == "None": continue
            first_eq = splitEquippables(eq)[0]
            eq_score, eq_num, eq_amt = getItemBoostData(first_eq)
            comp_score += eq_score
        if comp_score >= item_odds['explore']['composite_score_needed_3']:
            random_number = random.randint(1, 100)
            if (random_number <= item_odds['explore']['chance_for_3_item']):
                json_data = gathering_items["3"]
                random_index = random.randint(0, len(json_data) - 1)
                random_item = json_data[random_index]
                amt = 1
                await ctx.send(f'you found {amt} {random_item}')
                updateInventory(user, random_item, inventory[random_item]+amt)
                grantExperience(user, amt*random.randint(1,4)*enchant_data["experience_giver_strength"]*2)
                removeAllDurability(user)
                removeHunger(user, 9)
                return
        elif comp_score >= item_odds['explore']['composite_score_needed_2']:
            random_number = random.randint(1, 100)
            if (random_number <= item_odds['explore']['chance_for_2_item']):
                json_data = gathering_items["2"]
                random_index = random.randint(0, len(json_data) - 1)
                random_item = json_data[random_index]
                amt = random.randint(1, 3)
                await ctx.send(f'you found {amt} {random_item}')
                updateInventory(user, random_item, inventory[random_item]+amt)
                grantExperience(user, amt*random.randint(1,4)*enchant_data["experience_giver_strength"]*2)
                removeAllDurability(user)
                removeHunger(user, 7)
                return
        else:
            await ctx.send('you don\'t make it very far...')
            # userdm = await self.client.fetch_user(user)
            # await userdm.send("looks like you didn\'t make it very far exploring. you should work on getting some stronger gear & enchants before setting off on another journey.")

        if comp_score >= item_odds['explore']['composite_score_needed_2']: await ctx.send('no luck.')

    @commands.command(aliases=['fr'], brief="Fishes for items in the water", description="N/A")
    async def fish(self, ctx):
        resource_type = "fish"
        user = ctx.author.id
        if (getHunger(user) < 1):
            await ctx.send("your hunger is 0/10")
            return
        inv = getStats(user)
        fishing_rod = inv['equipped']['Fishing Rod']
        if fishing_rod == "None":
            await ctx.send('you don\'t have a fishing rod!')
        else:
            await resource_type_handler(ctx, user, resource_type)

async def setup(client):
    await client.add_cog(Resources(client))