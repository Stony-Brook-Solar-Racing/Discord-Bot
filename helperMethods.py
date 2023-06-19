# Simple helper method
def is_score_between(score, a, b):
    return (score >= a) and (score <= b)

# Simple helper method for converting a number "xy" into a range from x -> y
def spliceRangeHelper(xy):
    return (int(xy/10), xy%10)

def splitEquippables(items):
    return items.split(" ")

def parseEquippable(item):
    item = str(item)
    parts = item.split("_")
    durability = parts[0]
    type = parts[1]
    enchants = parts[2:]
    data = {
        "durability": durability,
        "type": type,
        "enchants": enchants
    }
    return data

# Return a composite score based on metrics defined in enchant_data.json
# Return a num_boost multiplier
# Return a amt_boost multiplier
def getItemBoostData(item):
    # parse eq ^
    # get the data
    # the enchants
    # separate into enchant:value
    # if enchant exist in json for num, or amt, add +0.03*value to num_boost and amt_boost
    # regardless, composite += 5 * value ? or smth
    # multiply by the type (wood = 1, iron = 2?, gold=2, diamond=4, netherite=6.)

    #examples 
    # 87_wood_eff3_unb4
    # num_boost = 0.09
    # amt_bosot = 0
    # composite = 35
    # 348_diamond_prot4
    # num_boost = 0
    # amt_boost = 0
    # compopsoite = 80
    pass