from asyncio import sleep
import json
from random import choice, randint, shuffle

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
        damage_moves = ["{attacker} sends out their army of doggos at {defender}, dealing {amount} damage",
                        "{attacker} conjures the mighty sharknado, dealing {amount} damage to {defender}",
                        "{attacker} busts out the ultimate attack, and tickles {defender}, this results in {amount} damage",
                        "While {attacker} takes a Beat Saber break, they accidentally hit {defender} and deal {amount} damage",
                        "{attacker}"
                        ]
        # All the possible healing moves
        # TODO: Add more healing moves
        healing_moves = ["Instead of attacking, {target} uses magical unicorn piss to heal themselves for {amount} HP",
                         "Using the power of friendship and bonds, {target} gets back on their feet and heals for {amount} HP"
                         ]

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
        for _ in range(0, 3):

            # One round consists of each player attacking and
            for attacker, defender in order:

                # Will this be a healing or attack turn?
                will_attack = choice([True, False])

                damage_or_heal_amount = randint(2, 8)
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
        winner = player_one if player_one.health > player_two.health else player_two
        loser = player_one if winner == player_two else player_two

        # Load win/loss data
        data = json.loads(open("assets/config.json", "r").read())
        member_data = data[str(ctx.message.guild.id)]["members"]

        # Update win/loss counts
        member_data[str(winner.id)]["win"] += 1
        member_data[str(loser.id)]["loss"] += 1

        # Save to variables
        winner_stats = [member_data[str(winner.id)]["win"], member_data[str(winner.id)]["loss"]]
        loser_stats = [member_data[str(loser.id)]["win"], member_data[str(loser.id)]["loss"]]

        # Save new win/loss count
        json.dump(data, open('assets/config.json', 'w'), indent=2, separators=(',', ': '))

        # Send who won, and stats
        await ctx.send(f"The winner is: {winner.name}. Final stats: {player_one.name}: {player_one.health}, {player_two.name}: {player_two.health}")
        await ctx.send(f"{winner.name} has: {winner_stats[0]} wins and {winner_stats[1]} losses. {loser.name} has: {loser_stats[0]} wins and {loser_stats[1]} losses.")


def setup(bot):
    bot.add_cog(Fun(bot))
