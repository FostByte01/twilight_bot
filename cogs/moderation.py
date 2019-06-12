from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge', 'remove'], pass_context=True)
    async def clear(self, ctx, count: int):
        """Clear the specified amount of messages"""
        await ctx.channel.purge(limit=count+1)


def setup(bot):
    bot.add_cog(Moderation(bot))
