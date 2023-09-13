# Imports
import interactions
from interactions import Embed, Extension, File, OptionType, SlashCommandChoice, check, slash_command, slash_option
from interactions import slash_command, SlashContext
import helpers
import embeds
import json
import os

class SolarRacing(Extension):

    @slash_command(name="sendrules", description="send a full list of rules")
    async def sendrules(self, ctx: SlashContext):
        if not helpers.is_admin(ctx): return
        rules_array = embeds.getRulesEmbeds()
        for rule in rules_array:
            ctx.send(rule)
    

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
        if not helpers.is_admin(ctx): return
        if not helpers.is_tester(ctx): return
        await ctx.channel.send(message)