import json
from urllib.parse import quote_plus

import pymongo

# DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH #
# DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH #
# Get config vars
with open("config.json") as file:
    config = json.load(file)
db_user = config["mongodb_user"]
db_pw = config["mongodb_pw"]
db_authstring = config["mongodb_authstring"]
# Quote_plus config vars
username = quote_plus(db_user)
password = quote_plus(db_pw)
# Log into client
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{db_authstring}")
# use SolarRacing database
db = client.SolarRacing
# use a collection named "DiscordBot"
BotData = db["DiscordBot"]
# DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH #
# DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH # # DO NOT TOUCH #


# Increments session number and returns new session number
def incrementSessionNumber():
    try:
        result = BotData.find_one({"Identifier": "SessionTag"})
        lastSessionNumber = result["SessionNumber"]
        my_doc = BotData.find_one_and_update(
            {"Identifier": "SessionTag"},
            {"$set": {"SessionNumber": lastSessionNumber + 1}},
            new=True,
        )
        print(
            f"SessionNumber successfully updates from {lastSessionNumber} to {lastSessionNumber+1}"
        )
        return lastSessionNumber + 1
    except pymongo.errors.OperationFailure:
        print(
            "An authentication error was received. Are you sure your database user is authorized to perform write operations?"
        )
