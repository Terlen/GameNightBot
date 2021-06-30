from discord import message
from discord.errors import HTTPException
import discord.ext
import utils.messages as messages
import pytest
import asyncio

class MockMessage:
    @staticmethod
    def add_reaction():
        pass

class MockHTTPResponse:
    status = "400"
    reason = "Bad Request"

@pytest.mark.asyncio
async def test_addConfirmEmojiSuccess(monkeypatch):
    
    async def mock_add_reaction(*args, **kwargs):
        pass

    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    result = await messages.addConfirmEmoji(fakeMessage)
    assert result == None

@pytest.mark.asyncio
async def test_addConfirmEmojiFailed(monkeypatch):
    async def mock_add_reaction(*args, **kwargs):
        raise HTTPException(MockHTTPResponse(),"This is a test of a failed message")

    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    result = await messages.addConfirmEmoji(fakeMessage)
    assert result == None

