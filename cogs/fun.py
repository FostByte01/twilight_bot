from random import choice, randint, shuffle
from asyncio import sleep

from discord.ext import commands
from discord import Member

# Class to keep track of health for duel command
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

        # Define possible responses
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
        # Pick random response and send it
        await ctx.send(f'{choice(responses)} {ctx.message.author.mention}')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """Flip a coin"""
        # Randomly choose heads or tails and send it
        await ctx.send(f'{ctx.message.author.mention}, I got {choice(["heads", "tails"])}')

    @commands.command(pass_context=True)
    async def duel(self, ctx, enemy: Member):
        await ctx.send(f"{ctx.message.author.name} challenges {enemy.name} to a duel!")

        # All the possible attack moves
        # TODO: Add more attacks
        damage_moves = ["Damage dealt by {attacker}, applied to {defender}, amount {amount}"]
        # All the possible healing moves
        # TODO: Add more healing moves
        healing_moves = ["{target} healed for {amount} "]

        # Create duelist objects for both players
        player_one = Duelist(ctx.message.author)
        player_two = Duelist(enemy)
        # Order the players will attack, will be randomly shuffled to pick who goes first
        order = [(player_one, player_two), (player_two, player_one)]
        shuffle(order)
        await sleep(1)
        await ctx.send(f"By random chance: {order[0][0].name} will be going first")
        await sleep(1)

        # Duels have 5 rounds
        for _ in range(0, 5):

            # One round consists of each player attacking and
            for attacker, defender in order:

                # Will this be a healing or attack turn?
                will_attack = choice([True, False])

                damage_or_heal_amount = randint(1, 8)
                if will_attack:
                    # Pick random attack move and send it in chat, then deal damage to defender
                    await ctx.send(choice(damage_moves).format(attacker=attacker.name, defender=defender.name, amount=damage_or_heal_amount))

                    defender.damage(damage_or_heal_amount)
                else:
                    # Pick random healing move and send it in chat, then add that amount of health to attacker
                    await ctx.send(choice(healing_moves).format(target=attacker.name, amount=damage_or_heal_amount))

                    attacker.heal(damage_or_heal_amount)
            await sleep(1)
        await(sleep(1))

        # Winner is player with more HP at the end
        winner = player_one.name if player_one.health > player_two.health else player_two

        # Say who won
        await ctx.send(f"The winner is: {winner}. Final stats: {player_one.name}: {player_one.health}, {player_two.name}: {player_two.health}")

        # TODO: Keep track of wins/losses

def setup(bot):
    bot.add_cog(Fun(bot))
