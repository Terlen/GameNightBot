import os

import discord
from discord.ext import commands, tasks
from discord.utils import get

import records

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix = '!', intents=intents)

#print(TOKEN)
#client = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(bot.guilds)
    print(GUILD)
    guild = discord.utils.get(bot.guilds, id=GUILD)
    print(guild)
    print(
        f'{bot.user} has connected to the Discord guild:\n'
        f'{guild.name}(id: {guild.id})'
        )
    
    members = '\n - '.join([member.name for member in guild.members])
    #print(members)
    print(f'Guild Members:\n - {members}')

@bot.command()
async def turn(ctx):
    await ctx.send("Hello!")

@bot.command()
async def setTurn(ctx):
    nextDate = records.nextGameNight()
    textPhrases = ctx.message.content.split()
    if len(textPhrases) == 1:
        records.saveNextChoice(ctx.author.id, nextDate)
        await ctx.send(f'Alright, you\'re picking the game next time {ctx.author.name}! The next game night is {nextDate}.')
    elif len(textPhrases) == 2:
        try:
            user = ctx.message.mentions[0]
            records.saveNextChoice(user.id, nextDate)
            await ctx.send(f'Looks like {user.name}\'s picking next time! The next game night is {nextDate}.')
        except:
            await ctx.send("Invalid command input")
    else:
        await ctx.send("Invalid command input, please use format \"!setTurn <@usermention>\" OR just use \"!setTurn\" (For example: !setTurn @Terlen OR !setTurn to set yourself)")

    


bot.run(TOKEN)