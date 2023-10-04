# Imports
import interactions
from interactions import Button, Embed, Extension, File, OptionType, SlashCommandChoice, check, slash_command, slash_option, ButtonStyle
from interactions import slash_command, SlashContext
import helpers, embeds

# This file contains the following slash commands:
# (ADMIN) sendrules - has the bot send out embeded list of rules
# (ADMIN) botsay - has the bot say anything
# 

class SolarRacing(Extension):

    @slash_command(name="openshop", description="send an embed to describe your shop hours")
    @slash_option(
        name="type",
        description="what kind of hours are these?",
        required=False,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="plan",
        description="what is this shop centered around?",
        required=False,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="time",
        description="how long do you plan to stay?",
        required=False,
        opt_type=OptionType.STRING
    )
    async def openshop(self, ctx:SlashContext, type = "General", plan = "N/A", time = "N/A"):
        if not helpers.is_admin(ctx): return
        shop_embed = embeds.getShopHoursEmbed(type, plan, time)
        await ctx.send(embed=shop_embed)

    '''
        Sends out an embeded list of rules

        ARGS:
            nada

        RETURNS:
            nada
    '''
    @slash_command(name="sendrules", description="send a full list of rules")
    async def sendrules(self, ctx: SlashContext):
        if not helpers.is_admin(ctx): return
        rules_array = embeds.getRulesEmbeds()
        for rule in rules_array:
            pass
            await ctx.channel.send(embed=rule)
        
        embed = Embed(
            title="Follow Discord’s Rules",
            description="Abide by the Discord Terms of Service and Guidelines.",
            color= 0xF8E71C
        )
        
        components = [
            Button(
                style = ButtonStyle.URL,
                label = "Terms of Service",
                url = "https://discord.com/terms"
            ),
            Button(
                style = ButtonStyle.URL,
                label = "Guidelines",
                url = "https://discord.com/guidelines"
            )
        ]
        
        
        # send the discord TOS and guidelines
        await ctx.channel.send(embed=embed, components=components)
    
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
        if not helpers.verify_access(ctx): return
        await ctx.channel.send(message)