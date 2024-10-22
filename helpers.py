# Imports
import json

# This file contains helper functions used throughout the other files.

"""
    Adds two numbers together.

    Args:
        x (float or int): The first number to be added.
        y (float or int): The second number to be added.
        
    Returns:
        float or int: The sum of the two input numbers.
"""
def add(x, y):
    return x + y

'''
    Checks to see if a user is an admin. Currently checks for the
    "Key Holder" role on Discord.

    Checks to see if a user is a tester. Currently checks for the
    "Authorized Bot Tester" role on Discord.

    Returns:
        bool: True if the user is an admin
'''
def is_admin(ctx):
    admin_role = ctx.guild.get_role(764221236032307272)  # THIS IS THE "E-BOARD" ROLE
    return admin_role in ctx.author.roles

def is_tester(ctx):
    tester_role = ctx.guild.get_role(1151599685547610143) # THIS IS THE "TESTER" ROLE
    return tester_role in ctx.author.roles

def verify_access(ctx):
    if is_admin(ctx) or is_tester(ctx): return True
    return False
