# Module to handle bot message functionality including input validation, command confirmation.

import discord
from discord.errors import Forbidden, HTTPException, InvalidArgument, NotFound
from discord.utils import get
from typing import Union
#from collections import defaultdict

pendingVerify = {}

class Verification:
    def __init__(self, ctx):
        self.user = ctx.author.id
        self.commandRequest = ctx
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.verified = False
        self.verifyMessage = None

# Send verification message to reiterate task being done
async def verifyMessage(context: Verification, game: str, operation: str):
    if operation == "add":
        context.verifyMessage = await context.commandRequest.send(f"{game} will be added to the list of played games, is that correct?")
    
    pendingVerify[context.commandRequest.guild.id].append(context)
    if (await addConfirmEmoji(context.verifyMessage)):
        await context.verifyMessage.clear_reactions()
        await context.commandRequest.send(f"An error occured")





# Add yes/no option to message via emoji reaction
async def addConfirmEmoji(verificationMessage: discord.Message) -> Union[None,HTTPException,Forbidden,NotFound,InvalidArgument]:
    try:
        # Post "No" reaction (red 'x' emoji)
        await verificationMessage.add_reaction('\u274C')
        # Post "Yes" reaction (white heave check mark emoji)
        await verificationMessage.add_reaction('\u2705')
    except (HTTPException,Forbidden,NotFound,InvalidArgument) as err:
        return err

