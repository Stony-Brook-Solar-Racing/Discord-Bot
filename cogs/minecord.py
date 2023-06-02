# Imports
import discord
from discord.ext import commands
from discord import File

from PIL import Image, ImageDraw, ImageFont

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
    retrieved_stat = data[0]['405918053226774538']['stats']
    return retrieved_stat

def getInventory(user_id: int):
    data = ref.get(user_id)
    retrieved_stat = data[0]['405918053226774538']['inventory']
    return retrieved_stat

def generateInventoryImage(inv):
    # size, background color, font
    width, height = 450, 200
    background_color = (255, 255, 255)
    text_color = (255, 255, 255)

    text = f"{inv['wood']}"

    # Set up image
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Set up font
    font = ImageFont.truetype("arial.ttf", 16)

    # Draw inventory background
    inventory_background = Image.open("images\inventory_background.png")
    inventory_background = inventory_background.resize((width, height))
    image.paste(inventory_background, (0,0))

    # Draw wood
    block_image = Image.open("images\wood.png").convert("RGBA")
    block_size = (35, 35)
    block_image = block_image.resize(block_size)
    block_position = (62, 9)
    image.paste(block_image, block_position, mask=block_image)

    # Draw text on the image using the data
    draw.text((82, 24), text, font=font, fill=text_color)

    # Save the image to a temporary file
    image_path = "temp_image.png"
    image.save(image_path, format="PNG")

    return image_path

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
    async def eat(self, ctx):
        user = ctx.author
        await ctx.send(f'you have NO FOOD')

    @commands.command(aliases=['hold'], brief="Equip an item", description="N/A")
    async def equip(self, ctx):
        user = ctx.author
        await ctx.send(f'you have NOTHING')

async def setup(bot):
    await bot.add_cog(Minecord(bot))