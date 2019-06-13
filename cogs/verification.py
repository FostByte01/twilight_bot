import json
from random import choices

from discord.ext import commands
import discord.utils


config = json.loads(open('config.json', 'r').read())


class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def create_verification(self, ctx):
        """Create roles necessary for the verification system to work"""
        if config[ctx.guild.name]['verification_enabled']:
            await ctx.guild.create_role(name="Unverified")
            channel = await ctx.guild.create_text_channel("Verification")
            config[ctx.guild.name]['verification_channel'] = channel.id
            json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '), sort_keys=True)
            await ctx.message.add_reaction(u"\U0001F44D")
        else:
            await ctx.send("This server does not have verification enabled, please enable it first")

    @commands.command(pass_context=True)
    @commands.check(lambda ctx: ctx.message.channel.id == config[ctx.guild.name]['verification_channel'])
    async def verify(self, ctx):
        words = ['shy', 'property', 'quack', 'half',
                 'hair', 'zebra', 'sneeze', 'mist',
                 'dinosaurs', 'nippy', 'overjoyed', 'imported',
                 'protect', 'fairies', 'sticks', 'empty',
                 'ill', 'road', 'screw', 'annoyed']
        random_phrase = ' '.join(choices(words, k=3))
        await ctx.message.author.send(f"Please reply with the following phrase: {random_phrase}")
        await self.bot.wait_for("message", timeout=30, check=lambda message: message.content == random_phrase)
        await ctx.message.author.send(f"Verification complete 👍")
        role = discord.utils.get(ctx.guild.roles, name="Unverified")
        await ctx.message.author.remove_roles(role)


def setup(bot):
    bot.add_cog(Verification(bot))