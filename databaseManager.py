import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import json

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
    retrieved_stat = data[0][str(user_id)]['stats']
    return retrieved_stat

def getInventory(user_id: int):
    data = ref.get(user_id)
    retrieved_stat = data[0][str(user_id)]['inventory']
    return retrieved_stat