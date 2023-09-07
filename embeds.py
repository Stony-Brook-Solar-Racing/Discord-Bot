# Imports
from interactions import Embed

"""
    This file (embeds.py) will store all embed information
    that needs to be sent out by the bot. Can return one embed,
    or an array of embeds, depending on your use case.
    
    Usage:
        from embeds import getTestEmbeds
"""

"""
    The testing Embed used to demonstrate how
    embeds are created and customized.

    Args: No Args
        
    Returns:
        Embed array with a single embed
"""
def getTestEmbeds():
    embeds = [

        Embed(
            title="this is an embed :flushed:",
            description="you love embeds",
            color=0x705037
        ),

    ]

    # Images for embeds need to be set like this
    embeds[0].set_image(url="https://google.com")

    return embeds

"""
    The rules Embed so club members behave.

    Args: No Args
        
    Returns:
        Embed array with a single embed
"""
def getRulesEmbeds():
    embeds = [

        Embed(
            title="Rule 1: Don't eat the solar panels!",
            description="They probably taste bad, and you might get sick.",
            color=0x705037
        ),

    ]

    return embeds