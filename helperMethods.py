# Simple helper method
def is_score_between(score, a, b):
    return (score >= a) and (score <= b)

# Simple helper method for converting a number "xy" into a range from x -> y
def spliceRangeHelper(xy):
    return (int(xy/10), xy%10)