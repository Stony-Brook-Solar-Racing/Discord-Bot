# Imports
import interactions
from interactions import Embed, Extension, File, OptionType, SlashCommandChoice, check, slash_command, slash_option
from interactions import slash_command, SlashContext
from helpers import is_admin
import json
import os

class SolarRacing(Extension):

    @slash_command(name="hello", description="Say hey to the Club Bot!")
    async def hello(self, ctx: SlashContext):
        await ctx.send("Hey Solar Racing!")
    
    '''
        Sends a message as the bot

        ARGS:
            String : The message to send

        RETURNS:
            nada
    '''
    @slash_command(name="botsay", description="Have the bot send a custom message")
    @slash_option(
        name="message",
        description="what do you want to say?",
        required=True,
        opt_type=OptionType.STRING
    )
    async def bot_say(self, ctx: SlashContext, message: str = "GO SEAWOLVES!"):
        if not is_admin(ctx): return
        await ctx.channel.send(message)