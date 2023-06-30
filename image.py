from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont
import requests

def generateInventoryImage(inv, stats, pfp):
    # Set up image with width and height
    width, height = 437, 412
    image = Image.new("RGB", (width, height), None)
    draw = ImageDraw.Draw(image)

    # Set up font for text and outline
    font = ImageFont.truetype("arial.ttf", 16)
    font_outline = ImageFont.truetype("arial.ttf", 20)

    # Draw inventory background
    inventory_background = Image.open("images\inventory_background.png")
    inventory_background = inventory_background.resize((width, height))
    image.paste(inventory_background, (0,0))

    # Display user profile picture and total levels
    response = requests.get(pfp)
    if response.status_code == 200:
        with open("temp.jpg", "wb") as file:
            file.write(response.content)
    profile = Image.open("temp.jpg")
    profile = profile.resize((100, 100))
    image.paste(profile, (118,35))

    lifetime_levels_text = f"Lifetime Levels"
    lifetime_levels_num = int(stats['lifetime_level'])
    lifetime_levels_num = "{:05d}".format(lifetime_levels_num)

    draw.text((116, 140), lifetime_levels_text, font=font, fill=(0, 0, 0))
    draw.text((145, 160), lifetime_levels_num, font=font, fill=(0, 0, 0))

    os.remove("temp.jpg")

    # Variables for displaying inventory
    block_size = (35, 35)
    block_x, block_y = 21, 210
    relative_text_x, relative_text_y = 20, 20
    row, col = 3, 9
    item_index = 0

    items = []
    for item, amount in inv.items():
        if (item != "food" and item != "placeable" and amount > 0):
            items.append(item)

    # Draw each item in inventory
    for i in range(row):
        for j in range(col):
            if (item_index >= len(items)):
                break
            item = items[item_index]
            text = f"{inv[item]}"

            block_position = (block_x, block_y)

            block_image = Image.open(f"images\{item}.png").convert("RGBA")
            block_image = block_image.resize(block_size)
            image.paste(block_image, block_position, mask=block_image)

            draw.text((block_x+relative_text_x, block_y+relative_text_y), text, font=font, fill=(255, 255, 255))
            draw.text((block_x+relative_text_x-1, block_y+relative_text_y-1), text, font=font_outline, fill=(0, 0, 0))

            item_index += 1
            block_x += 45
        block_x = 22
        block_y += 45

    # Write food hunger and level
    food_text = f"food: {inv['food']['total']}"
    hunger_text = f"hunger: {stats['hunger']}/10"
    level_text = f"level: "
    level_text += "{:.2f}".format(stats["level"])
    draw.text((290, 170), level_text, font=font, fill=(0, 0, 0))
    draw.text((290, 150), hunger_text, font=font, fill=(0, 0, 0))
    draw.text((290, 130), food_text, font=font, fill=(0, 0, 0))

    # Highlight the placeables that I have
    anvil = inv['placeable']['anvil']
    beacon = inv['placeable']['beacon']
    blast_furnace = inv['placeable']['Blast Furnace']
    crafting_table = inv['placeable']['Crafting Table']
    enchanting_table = inv['placeable']['Enchanting Table']
    grindstone = inv['placeable']['grindstone']
    bookshelf = inv['placeable']['bookshelf']

    def paste_block(item, pos):
        block_image = Image.open(f"tools\{item}.png").convert("RGBA")
        block_image = block_image.resize(block_size)
        image.paste(block_image, pos, mask=block_image)

    if anvil != 0:
        paste_block("anvil", (270, 81))
        draw.text((283, 92), str(anvil), font=font, fill=(255, 255, 255))
    if beacon != "None":
        paste_block("beacon", (360, 81))
    if blast_furnace != "None":
        paste_block("Blast Furnace", (270, 20))
    if crafting_table != "None":
        paste_block("Crafting Table", (317, 56))
    if enchanting_table != "None":
        paste_block("Enchanting Table", (317, 92))
    if grindstone != "None":
        paste_block("grindstone", (317, 16))
    if bookshelf != 0:
        paste_block("bookshelf", (360, 20))
        draw.text((374, 31), str(bookshelf), font=font, fill=(255, 255, 255))
    

    # Display armor and tools
    equipped = stats['equipped']
    hotbar = ["sword", "pickaxe", "axe", "shovel", "hoe", "crossbow", "bow", "shield", "Fishing Rod"]
    start_x, start_y = 22, 355

    for item in hotbar:
        spliced = equipped[item].split(" ")
        the_item = spliced[0]
        if the_item == "None":
            start_x += 45
            continue
        block_image = Image.open(f"tools/blank_cover.png").convert("RGBA")
        block_image = block_image.resize(block_size)
        image.paste(block_image, (start_x, start_y), mask=block_image)
        png_name = ""
        png_name += the_item.split("_")[1]
        png_name += "_"
        png_name += item
        block_image = Image.open(f"tools/{png_name}.png").convert("RGBA")
        block_image = block_image.resize(block_size)
        image.paste(block_image, (start_x, start_y), mask=block_image)
        if (the_item.split("_")[2] != "CLEAN0"):
            block_image = Image.open(f"tools/sparkle.png").convert("RGBA")
            block_image = block_image.resize((15, 15))
            image.paste(block_image, (start_x-3, start_y-3), mask=block_image)
        start_x += 45

    armor = ["helmet", "chestplate", "leggings", "boots"]
    start_x, start_y = 21, 21
    for item in armor:
        spliced = equipped[item].split(" ")
        the_item = spliced[0]
        if the_item != "None":
            block_image = Image.open(f"tools/blank_cover.png").convert("RGBA")
            block_image = block_image.resize(block_size)
            image.paste(block_image, (start_x, start_y), mask=block_image)
            png_name = ""
            png_name += the_item.split("_")[1]
            png_name += "_"
            png_name += item
            block_image = Image.open(f"tools/{png_name}.png").convert("RGBA")
            block_image = block_image.resize(block_size)
            image.paste(block_image, (start_x, start_y), mask=block_image)
            if (the_item.split("_")[2] != "CLEAN0"):
                block_image = Image.open(f"tools/sparkle.png").convert("RGBA")
                block_image = block_image.resize((15, 15))
                image.paste(block_image, (start_x-3, start_y-3), mask=block_image)
        start_y += 45

    
    # Save the image to a temporary file  and return
    image_path = "temp_image.png"
    image.save(image_path, format="PNG")

    return image_path