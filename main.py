import datetime
import json
import os

from discord import Embed
from discord.ext import commands

bot = commands.Bot(command_prefix="t!")

config = json.loads(open('config.json', 'r').read())


@bot.event
async def on_ready():
    print("Twilight bot initialized and ready")
    print(f"User: {bot.user}")


@bot.event
async def on_member_join(member):
    embed = Embed(color=0x9370DB, description=f'Welcome to the server! You are member number {len(list(member.guild.members))}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    channel = bot.get_channel(id=config[member.guild.name]['join_leave_channel'])

    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    embed = Embed(color=0x9370DB, description=f'Goodbye! Thank you for spending time with us!')
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

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(config['token'])
