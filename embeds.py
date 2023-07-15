from interactions import Embed


def getTutorialEmbeds():
    embeds = [

        Embed(
            title="Minecord Tutorial",
            description="welcome to minecord.\n\ncontinue forward to learn everything about this bot\n\n(and slay some dragons :flushed:)",
            color=0x705037
        ),

        Embed(
            title="checking your items",
            description="/inventory send a png like below, which includes equipped armor, tools, and your level\n\n/stats shows you a few stats about your character\n\n/items shows ALL your items, including unequipped ones.\n\n/food shows you your food items.",
            color=0x705037
        ),

        Embed(
            title="unlocking and crafting",
            description="when you start out, your inventory will look bland and gray. stations you've unlocked like the crafting table and enchanting table will be grayed out until you've created them once.\n\nwhen you have multiple items, for example, two wooden pickaxes, you can view all with /items\n\nequip a different item with /equip (tool name) (tool_number)\n(ex. /equip pickaxe 3)",
            color=0x705037
        ),

        Embed(
            title="crafting items",
            description="you can use /craft to craft.\n\nto balance the bot out from its 3D counterpart, some items may be harder to craft.\n\na full list of recipes can be found from /recipes",
            color=0x705037
        ),

        Embed(
            title="getting items.. in the first place",
            description="there are 5 main commands for exploring\n\n/gather is where you begin.\n\n/hunt requires a weapon\n\n/mine requires a pickaxe\n\n/fish requires a fishing rod\n\n/explore requires a secret amount of progression to be done.\n\nthe rest is for you to figure out\n\nat some point, you will run out of food. run /eat to eat a random food item you own, or you can supply some arguments yourself. note that /inventory does not display food items separately.",
            color=0x705037
        ),

        Embed(
            title="enchanting",
            description="ENCHANTING COMING SOON",
            color=0x705037
        ),

        Embed(
            title="the end",
            description="use these commands to progress your way to a full set of enchanted armor and tools, and when you feel prepared, you can challenge the enderdragon with /enderdragon.\n\nthis bot has a lot of features to come, so stay tuned.\n\nrun /updates for a changelog\n\nif you ever want to restart your progress, you can run /die",
            color=0x705037
        ),
    ]
    embeds[0].set_image(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c7/Grass_Block.png/revision/latest?cb=20230226144250")
    embeds[1].set_image(url="https://cdn.discordapp.com/attachments/1112448942144229426/1128457320624562248/image.png")
    embeds[2].set_image(url="https://cdn.discordapp.com/attachments/1112448942144229426/1128458374430851173/image.png")
    embeds[3].set_image(url="https://cdn.discordapp.com/attachments/1112448942144229426/1128464723915067433/image.png")
    embeds[4].set_image(url="https://cdn.discordapp.com/attachments/1112448942144229426/1128464978844860436/image.png")

    return embeds

def getUpdateEmbeds():
    embeds = [

        Embed(
            title="version 1.0",
            description="release date: 7/11/2023\n\ninitial bot release.\nreleased commands: craft, destroy, smelt, inventory, stats, eat, food, equip, items, die, gather, hunt, mine, explore, fish, recipes, updates",
            color=0x705037
        ),
    ]
    
    return embeds


def getRecipeEmbeds():

    craftable_items = f'"bread"\n"Golden Apple"\n"Golden Carrot"\n"Blaze Powder"\n"book"\n"Gold Ingot"\n"Gold Nugget"\n"Iron Ingot"\n"Iron Block"\n"Netherite Ingot"\n"stick"\n"anvil"\n"Blast Furnace"\n"Crafting Table"\n"Enchanting Table"\n"grindstone"\n"bookshelf"\n"bow"\n"crossbow"\n"Fishing Rod"\n"shield"\n"axe"\n"boots"\n"chestplate"\n"helmet"\n"hoe"\n"leggings"\n"pickaxe"\n"shovel"\n"sword"'


    embeds = [

        Embed(
            title="ALL CRAFTABLE ITEMS",
            description=f"items must be spelled EXACTLY as shown. some items, such as armor or tools, require the second MATERIAL parameter in the slash command.\n{craftable_items}",
            color=0x705037
        ),

        Embed(
            title="recipes that adhere to the 3D game",
            description="the following is a list of recipes which follow the original game. they will not be described in more detail.\n\nbread, golden apple, golden carrot, blaze powder, book, stick, ingots, nuggets, and iron blocks.\n\nall tools and armors (crossbows replace the tripwire hook with an extra iron, string, and stick)\n\nancient debris can be smelted into netherite scrap with /smelt",
            color=0x705037
        ),

        Embed(
            title="stations",
            description="the follow are the same as the original game:\n\nanvil, crafting table, enchanting table, grindstone, bookshelf\n\nbookshelves can be destroyed with /destroy (if you want weaker enchants)\n\nblast furnaces are the ONLY furnaces and require 128 cobblestone",
            color=0x705037
        ),
    ]
    
    return embeds