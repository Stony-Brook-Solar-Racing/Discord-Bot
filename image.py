from PIL import Image, ImageDraw, ImageFont

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