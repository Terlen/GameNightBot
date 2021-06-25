import os

import discord
from discord.ext import commands, tasks
from discord.utils import get

import records
import gameHistory
import reactionHandler as react

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
    #print(bot.guilds)
    #print(GUILD)
    #guild = discord.utils.get(bot.guilds, id=GUILD)
    #print(guild)
    print(
        f'{bot.user} has connected to the Discord guilds:\n'
        f'{bot.guilds}'
        )
    
    #members = '\n - '.join([member.name for member in guild.members])
    #print(members)
    #print(f'Guild Members:\n - {members}')

# listen for reactions being added to bot messages and handle the event
@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if (payload.user_id != bot.user.id):
        pass
        reactionGuild = discord.utils.get(bot.guilds, id=payload.guild_id)
        reactionChannel = discord.utils.get(reactionGuild.text_channels, id=payload.channel_id)
        reactionMessage = await reactionChannel.fetch_message(payload.message_id)
        if reactionMessage.author.id == bot.user.id:
            if payload.emoji.name == '\u274c' or payload.emoji.name == '\u2705':
                # verification logic/function
                pass

# Define command to have bot fetch the user who is picking the next game and the date they are picking for.
@bot.command()
async def whosnext(ctx):
    nextMemberData = records.loadNextChoice()
    memberID = nextMemberData[0]
    nextDate = nextMemberData[1]
    guild = discord.utils.get(bot.guilds, id=GUILD)
    nextMember = discord.utils.get(guild.members, id=memberID)
    await ctx.send(f"The person choosing the next game is {nextMember.display_name}! We'll be playing their game on {nextDate}.")
    
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

@bot.command()
async def addGame(ctx):
    commandText = ctx.message.content.split()
    if len(commandText) > 3:
        commandText = ctx.message.content.split("\"")
    if len(commandText) == 3:
        gameHistory.dbAddGameRecord(commandText[1],ctx.message.mentions[0].id)
        await ctx.send(f"Alright, {commandText[1]} was added to our play history! Hope it was a good choice {ctx.message.mentions[0].name}!")
    else:
        await ctx.send(f"Invalid command. Make sure you're quoting if there are spaces in the name! (For example: \"The Game of Life\")")
    
@bot.command()
async def addPlayer(ctx):
    commandText = ctx.message.content.split()
    if len(commandText) == 2:
        gameHistory.dbAddPlayerRecord(ctx.message.mentions[0].id, ctx.message.mentions[0].name)
        await ctx.send(f"Alright, player {ctx.message.mentions[0].name} has been recorded!")

@bot.command()
async def mercy(ctx):
    commandText = ctx.message.content.split()
    await ctx.send(f"I am not a merciful god, but this indiscretion shall be allowed.")

bot.run(TOKEN)