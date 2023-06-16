import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import json

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
# initializeNewUserData(405918053226774538)

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
    retrieved_stat = data[0][str(user_id)]['stats']
    return retrieved_stat

def getInventory(user_id: int):
    data = ref.get(user_id)
    retrieved_stat = data[0][str(user_id)]['inventory']
    return retrieved_stat

# Calculate the strength of the users items and what they can find
def calculate_score(id, type):
    if type=="gather":
         return calculateGatherScore(id)
    if type=="hunt":
         return calculateHuntScore(id)
    if type=="mine":
         return calculateMineScore(id)
    if type=="explore":
         return calculateExploreScore(id)
    if type=="fish":
         return calculateFishScore(id)
    return 0

def calculateGatherScore(id):
     return 0

def calculateHuntScore(id):
     return 0

def calculateMineScore(id):
     return 0

def calculateExploreScore(id):
     return 0

def calculateFishScore(id):
     return 0