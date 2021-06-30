# Module to handle bot message functionality including input validation, command confirmation.

import discord
from discord.utils import get
#from collections import defaultdict

pendingVerify = {}

# Send verification message to reiterate task being done
async def verifyMessage(context: 'Verification', game: str, operation: str):
    if operation == "add":
        context.verifyMessage = await context.commandRequest.send(f"{game} will be added to the list of played games, is that correct?")
    
    pendingVerify[context.commandRequest.guild.id].append(context)
    await addConfirmEmoji(context.verifyMessage)



# Add yes/no option to message via emoji reaction
async def addConfirmEmoji(verificationMessage: 'discord.Message') -> None:
    # Post "No" reaction (red 'x' emoji)
    await verificationMessage.add_reaction('\u274C')
    # Post "Yes" reaction (white heave check mark emoji)
    await verificationMessage.add_reaction('\u2705')
    

