# Imports
from interactions import Embed, EmbedField

"""

the following code is an example of creating a paginator.
requires the
from interactions.ext.paginators import Paginator
import, and probably a few others

this following code kinda has to be in bot.py? question mark?
cus of the bot parameter i create_from_embeds?
probably a way around it in the docs

# Create an Embeds booklet which can be flipped through
rules_embeds = embeds.getRulesEmbeds()
rules_paginator = Paginator.create_from_embeds(bot, *rules_embeds)

@slash_command(name="rules", description="Clubs have rules to follow!")
async def rules(ctx: SlashContext):
    await rules_paginator.send(ctx)

"""

"""
    This file (embeds.py) will store all embed information
    that needs to be sent out by the bot. Can return one embed,
    or an array of embeds, depending on your use case.

    Usage:
        from embeds import getTestEmbeds
"""

def getShopHoursEmbed(type, plan, estimated_time, sessionNumber):
    embed = Embed(
        color = 0x00FFFF,
        title = f'SHOP OPEN (Session #{sessionNumber})',
        fields=[
            EmbedField(
                name = 'Shop Type',
                value = f'{type}',
                inline = True
            ),
            EmbedField(
                name = 'Rough Plan',
                value = f'{plan}',
                inline = True
            ),
            EmbedField(
                name = 'Estimated Time',
                value = f'{estimated_time}',
                inline = True
            )
        ]
    )
    return embed

def getShopHoursClosedEmbed():
    embed = Embed(
        color = 0x00FFFF,
        title = f'SHOP CLOSED',
        fields=[
            EmbedField(
                name = 'goodbye. come back next time. we\'ll miss you.',
                value ='👋'
            )
        ]
    )
    return embed

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

    # Images for embeds need to be set like this, obv pointing to an image.
    embeds[0].set_image(url="https://google.com")

    return embeds

"""
    The rules Embed so club members behave.

    Args: No Args

    Returns:
        Embed array with a single embed
"""
def getRulesEmbeds():
    color = 0xF8E71C
    embeds = [

        Embed(
            title="Respect Others",
            description = "Be respectful and civil to others in conversation. Do not make comments considered mean, rude, harassing, insulting, or instigative.",
            color=color
        ),

        Embed(
            title="Be Inclusive",
            description="We will not allow discrimination or hazing in any form on this server. Be reasonable in understanding these rules.",
            color=color
        ),

        Embed(
            title="Keep Profanity to a Minimum",
            description="Swearing is a form of expressing human emotion, and we will not stop you from expressing those emotions, but please try to refrain from using it openly. Any derogatory language directed at others will not be tolerated.",
            color=color
        ),

        Embed(
            title="Appropriate Content Only",
            description="Content that is considered “Not Safe For Work” including links to such NSFW content is not allowed anywhere in the server.",
            color=color
        ),

        Embed(
            title="Do Not Spam Messages",
            description="Many messages sent in short succession meant to disrupt normal server usage and operation will not be tolerated.",
            color=color
        ),

        Embed(
            title="No Academic Dishonesty",
            description="Do not discuss details of examinations or assignments on this server. We condone independent work, but we won’t attend your academic dishonesty trial. Follow the University Academic Integrity Policy.",
            color=color
        ),

        Embed(
            title="Properly Identify Yourself",
            description="Please change your Discord nickname so that we can identify you. Offensive nicknames and profile pictures as well as falsely assuming another’s identity will not be tolerated.",
            color=color
        ),

        Embed(
            title="Do Not Endanger Other Members or their Property",
            description="Sending links or files for malware, sharing private information of others without their consent, or otherwise threatening the safety of members or property will not be tolerated.",
            color=color
        ),

        Embed(
            title="E-Board Makes the Decisions",
            description="The E-Board will decide appropriate actions for unruly users, and maintains the right to change the rules at any time.",
            color=color
        ),

        Embed(
            title="Advertise only with Permission",
            description="Promoting events or other clubs on campus should be done only with the approval of the E-Board. Unapproved adverts in the server will be deleted.",
            color=color
        ),


    ]

    return embeds

def concat_name(name):
    return name[0]+" "+name[1]

# Embed for people in Shop
def get_people_in_shop(names):
    names = map(concat_name, names)
    embed = Embed(
        title="Who's in the shop?",
        description='\n'.join(names)
        # description="names"
    )

    return embed

# Embed for leaderboard
def get_leaderboard(people):
    names = "";
    times = "";
    count = 1;
    for person in people:
        names += str(count)+" "+person[0]+" "+person[1]+"\n";
        if(person[2].total_seconds()/3600 > 1):
            hours = person[2].total_seconds()/3600;
            mins = (person[2].total_seconds()/60)%60;
            times += str(int(hours))+"h "+str(int(mins))+"m\n";
        else:
            times += str(int(person[2].total_seconds()/60))+"m\n";
        count+=1
    embed = Embed( title="Leaderboard" );
    embed.add_field("Name", names , True);
    embed.add_field("Time(Mins)", times, True);
    embed.add_field("Sign out if you want time!!!", " ")
    return embed;
