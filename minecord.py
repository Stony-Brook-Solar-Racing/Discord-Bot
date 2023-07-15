# Imports
import interactions
from interactions import Embed, Extension, File, OptionType, SlashCommandChoice, check, slash_command, slash_option
from interactions import slash_command, SlashContext

# Misc. imports
import json
import os

# Custom Imports
from helperMethods import parseEquippable
from image import generateInventoryImage
from databaseManager import attempt_kill_user, createUserInDatabase, getInventory, getStats, grantHunger, updateInventory, updateStats

with open('config.json') as file:
    config_databaseURL = json.load(file)
with open('food_hunger_data.json') as file:
    food_hunger_data = json.load(file)

class Minecord(Extension):

    @check(check=createUserInDatabase)
    @slash_command(name="inventory", description="Displays your current inventory")
    async def inventory(self, ctx: SlashContext):
        user = ctx.author.id
        inventory = getInventory(user)
        stats = getStats(user)
        member = ctx.author
        pfp = member.avatar.url
        inventory_image = generateInventoryImage(user, inventory, stats, pfp)
        
        # Send the image as a file
        with open(inventory_image, "rb") as fp:
            files = [interactions.File(file=fp, file_name=f"inventory_image_{user}.png")]
            await ctx.send(files=files)

            # Delete the temporary image file
            fp.close()
            os.remove(f"inventory_image_{user}.png")
            os.remove(f"user_profile_{user}.jpg")

    @check(check=createUserInDatabase)
    @slash_command(name="stats", description="Displays various player stats")
    async def stats(self, ctx: SlashContext):
        user = ctx.author.id
        stats = getStats(user)
        level = "{:.2f}".format(stats["level"])
        hunger = "{:.1f}".format(stats["hunger"])

        embed = Embed(
            title="stats",
            description=f"user: {ctx.author.username}",
            color=0x008800,  # Set the color of the embed (hex format)
        )

        embed.add_field(name="level", value=f"{level}", inline=False)
        embed.add_field(name="hunger", value=f"{hunger}/10", inline=False)

        await ctx.send(embed=embed)

    @check(check=createUserInDatabase)
    @slash_command(name="eat", description="Replenishes hunger")
    @slash_option(
        name="item",
        description="Which food do you want to eat",
        required=False,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="apple", value="apple"),
            SlashCommandChoice(name="beef", value="beef"),
            SlashCommandChoice(name="beetroot", value="beetroot"),
            SlashCommandChoice(name="bread", value="bread"),
            SlashCommandChoice(name="carrot", value="carrot"),
            SlashCommandChoice(name="chicken", value="chicken"),
            SlashCommandChoice(name="cod", value="cod"),
            SlashCommandChoice(name="Golden Apple", value="Golden Apple"),
            SlashCommandChoice(name="Golden Carrot", value="Golden Carrot"),
            SlashCommandChoice(name="Melon Slice", value="Melon Slice"),
            SlashCommandChoice(name="mutton", value="mutton"),
            SlashCommandChoice(name="porkchop", value="porkchop"),
            SlashCommandChoice(name="potato", value="potato"),
            SlashCommandChoice(name="rabbit", value="rabbit"),
            SlashCommandChoice(name="Rotten Flesh", value="Rotten Flesh"),
            SlashCommandChoice(name="salmon", value="salmon"),
            SlashCommandChoice(name="Sweet Berries", value="Sweet Berries")
        ]
    )
    @slash_option(
        name="amt",
        description="How much do you want to eat",
        required=False,
        opt_type=OptionType.INTEGER
    )
    async def eat(self, ctx: SlashContext, amt=1, *, item=None):
        user = ctx.author.id
        stats = getStats(user)
        hunger = stats["hunger"]
        if (hunger == 10):
            await ctx.send(f'🍖 You are full (10/10)')
            return

        inventory = getInventory(user)
        food = inventory["food"]
        if (food["total"] == 0):
            if (hunger < 1):
                # No food and no hunger
                await ctx.send(f"notch notices you are starving and have no food. fine. you will be spared, this once.")
                grantHunger(user, 5)
                return
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
            grantHunger(user, food_hunger_data[item]*amt)
            return

    @check(check=createUserInDatabase)
    @slash_command(name="food", description="Check your food items")
    async def food(self, ctx: SlashContext):
        user = ctx.author.id
        inventory = getInventory(user)
        food = inventory["food"]
        foods = list(food.keys())
        items = []
        embed = Embed(
            title="stats",
            description=f"user: {ctx.author.username}",
            color=0x008800,  # Set the color of the embed (hex format)
        )
        for foodx in foods:
            if food[foodx] != 0:
                items.append(foodx)
        display = ""
        for item in items:
            embed.add_field(name=f"{item}", value=f"{food[item]}", inline=False)
            display+=f'{item}: {food[item]}\n'
        if display == "":
            embed.add_field(name=f"no food.", value=" ", inline=False)
        await ctx.send(embed=embed)

    @check(check=createUserInDatabase)
    @slash_command(name="equip", description="Equip an item")
    @slash_option(
        name="item_type",
        description="What do you want to equip?",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="sword", value="sword"),
            SlashCommandChoice(name="axe", value="axe"),
            SlashCommandChoice(name="boots", value="boots"),
            SlashCommandChoice(name="bow", value="bow"),
            SlashCommandChoice(name="crossbow", value="crossbow"),
            SlashCommandChoice(name="chestplate", value="chestplate"),
            SlashCommandChoice(name="Fishing Rod", value="Fishing Rod"),
            SlashCommandChoice(name="helmet", value="helmet"),
            SlashCommandChoice(name="hoe", value="hoe"),
            SlashCommandChoice(name="leggings", value="leggings"),
            SlashCommandChoice(name="pickaxe", value="pickaxe"),
            SlashCommandChoice(name="shield", value="shield"),
            SlashCommandChoice(name="shovel", value="shovel")
        ]
    )
    @slash_option(
        name="number",
        description="Which one do you want to equip?",
        required=True,
        opt_type=OptionType.INTEGER
    )
    async def equip(self, ctx: SlashContext, item_type, number):
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

    @check(check=createUserInDatabase)
    @slash_command(name="items", description="Check what you own")
    async def items(self, ctx: SlashContext):
        user = ctx.author.id
        items_message = ""
        inv = getStats(user)
        equipped = inv['equipped']

        embed = Embed(
            title="stats",
            description=f"user: {ctx.author.username}",
            color=0x008800,  # Set the color of the embed (hex format)
        )

        for key, value in equipped.items():
            if value=="None": continue
            items_message = ""
            first_item_counter = 1
            for v in value.split(" "):
                v_data = parseEquippable(v)
                items_message += f'({first_item_counter}) *{v_data["type"]}* {key} {v_data["enchants"]}'
                if first_item_counter == 1:
                    items_message += " <-(EQUIPPED)"
                first_item_counter+=1
                items_message += "\n"
            items_message += "\n"
            embed.add_field(name=f"{key}", value=f"{items_message}", inline=False)
        if items_message == "":
            items_message = "you have no equippable items"
            embed.add_field(name=f"you have no equippable items", value=f" ", inline=False)
        await ctx.send(embed=embed)

    @check(check=createUserInDatabase)
    @slash_command(name="die", description="Kill your character")
    @slash_option(
        name="confirmation",
        description="Please type 'CONFIRM DEATH' here to confirm",
        required=False,
        opt_type=OptionType.STRING
    )
    async def die(self, ctx: SlashContext, confirmation="a"):
        if confirmation != "CONFIRM DEATH":
            await ctx.send("please type the confirmation message \"CONFIRM DEATH\" to confirm your death")
            return

        user = ctx.author.id
        success = attempt_kill_user(user, False)
        if not success:
            await ctx.send("you were saved by your Totem of Undying")
        else:
            await ctx.send("you threw yourself into a pool of lava... ouch")