from discord import message
import discord.ext
import utils.messages as messages
import pytest
import asyncio

class MockMessage:
    @staticmethod
    def add_reaction():
        pass

@pytest.mark.asyncio
async def test_addConfirmEmojiSuccess(monkeypatch):
    
    async def mock_add_reaction(*args, **kwargs):
        pass

    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    result = await messages.addConfirmEmoji(fakeMessage)
    assert result == None



