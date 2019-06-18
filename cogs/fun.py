from random import choice, randint
from asyncio import sleep

from discord.ext import commands
from discord import Member


class Fun(commands.Cog):

    def __init__(self, bot):
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

    @commands.command(pass_context=True)
    async def duel(self, ctx, enemy: Member):
        await ctx.send(f"{ctx.message.author.name} challenges {enemy.name} to a duel!")
        damage_moves = ["Damage dealt by {attacker}, applied to {defender}, amount {amount}"]
        healing_moves = ["{attacker} healed for {amount} "]
        author_health, enemy_health = 20, 20
        winner = None
        for turn in range(1, 5):
            if author_health <= 0 or enemy_health <= 0:
                break
            elif turn % 2 == 0:
                damage = randint(1, 5)
                await ctx.send(f"{choice(damage_moves).format(attacker=ctx.message.author.name, defender=enemy.name, amount=damage)}")
                enemy_health -= damage
            else:
                damage = randint(1, 5)
                await ctx.send(f"{choice(damage_moves).format(defender=ctx.message.author.name, attacker=enemy.name, amount=damage)}")
                author_health -= damage
            await sleep(1)
        await ctx.send(f"Final results {ctx.message.author.name}: {author_health}HP, {enemy.name}: {enemy_health}HP")

def setup(bot):
    bot.add_cog(Fun(bot))