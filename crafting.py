# Imports
import json
from interactions import Extension, OptionType, SlashCommandChoice, check, slash_option
from interactions import slash_command, SlashContext

from databaseManager import checkEquippableCraftable, checkPlaceableCraftable, checkSimpleCraftable, createUserInDatabase, getInventory, updateInventory

with open('recipes.json') as file:
    recipes = json.load(file)

class Crafting(Extension):

    @check(check=createUserInDatabase)
    @slash_command(name="craft", description="Craft an item with your resources")
    @slash_option(
        name="item",
        description="what do you want to craft?",
        required=True,
        opt_type=OptionType.STRING
    )
    async def craft(self, ctx: SlashContext, *, item: str):
        simple = recipes["simple"]
        placeable = recipes["placeable"]
        equippable = recipes["equippable"]
        user_id = ctx.author.id

        final_msg = f'cannot craft "{item}"'
        
        if item in simple:
            canCraft = checkSimpleCraftable(user_id, item)
            if canCraft:
                final_msg = f"crafted {item}"

        elif item in placeable:
            final_msg = checkPlaceableCraftable(user_id, item)

        elif item in equippable:
            final_msg = checkEquippableCraftable(user_id, item)

        else:
            final_msg = "idf isadfasuifsda"
            
        await ctx.send(final_msg)

    @check(check=createUserInDatabase)
    @slash_command(name="destroy", description="destroy an item")
    @slash_option(
        name="item",
        description="What are you destroying?",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="bookshelf", value="bookshelf"),
        ]
    )
    async def destroy(self, ctx: SlashContext, *, item: str):
        user_id = ctx.author.id
        inv = getInventory(user_id)
        final_msg = "destroyed nothing"
        if (item == "bookshelf") and (inv["placeable"]["bookshelf"] > 0):
            updateInventory(user_id, f"placeable/bookshelf", int(inv["placeable"]["bookshelf"]) - 1)
            final_msg = "destroyed bookshelf"
            
        await ctx.send(final_msg)

    @check(check=createUserInDatabase)
    @slash_command(name="smelt", description="Smelt an item with your resources")
    @slash_option(
        name="item",
        description="What are you smelting?",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="Ancient Debris", value="Ancient Debris"),
        ]
    )
    async def smelt(self, ctx: SlashContext, *, item: str):
        smelt = recipes["smelt"]
        user_id = ctx.author.id
        final_msg = f'you don\'t have a blast furnace'
        inv = getInventory(user_id)
        if inv["placeable"]["Blast Furnace"] != "None":
            if inv[item] > 0:
                updateInventory(user_id, f"{item}", int(inv[item]) - 1)
                updateInventory(user_id, f"{smelt[item]}", int(inv[smelt[item]]) + 1)
                updateInventory(user_id, f"placeable/Blast Furnace", int(inv["placeable"]["Blast Furnace"]) + 1)
                final_msg = f'smelted {item} into {smelt[item]}'
        await ctx.send(final_msg)
