# Imports
import json
import math
import random
from interactions import Extension, OptionType, SlashCommandChoice, check, slash_option
from interactions import slash_command, SlashContext

from databaseManager import createUserInDatabase, getInventory, getStats, negateExperience, updateStats
from helperMethods import parseEquippable

with open('enchant_data.json') as file:
    enchant_data = json.load(file)

class Enchanting(Extension):

    @check(check=createUserInDatabase)
    @slash_command(name="enchant", description="Enchant your item")
    @slash_option(
        name="item",
        description="What do you want to enchant?",
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
    async def enchant(self, ctx: SlashContext, item):

        # Some variables
        minimumEnchantLevel = 5

        user = ctx.author.id
        stats = getStats(user)
        inv = getInventory(user)

        enchanting_table = inv["placeable"]["Enchanting Table"]
        if enchanting_table == "None":
            await ctx.send("you don't have an enchanting table")
            return

        _item = stats["equipped"][item]
        if _item == "None":
            await ctx.send(f"you don't have a(n) {item}")
            return
        else:
            itemToEnchant = _item.split(" ")[0]

        print(itemToEnchant)
        parsedData = parseEquippable(itemToEnchant)
        enchants = parsedData["enchants"]
        if enchants[0] != "CLEAN0":
            await ctx.send(f"your equipped {item} is already enchanted.")
            return
        
        bookshelves = inv["placeable"]["bookshelf"]
        userLevels = stats["level"]

        minimumEnchantLevel = minimumEnchantLevel + (bookshelves * 2)

        if userLevels < minimumEnchantLevel:
            await ctx.send(f"you must be at least level {minimumEnchantLevel} to enchant items with {bookshelves} bookshelves. if you need to, run /destroy to get rid of bookshelves")
            return

        # After all checks, the user is good to enchant their stuff.

        possibleEnchantsForItem = enchant_data[item]
        random_index = random.randint(0, len(possibleEnchantsForItem)-1)
        enchantToGive = possibleEnchantsForItem[random_index]
        max_level = int(enchant_data[enchantToGive])
        proportional_value = ((userLevels - 5) / (50 - 5)) * (max_level - 1) + 1
        rounded_value = math.floor(proportional_value)
        if random.random() < 0.5:
            proportional_value = int(rounded_value)  # Round down
        else:
            proportional_value = int(rounded_value) + 1  # Round up
        if proportional_value > max_level:
            proportional_value = max_level

        allItems = _item.split()
        restOfItems = ' '.join(allItems[1:])
        newItemsData = f"{parsedData['durability']}_{parsedData['type']}_{enchantToGive}{proportional_value} {restOfItems}"
        newItemsData = newItemsData.rstrip()

        updateStats(user, f"equipped/{item}", newItemsData)
        negateExperience(user, 10)

        await ctx.send(f"it got... {enchantToGive} {proportional_value}")
