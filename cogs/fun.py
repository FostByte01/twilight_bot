from random import choice

from discord.ext import commands


class Fun(commands.Cog):

    def __init(self, bot):
        self.bot = bot

    @commands.command(name="8ball", pass_context=True)
    async def _8ball(self, ctx):
        """Ask the magic 8 ball"""
        responses = ['It is certain',
                     'It is decidedly so',
                     'Without a doubt',
                     'Yes - definitely',
                     'You may rely on it',
                     'As I see it, yes',
                     'Most likely',
                     'Outlook is good',
                     'Yes',
                     'Signs indicate yes',
                     'Reply hazy, try again',
                     'Ask again later',
                     'Better not tell you now',
                     'I can\'t give a prediction at this time',
                     'Concentrate and ask again later',
                     'Don\'t count on it',
                     'No',
                     'My sources say no',
                     'Outlook is not so good',
                     'Very doubtful']
        await ctx.send(f'{choice(responses)} {ctx.message.author.mention}')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """Flip a coin"""
        await ctx.send(f'{ctx.message.author.mention}, I got {choice(["heads", "tails"])}')


def setup(bot):
    bot.add_cog(Fun(bot))