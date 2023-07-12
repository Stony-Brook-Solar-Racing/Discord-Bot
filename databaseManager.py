import random
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import json

from helperMethods import parseEquippable

with open('config.json') as file:
    config_databaseURL = json.load(file)

with open('newUserData.json') as file:
        data = json.load(file)

# Firebase Store
cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':config_databaseURL["firebase_databaseURL"]
})
ref = db.reference('users')

def isFoodItem(item: str):
    
    # Access the food items and create a list
    foodsList = []
    for items, quantity in data['inventory']['food'].items():
            foodsList.append(items)

    if item in foodsList:
        return True
    else:
        return False

async def createUserInDatabase(ctx):
    user_id = ctx.author.id
    exists = checkIfUserExist(user_id)
    if exists == False:
        await ctx.send(f"welcome to minecord {ctx.author.mention}. initializing new user data")
        initializeNewUserData(user_id)
        await ctx.send("initialization complete. happy mining!")
        return True
    return True

def initializeNewUserData(user_id: int):
    with open('newUserData.json') as file:
        config = json.load(file)
    ref.update({
        user_id: config
    })

def initializePreDefinedUserData(user_id: int):
    with open('preDefinedUserData.json') as file:
        config = json.load(file)
    ref.update({
        user_id: config
    })

def checkIfUserExist(user_id):
    try:
        snapshot = ref.child(str(user_id)).get()

        if snapshot is not None:
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred:", str(e))

def updateInventory(user_id: int, item: str, newCount: int):
    user = ref.child(str(user_id))
    if isFoodItem(item):
        user.update({
            'inventory/food/'+item:newCount
        })
    else:
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
    if data is not None:
        return data[0][str(user_id)]['stats']
    else:
        print("User does not exist.")

def getHunger(user_id):
    return getStats(user_id)['hunger']

def getInventory(user_id: int):
    data = ref.get(user_id)
    if data is not None:
        return data[0][str(user_id)]['inventory']
    else:
        print("User does not exist.")

with open('recipes.json') as file:
        recipes = json.load(file)
with open('enchant_data.json') as file:
        enchant_data = json.load(file)

def checkSimpleCraftable(user_id, item):
    simple = recipes["simple"]
    inv = getInventory(user_id)

    amtToGive = simple[item][0]
    recipe_items = simple[item][1:]
    for recipe_item in recipe_items:
        recipeAmt = int(recipe_item[0])
        recipeItem = recipe_item[2:]
        if isFoodItem(recipeItem):
            if not inv["food"][recipeItem] >= recipeAmt:
                return False
        else:
            if not inv[recipeItem] >= recipeAmt:
                return False
    for recipe_item in recipe_items:
        recipeAmt = int(recipe_item[0])
        recipeItem = recipe_item[2:]
        if isFoodItem(recipeItem):
            updateInventory(user_id, f"food/{recipeItem}", int(inv["food"][recipeItem]) - int(recipeAmt))
        else:
            updateInventory(user_id, f"{recipeItem}", int(inv[recipeItem]) - int(recipeAmt))
    if isFoodItem(item):
        updateInventory(user_id, f"food/{item}", int(inv["food"][item]) + int(amtToGive))
    else:
        updateInventory(user_id, f"{item}", int(inv[item]) + int(amtToGive))
    return True

def checkPlaceableCraftable(user_id, item):
    placeable = recipes["placeable"]
    invp = getInventory(user_id)["placeable"]
    inv = getInventory(user_id)
    if item == "anvil":
        if not ((inv["Iron Ingot"] >= 4) and (inv["Iron Block"] >= 3)):
            return "you don't have enough Iron Ingots (or) Blocks"
        updateInventory(user_id, f"Iron Ingot", int(inv["Iron Ingot"]) - 4)
        updateInventory(user_id, f"Iron Block", int(inv["Iron Block"]) - 3)
        updateInventory(user_id, f"placeable/anvil", int(invp["anvil"]) + 25)
        return "more anvil uses acquired"
    if item == "bookshelf":
        if not ((inv["book"] >= 3) and (inv["wood"] >= 6)):
            return "you don't have enough wood (or) books"
        updateInventory(user_id, f"book", int(inv["book"]) - 3)
        updateInventory(user_id, f"wood", int(inv["wood"]) - 6)
        updateInventory(user_id, f"placeable/bookshelf", int(invp["bookshelf"]) + 1)
        return "you built another bookshelf"
    if invp[item] != "None":
        return "you already have that. it's yours forever :)"

    recipe_items = placeable[item]
    for recipe_item in recipe_items:
        recipeAmt = int(recipe_item[0])
        recipeItem = recipe_item[2:]
        if not inv[recipeItem] >= recipeAmt:
            return f"you don't have enough {recipeItem}"
    for recipe_item in recipe_items:
        recipeAmt = int(recipe_item[0])
        recipeItem = recipe_item[2:]
        updateInventory(user_id, f"{recipeItem}", int(inv[recipeItem]) - int(recipeAmt))
    updateInventory(user_id, f"placeable/{item}", "CRAFTED")
    return f"successfully crafted {item}"

