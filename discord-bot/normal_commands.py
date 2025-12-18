import embeds
from interactions import (
    Extension,
    SlashContext,
    slash_command,
    slash_option,
    OptionType,
    Embed,
)
from solardb import solardb


class NonAdmin(Extension):
    @slash_command(name="peoplein", description="send an embed of who's in the shop")
    async def peoplein(self, ctx: SlashContext):
        names = solardb().people_in_names()
        shop_embed = embeds.get_people_in_shop(names)
        await ctx.send(embed=shop_embed)

    @slash_command(
        name="leaderboard", description="send an embed of the leaderboard of times"
    )
    async def leaderboard(self, ctx: SlashContext):
        people = solardb().get_leaderboard()
        shop_embed = embeds.get_leaderboard(people)
        await ctx.send(embed=shop_embed)

    @slash_command(name="task", description="Manage tasks")
    async def tasks_base(self, ctx=None):
        pass

    @tasks_base.subcommand(sub_cmd_name="show", sub_cmd_description="View all tasks")
    async def view_tasks(self, ctx: SlashContext):
        tasks = solardb().get_tasks()
        tasks_dict = {}
        for task in tasks:
            id, category, content, is_complete = task
            if not category:
                category = "Miscellaneous"
            if category not in tasks_dict:
                tasks_dict[category] = [];
            tasks_dict[category].append((id, content, is_complete))

        embed = Embed(title="Tasks")
        for category, tasks in tasks_dict.items():
            tasks_text = ""
            for task in tasks:
                id, content, is_complete = task
                check_text = ":white_check_mark:" if is_complete else ":x:"
                tasks_text += f"{id}. {check_text} {content}\n"
            embed.add_field(name=category, value=tasks_text)

        await ctx.send(embed=embed)

    @tasks_base.subcommand(sub_cmd_name="purge", sub_cmd_description="Delete complete tasks")
    async def purge_tasks(self, ctx: SlashContext):
        solardb().purge_tasks()
        await ctx.send("Purged tasks.")

    @tasks_base.subcommand(sub_cmd_name="complete", sub_cmd_description="Complete task")
    @slash_option(
        name="id",
        description="id of the task you want to complete",
        required=True,
        opt_type=OptionType.INTEGER
    )
    async def complete_task(self, ctx: SlashContext, id):
        solardb().complete_task(id)
        await ctx.send(f"Completed task {id}!")
