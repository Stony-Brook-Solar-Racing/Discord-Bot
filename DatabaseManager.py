import pymongo
import json
from urllib.parse import quote_plus

with open('config.json') as file:
    config = json.load(file)
db_user = config['mongodb_user']
db_pw = config['mongodb_pw']
db_authstring = config['mongodb_authstring']

username = quote_plus(db_user)
password = quote_plus(db_pw)

client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{db_authstring}")

# use SolarRacing database
db = client.SolarRacing
# use a collection named "DiscordBot"
BotData = db["DiscordBot"]

# Increments session number and returns new session number
def incrementSessionNumber():
    try: 
        result = BotData.find_one({"Identifier":"SessionTag"})
        lastSessionNumber = result["SessionNumber"]
        my_doc = BotData.find_one_and_update({"Identifier": "SessionTag"}, {"$set": { "SessionNumber": lastSessionNumber+1 }}, new=True)
        return lastSessionNumber+1
    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")