def checkEquippableCraftable(user_id, item, material):
    durability = enchant_data["durability"]
    equippable = recipes["equippable"]
    inv = getInventory(user_id)
    raw_material = material
    if material == "stone":
        material = "cobblestone"
    if material == "gold":
        material = "Gold Ingot"
    if material == "iron":
        material = "Iron Ingot"
    if material == "netherite":
        material = "Netherite Ingot"

    recipe_items = equippable[item]
    for recipe_item in recipe_items:
        recipeAmt = int(recipe_item[0])
        recipeItem = recipe_item[2:]
        if recipeItem == "GEM":
            recipeItem = material
        if not inv[recipeItem] >= recipeAmt:
            return f"you don't have enough {recipeItem}"
    for recipe_item in recipe_items:
        recipeAmt = int(recipe_item[0])
        recipeItem = recipe_item[2:]
        if recipeItem == "GEM":
            recipeItem = material
        updateInventory(user_id, f"{recipeItem}", int(inv[recipeItem]) - int(recipeAmt))
    craftedItem = f"{durability[raw_material]}_{raw_material}_CLEAN0"
    alreadyEquipped = getStats(user_id)["equipped"][item]
    if alreadyEquipped == "None":
        alreadyEquipped = craftedItem
    else:
        alreadyEquipped += " "
        alreadyEquipped += craftedItem
    updateStats(user_id, f"equipped/{item}", alreadyEquipped)
    return f"successfully crafted {item} (TYPE: {material})"
    

def attempt_kill_user(user_id: int, override):
    totem_amt = getInventory(user_id)['Totem of Undying']
    if (totem_amt > 0 and (not override)):
        updateInventory(user_id, 'Totem of Undying', totem_amt-1)
        return False
    lifetime_levels = getStats(user_id)['lifetime_level']
    initializeNewUserData(user_id)
    updateStats(user_id, 'lifetime_level', lifetime_levels)
    return True

def grantExperience(user_id: int, amount):
    updateStats(user_id, "level", getStats(user_id)["level"]+amount)
    updateStats(user_id, "lifetime_level", getStats(user_id)["lifetime_level"]+amount)

def negateExperience(user_id: int, amount):
    updateStats(user_id, "level", getStats(user_id)["level"]-amount)

def removeAllDurability(user_id):
    removeDurability(user_id, "axe")
    removeDurability(user_id, "boots")
    removeDurability(user_id, "bow")
    removeDurability(user_id, "chestplate")
    removeDurability(user_id, "crossbow")
    removeDurability(user_id, "Rod")
    removeDurability(user_id, "helmet")
    removeDurability(user_id, "hoe")
    removeDurability(user_id, "leggings")
    removeDurability(user_id, "pickaxe")
    removeDurability(user_id, "shield")
    removeDurability(user_id, "shovel")
    removeDurability(user_id, "sword")

def removeDurability(user_id, item_type, amount=1):
    amtToRemove = amount
    stats = getStats(user_id)
    item = stats["equipped"][item_type]
    if (item == "None"):
        return
    items = item.split(" ")
    itemToUpdate = items[0]

    enchants = parseEquippable(itemToUpdate)["enchants"]
    for enchant in enchants:
        if enchant.startswith("unbr"):
            numbers = re.findall(r'\d+', enchant)
            result = int(numbers[0]) if numbers else 0
            chanceToRemove = int(100 / (result + 1)) # 100, 50, 33, 25, 20
            if (item_type == "helmet" or item_type == "boots" or item_type == "chestplate" or item_type == "leggings"):
                chanceToRemove = int(60 + 40 / (result+1))
            randomNumber = random.randint(1, 100)
            if (randomNumber < chanceToRemove):
                amtToRemove = 0

    if (amount != 1):
        amtToRemove = amount

    durability = itemToUpdate[0:itemToUpdate.index("_")]
    restOfItemDescript = itemToUpdate[itemToUpdate.index("_"):]
    durability = int(durability) - amtToRemove
    newItem = str(durability) + str(restOfItemDescript)
    newItems = ""
    if (durability < 1):
        newItem = ""
        # good place to announce item broke
    newItems += newItem
    newItems += " "
    items.pop(0)
    for xitem in items:
        newItems += xitem
        newItems += " "
    newItems = newItems.rstrip()
    newItems = newItems.lstrip()
    if (newItems == ""):
        newItems = "None"
    updateStats(user_id, f"equipped/{item_type}", newItems)

def removeHunger(user_id, amount):
    newHunger = getStats(user_id)['hunger']-amount
    if newHunger < 0:
        newHunger = 0
    updateStats(user_id, f"hunger", newHunger)
    return newHunger

def grantHunger(user_id, amount):
    newHunger = getStats(user_id)['hunger']+amount
    if newHunger > 10:
        newHunger = 10
    updateStats(user_id, f"hunger", newHunger)