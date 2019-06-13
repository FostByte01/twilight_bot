from discord.ext import commands
from asyncio import sleep


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge', 'remove'], pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        """Clear the specified amount of messages"""
        await ctx.channel.purge(limit=count+1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions to do that!")
            await sleep(2)
            await ctx.channel.purge(limit=2)


def setup(bot):
    bot.add_cog(Moderation(bot))
