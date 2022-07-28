import os
import discord
from discord.ext import commands, tasks
from discord.utils import get

import utils.records as records
import utils.database as database
import utils.reactionHandler as react
from utils.messages import verifyMessage, pendingVerify, Verification

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
    
    for guild in bot.guilds:
        pendingVerify[guild.id] = []
        try:
            database.databaseConnections[guild.id] = database.dbConnect(guild.id)
        except database.sqlite3.OperationalError:
            database.databaseConnections[guild.id] = database.initializeDatabase(guild.id)
        
    #members = '\n - '.join([member.name for member in guild.members])
    #print(members)
    #print(f'Guild Members:\n - {members}')

# listen for reactions being added to bot messages and handle the event
@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    # Ignore bot generated reactions
    if (payload.user_id != bot.user.id):
        #pass
        reactionGuild = discord.utils.get(bot.guilds, id=payload.guild_id)
        reactionChannel = discord.utils.get(reactionGuild.text_channels, id=payload.channel_id)
        reactionMessage = await reactionChannel.fetch_message(payload.message_id)
        # Respond to reactions to bot messages
        if reactionMessage.author.id == bot.user.id:
            
            for item in pendingVerify[reactionGuild.id]:
                if payload.user_id == item.commandRequest.author.id and reactionMessage == item.verifyMessage:
                    # Red X or Green Check emojis used by bot verification messages
                    if payload.emoji.name == '\u274c':
                        pass 
                    elif payload.emoji.name == '\u2705':
                        # verification logic/function
                        #await reactionMessage.channel.send("Yay!")
                        await addGameVerified(reactionMessage.channel,item.game, item.suggestor)
                    break

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
        # Order bot to create a verification message
        addRequest = Verification(ctx)
        addRequest.game = commandText[1]
        addRequest.suggestor = ctx.message.mentions[0]
        await verifyMessage(addRequest,operation="add",game=addRequest.game)
    else:
        await ctx.send(f"Invalid command. Make sure you're quoting if there are spaces in the name! (For example: \"The Game of Life\")")

async def addGameVerified(channel, game, member):
    dbConnection = database.databaseConnections[channel.guild.id]
    dbCursor = dbConnection.cursor()
    with dbConnection:
        try:
            database.addGame(dbCursor, game, member)
            await channel.send(f"Alright, {game} was added to our play history! Hope it was a good choice {member.name}!")
        # Foreign key mismatches show up as OperationalErrors instead of Integrity Errors as I expected, so we'll have to handle it here I guess
        except database.sqlite3.OperationalError as exception:
            if str(exception).split(' - ')[0] == 'foreign key mismatch':
                await channel.send(f"{member.name} isn't in the database yet, please add them via !addPlayer first then try again.")
            else:
                await channel.send(f"An error occured adding the game to the database, please try again later.")
            


    
    
@bot.command()
async def addPlayer(ctx):
    commandText = ctx.message.content.split()
    if len(commandText) == 2:
        database.dbAddPlayerRecord(database.databaseConnections[ctx.message.guild.id], ctx.message.mentions[0].id, ctx.message.mentions[0].name)
        await ctx.send(f"Alright, player {ctx.message.mentions[0].name} has been recorded!")

@bot.command()
async def mercy(ctx):
    commandText = ctx.message.content.split()
    await ctx.send(f"I am not a merciful god, but this indiscretion shall be allowed.")


bot.run(TOKEN)