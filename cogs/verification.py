import json
from random import choices
import aiohttp

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
        if config[ctx.guild.id]['verification_enabled']:
            await ctx.guild.create_role(name="Unverified")
            channel = await ctx.guild.create_text_channel("Verification")
            config[ctx.guild.id]['verification_channel'] = channel.id
            json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '), sort_keys=True)
            await ctx.message.add_reaction(u"\U0001F44D")
        else:
            await ctx.send("This server does not have verification enabled, please enable it first")

    @commands.command(pass_context=True)
    @commands.check(lambda ctx: ctx.message.channel.id == config[ctx.guild.id]['verification_channel'])
    async def verify(self, ctx):
        async with aiohttp.ClientSession() as client:
            async with client.get("https://www.mit.edu/~ecprice/wordlist.10000") as response:
                text = await response.text()
                words = text.splitlines()
            await client.close()
        random_phrase = ' '.join(choices(words, k=3))
        await ctx.message.author.send(f"Please reply with the following phrase: {random_phrase}")
        await self.bot.wait_for("message", timeout=30, check=lambda message: message.content == random_phrase)
        await ctx.message.author.send(f"Verification complete 👍")
        role = discord.utils.get(ctx.guild.roles, name="Unverified")
        await ctx.message.author.remove_roles(role)


def setup(bot):
    bot.add_cog(Verification(bot))