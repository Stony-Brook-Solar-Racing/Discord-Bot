# Imports
from interactions import Embed, EmbedField
from datetime import datetime
from zoneinfo import ZoneInfo

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

def print_tasks(tasks):
    embeds = []
    for t in tasks:
        embed = Embed( title=f"{t.get('SUMMARY')}" )
        embed.add_field("Due", f"{t.get('DUE')}")
        embed.add_field("Notes", f"{t.get('DESCRIPTION')}")
        embed.add_field("Status", f"{t.get('STATUS')}")
        embeds.append(embed)
    return embeds

# =================== Nextcloud Tasks Embeds ===========================
from pull_tasks import (
    ical_unescape, clamp,
    parse_due, humanize_due,
)

EMBED_COLOR_BY_STATUS = {
    "NEEDS-ACTION": 0xF1C40F,  # yellow
    "IN-PROCESS": 0x3498DB,  # blue
    "COMPLETED": 0x2ECC71,  # green
    "CANCELLED": 0x95A5A6,  # gray
}
STATUS_ORDER = {
    "NEEDS-ACTION": 0,
    "IN-PROCESS": 1,
    "": 2,   # unknown / missing
    "CANCELLED": 3,
    "COMPLETED": 4,   # push completed to the bottom
}

def _sort_key_for_task(task: dict, *, tz: str):
    status = (task.get("STATUS") or "").upper()
    bucket = STATUS_ORDER.get(status, 2)

    # parse due; put undated after dated
    due_params = task.get("_DUE_PARAMS") or {}
    due_raw = task.get("DUE")
    due_parsed, is_date_only = parse_due(due_raw, due_params, default_tz=tz)
    # normalize to a datetime for comparison (date-only -> midnight in tz)
    if due_parsed is None:
        due_key = (1, None)  # undated goes after dated
    else:
        if is_date_only:
            due_dt = datetime(due_parsed.year, due_parsed.month, due_parsed.day, 0, 0, tzinfo=ZoneInfo(tz))
        else:
            due_dt = due_parsed.astimezone(ZoneInfo(tz))
        due_key = (0, due_dt)

    summary = (task.get("SUMMARY") or "").lower()
    return (bucket, due_key, summary)

def _format_child_line(child: dict, *, tz: str) -> str:
    title = ical_unescape(child.get("SUMMARY")) or "(no summary)"
    status = (child.get("STATUS") or "").upper()
    due_params = child.get("_DUE_PARAMS") or {}
    due_raw = child.get("DUE")
    due_parsed, is_date_only = parse_due(due_raw, due_params, default_tz=tz)
    due_human = humanize_due(due_parsed, is_date_only, display_tz=tz) if due_parsed else (due_raw or "—")

    return f"• {clamp(title, 80)} — {clamp(due_human, 60)} — {status or 'UNKNOWN-STATUS'}"

def build_parent_task_embeds_grouped_by_list(by_uid: dict, children_of: dict, listname_of_uid: dict, *, tz: str = "America/New_York"):
    for uid, task in by_uid.items():
        p = task.get("_PARENT_UID")
        if p:
            task["_PARENT_LISTNAME"] = listname_of_uid.get(p)
            task["_PARENT_SUMMARY"] = (by_uid.get(p) or {}).get("SUMMARY")

    # Group UIDs by list
    from collections import defaultdict
    uids_by_list = defaultdict(list)
    for uid in by_uid.keys():
        uids_by_list[listname_of_uid.get(uid, "(unknown)")].append(uid)

    all_uids = set(by_uid.keys())

    embeds_by_list = {}

    for list_name, uids in uids_by_list.items():
        # parents = tasks in this list with no parent (or parent not present)
        parents = []
        for uid in uids:
            t = by_uid[uid]
            p = t.get("_PARENT_UID")
            if not p or p not in all_uids:
                parents.append(uid)

        # Build embeds
        embeds = []
        for puid in sorted(parents, key=lambda u: _sort_key_for_task(by_uid[u], tz=tz)):
            if parent.get("STATUS") != "COMPLETED":
                parent = by_uid[puid]
                child_uids = children_of.get(puid, [])
                children = [by_uid[cid] for cid in child_uids if cid in by_uid]
                embeds.append(build_parent_task_embed(parent, children, tz=tz))

        embeds_by_list[list_name] = embeds

    return embeds_by_list

def build_parent_task_embed(parent: dict, children: list[dict], *, tz: str = "America/New_York") -> Embed:
    status = (parent.get("STATUS") or "NEEDS-ACTION").upper()
    color  = EMBED_COLOR_BY_STATUS.get(status, 0x7289DA)

    emb = Embed(color=color)

    parent_uid = parent.get("_PARENT_UID")
    if parent_uid and parent_uid not in ():
        p_name  = parent.get("_PARENT_SUMMARY") or parent_uid
        p_list  = parent.get("_PARENT_LISTNAME")
        sub_val = f"{p_name} — {p_list}" if p_list else p_name
        emb.add_field(name="Subtask of", value=clamp(sub_val, 1024), inline=False)

    title = ical_unescape(parent.get("SUMMARY")) or "(no summary)"
    emb.add_field(name="Task", value=clamp(title, 1024), inline=False)

    p_due_params = parent.get("_DUE_PARAMS") or {}
    p_due_raw = parent.get("DUE")
    p_due_parsed, p_is_date_only = parse_due(p_due_raw, p_due_params, default_tz=tz)
    p_due_human = humanize_due(p_due_parsed, p_is_date_only, display_tz=tz) if p_due_parsed else (p_due_raw or "—")
    notes = ical_unescape(parent.get("DESCRIPTION"))
    if notes:
        emb.add_field(name="Notes", value=clamp(notes, 1024), inline=False)

    emb.add_field(name="Due Date", value=clamp(p_due_human, 1024), inline=True)

    emb.add_field(name="Status", value=status, inline=True)

    if children:
        children_sorted = sorted(children, key=lambda c: _sort_key_for_task(c, tz=tz))
        lines = []
        hidden = 0
        current_len = 0
        for ch in children_sorted:
            line = _format_child_line(ch, tz=tz)
            extra = len(line) + (1 if lines else 0)
            if current_len + extra > 1024:
                hidden += 1
                continue
            lines.append(line)
            current_len += extra
        if hidden:
            tail = f"\n… +{hidden} more"
            if current_len + len(tail) <= 1024:
                lines.append(tail)
        emb.add_field(name="Subtasks", value="\n".join(lines) if lines else "—", inline=False)

    list_name = parent.get("_LISTNAME") or "(unknown list)"
    emb.set_footer(text=f"{list_name} • Nextcloud Tasks")
    return emb
# ======================================================================
