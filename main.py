from random import choice
import datetime
import json

from discord import Embed
from discord.ext import commands

bot = commands.Bot(command_prefix="t!")

config = json.loads(open('config.json', 'r').read())


@bot.event
async def on_ready():
    print("Twilight bot initialized and ready")
    print(f"User: {bot.user}")


@bot.event
async def on_ready():
    print("Twilight bot initialized and ready")
    print(f"User: {bot.user}")

@bot.event
async def on_member_join(member):
    embed = Embed(color=0xbada55, description=f'Welcome to the server! You are member number {len(list(member.guild.members))}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    channel = bot.get_channel(id=config[member.guild.name]['join_leave_channel'])

    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    embed = Embed(color=0xbada55, description=f'Goodbye! Thank you for spending time with us!')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    channel = bot.get_channel(id=config[member.guild.name]['join_leave_channel'])

    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(f"Message Sent: {message.author}: {message.content}")
    await bot.process_commands(message)


@bot.command(aliases=['8ball'], pass_context=True)
async def _8ball(ctx):
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


@bot.command(pass_context=True)
async def flip(ctx):
    """Flip a coin"""
    await ctx.send(f'{ctx.message.author.mention}, I got: {choice(["heads", "tails"])}')


@bot.command(pass_context=True)
async def ping(ctx):
    """Test command"""
    await ctx.send(f'Pong! {ctx.message.author.mention}')


bot.run(config['token'])
