

# Simple helper method
def is_score_between(score, a, b):
    return (score >= a) and (score <= b)

# Calculate the strength of the users items and what they can find
def calculate_gather_score(id):
    return 0

# Simple helper method for converting a number "xy" into a range from x -> y
def spliceRangeHelper(xy):
    return (int(xy/10), xy%10)