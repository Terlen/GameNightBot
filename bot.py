import os

import discord
from discord.ext import commands, tasks
from discord.utils import get

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
    text = ctx.message.content
    


bot.run(TOKEN)