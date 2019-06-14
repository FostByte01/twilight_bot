import datetime
import json
import os

from discord import Embed
from discord.ext import commands
import discord.utils

bot = commands.Bot(command_prefix="t!")

config = json.loads(open('config.json', 'r').read())


@bot.event
async def on_ready():
    print("Twilight bot initialized and ready")
    print(f"User: {bot.user}")


@bot.event
async def on_member_join(member):
    if config[member.guild.name]['verification_enabled']:
        role = discord.utils.get(member.guild.roles, name="Unverified")
        await member.add_roles(role)

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
    if message.guild is None:
        await bot.process_commands(message)
        return
    if message.author != bot.user:
        verify_channel = config[message.guild.name]['verification_channel']
        if message.content != 't!verify' and message.channel.id == verify_channel:
            await message.channel.purge(limit=1)
        unverified_role = discord.utils.get(message.author.guild.roles, name="Unverified")
        if unverified_role in message.author.roles and message.content != "t!verify":
            await message.channel.purge(limit=1)
            await message.author.send("You have not verified your account, please type 't!verify' in your servers verification channel")
    await bot.process_commands(message)

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(config['token'])
