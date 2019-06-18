from random import choice, randint, shuffle
from asyncio import sleep

from discord.ext import commands
from discord import Member


class Duelist:
    def __init__(self, member: Member):
        self.member = member
        self.health = 20
        self.name = member.name
        self.id = member.id

    def heal(self, amount):
        self.health += amount

    def damage(self, amount):
        self.health -= amount


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
        healing_moves = ["{target} healed for {amount} "]
        player_one = Duelist(ctx.message.author)
        player_two = Duelist(enemy)
        order = [(player_one, player_two), (player_two, player_one)]
        shuffle(order)
        await sleep(1)
        await ctx.send(f"By random chance: {order[0][0].name} will be going first")
        await sleep(1)
        for _ in range(0, 5):
            for attacker, defender in order:
                will_attack = choice([True, False])
                damage_or_heal_amount = randint(1, 8)
                if will_attack:
                    await ctx.send(choice(damage_moves).format(attacker=attacker.name, defender=defender.name, amount=damage_or_heal_amount))
                    defender.damage(damage_or_heal_amount)
                else:
                    await ctx.send(choice(healing_moves).format(target=attacker.name, amount=damage_or_heal_amount))
                    attacker.heal(damage_or_heal_amount)
            await sleep(1)
        await(sleep(1))
        winner = player_one.name if player_one.health > player_two.health else player_two.name
        await ctx.send(f"The winner is: {winner}. Final stats: {player_one.name}: {player_one.health}, {player_two.name}: {player_two.health}")





def setup(bot):
    bot.add_cog(Fun(bot))
