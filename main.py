import datetime
import json
import os

from discord.ext import commands
from discord import Embed
import discord.utils

bot = commands.Bot(command_prefix="t!")

config = json.loads(open('config.json', 'r').read())


@bot.event
async def on_ready():
    print("Twilight bot initialized and ready")
    print(f"User: {bot.user}")
    # Check if there are any new servers the bot does not have configs for
    for server in bot.guilds:
        if str(server.id) not in config:
            # Add empty config to JSON + initialize all win/loss stats for users
            config[server.id] = {
                "verification_channel": None,
                "verification_enabled": False,
                "members": {
                    str(member.id): {"win": 0, "loss": 0} for member in server.members
                }
            }
            # Save to config file
            json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_member_join(member):
    # Add unverified role to user if the server has verification enabled
    if config[str(member.guild.id)]['verification_enabled']:
        role = discord.utils.get(member.guild.roles, name="Unverified")
        await member.add_roles(role)

    # Prepare welcome embed
    embed = Embed(color=0x9370DB, description=f'Welcome to the server! You are member number {len(list(member.guild.members))}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    # Get the server message channel and send welcome message there
    channel = bot.get_channel(id=member.guild.system_channel.id)

    await channel.send(embed=embed)

    # Initialize user data to JSON file
    config[str(member.guild.id)]["members"].update({str(member.id): {"win": 0, "loss": 0}})
    json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_member_remove(member):
    # Prepare goodbye embed
    embed = Embed(color=0x9370DB, description=f'Goodbye! Thank you for spending time with us!')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    # Get the server message channel and send goodbye message there
    channel = bot.get_channel(id=member.guild.system_channel.id)

    await channel.send(embed=embed)

    # Remove user data from JSON file
    config[str(member.guild.id)]["members"].pop(str(member.id))
    json.dump(config, open('config.json', 'w'), indent=2, separators=(',', ': '))


@bot.event
async def on_message(message):
    # Do not handle on message event if in DM
    if message.guild is None:
        await bot.process_commands(message)
        return
    if message.author != bot.user:
        # Check if the user is attempting to verify, if not then delete the message and send them a notice in DM
        verify_channel = config[str(message.guild.id)]['verification_channel']
        if message.content != 't!verify' and message.channel.id == verify_channel:
            await message.channel.purge(limit=1)
        unverified_role = discord.utils.get(message.author.guild.roles, name="Unverified")
        if unverified_role in message.author.roles and message.channel.id != verify_channel:
            await message.channel.purge(limit=1)
            await message.author.send("You have not verified your account, please type 't!verify' in your servers verification channel")

    # Continue processing all other commands
    await bot.process_commands(message)

# Recursively load all cogs
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

# Bring the bot online
bot.run(config['token'])
