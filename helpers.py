# Imports
import json

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

    Returns:
        bool: True if the user is an admin
'''
def is_admin(ctx):
    admin_role = ctx.guild.get_role(1141820845237477447)  # THIS IS THE "KEY HOLDER" ROLE
    return admin_role in ctx.author.roles