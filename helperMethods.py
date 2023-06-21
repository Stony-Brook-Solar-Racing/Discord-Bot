import json
import re

with open('enchant_data.json') as file:
    enchant_data = json.load(file)

# Simple helper method for converting a number "xy" into a range from x -> y
def spliceRangeHelper(xy):
    return (int(xy/10), xy%10)

def splitEquippables(items):
    return items.split(" ")

def parseEquippable(item):
    item = str(item)
    parts = item.split("_")
    durability = parts[0]
    item_type = parts[1]
    enchants = parts[2:]
    data = {
        "durability": durability,
        "type": item_type,
        "enchants": enchants
    }
    return data

# Return a composite score based on metrics defined in enchant_data.json
# Return a num_boost multiplier
# Return a amt_boost multiplier
def getItemBoostData(item):
    composite, num_boost, amt_boost = 0, 0, 0
    item_data = parseEquippable(item)
    item_type = item_data['type']
    type_multiplier = enchant_data['type_multiplier'][item_type]
    item_enchants = item_data['enchants']
    
    for enchant in item_enchants:
        numbers = re.findall(r'\d+', enchant)
        enchant_text = re.sub(r'\d+', '', enchant)
        enchant_value = int(numbers[0])

        composite += enchant_data['enchant_add_composite_value'] * enchant_value

        if enchant_text in enchant_data['num_item_enchant']:
            num_boost += enchant_data['enchant_add_num_boost_value'] * enchant_value
        if enchant_text in enchant_data['amt_item_enchant']:
            amt_boost += enchant_data['enchant_add_amt_boost_value'] * enchant_value

    composite *= type_multiplier
    num_boost *= type_multiplier
    amt_boost *= type_multiplier
    
    return composite, num_boost, amt_boost