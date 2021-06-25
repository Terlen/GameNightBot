# Module to handle bot message functionality including input validation, command confirmation.

import discord
from discord.utils import get

# Send verification message to reiterate task being done
async def commandMessage(ctx: discord.ext.commands.Context):
    pass


# Add yes/no option to message via emoji reaction
async def addConfirmEmoji(verificationMessage: discord.Message) -> None:
    # Post "No" reaction (red 'x' emoji)
    await verificationPrompt.add_reaction('\U0000274C')
    # Post "Yes" reaction (white heave check mark emoji)
    await verificationPrompt.add_reaction('\U00002705')

