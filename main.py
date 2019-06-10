from random import choice

from discord.ext import commands

bot = commands.Bot(command_prefix="t!")


@bot.event
async def on_ready():
    print("Twilight bot initialized and ready")
    print(f"User: {bot.user}")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(f"Message Sent: {message.author}: {message.content}")
    await bot.process_commands(message)


@bot.command(aliases=['8ball'], pass_context=True)
async def _8ball(ctx):
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
    await ctx.send(choice(responses))


@bot.command(pass_context=True)
async def flip(ctx):
    await ctx.send(f'{ctx.message.author.mention}, I got: {choice(["heads", "tails"])}')


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'Pong! {ctx.message.author.mention}')


bot.run(open("token.txt", "r").read())
