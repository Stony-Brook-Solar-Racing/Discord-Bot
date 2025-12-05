import embeds
from interactions import (
    Extension,
    SlashContext,
    slash_command,
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

    # @slash_command(name="todo add", description="add todos in markdown bullet format")
    # async def add_todos(self, ctx: SlashContext):
    #     # Take the user's next message, and add those as todos
    #     generate_todos(ctx.content)
    #     await ctx.send(embed=embed)
    #
    # @slash_command(name="todo check", description="add todos")
    # async def check_todo(self, ctx: SlashContext):
    #     await ctx.send(embed=embed)
    #
    # @slash_command(name="todo remove", description="remove all completed todos")
    # async def remove_todos(self, ctx: SlashContext):
    #     await ctx.send(embed=embed)
