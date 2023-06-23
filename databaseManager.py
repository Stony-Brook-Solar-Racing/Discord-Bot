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

def initializeNewUserData(user_id: int):
    with open('newUserData.json') as file:
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

def grantExperience(user_id: int, amount):
    updateStats(user_id, "level", getStats(user_id)["level"]+amount)

def removeAllDurability(user_id):
    removeDurability(user_id, "axe")
    removeDurability(user_id, "boots")
    removeDurability(user_id, "bow")
    removeDurability(user_id, "chestplate")
    removeDurability(user_id, "crossbow")
    removeDurability(user_id, "Fishing Rod")
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