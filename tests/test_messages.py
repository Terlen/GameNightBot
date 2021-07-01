from discord import message
from discord.errors import Forbidden, HTTPException, InvalidArgument, NotFound
import discord.ext
import utils.messages as messages
import pytest
import asyncio

class MockMessage:
    @staticmethod
    def add_reaction(emoji):
        pass

class MockHTTPResponse:
    def __init__(self, status=400,reason="Bad Request"):
        self.status = status
        self.reason = reason

@pytest.mark.asyncio
async def test_addConfirmEmojiSuccess(monkeypatch):
    
    async def mock_add_reaction(*args, **kwargs):
        return None

    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    result = await messages.addConfirmEmoji(fakeMessage)
    assert result == None

@pytest.mark.asyncio
async def test_addConfirmEmojiHTTPException(monkeypatch):
    async def mock_add_reaction(*args, **kwargs):
        raise HTTPException(MockHTTPResponse(), "Bad Request")
    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    err = await messages.addConfirmEmoji(fakeMessage)
    assert type(err) == HTTPException
    
@pytest.mark.asyncio
async def test_addConfirmEmojiForbidden(monkeypatch):
    async def mock_add_reaction(*args, **kwargs):
        raise Forbidden(MockHTTPResponse(403,"Forbidden"),"This is a test of a forbidden message")
    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    err = await messages.addConfirmEmoji(fakeMessage)
    assert type(err) == Forbidden

@pytest.mark.asyncio
async def test_addConfirmEmojiNotFound(monkeypatch):
    async def mock_add_reaction(*args, **kwargs):
        raise NotFound(MockHTTPResponse(404,"Not Found"),"This is a test of a not found message")
    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    err = await messages.addConfirmEmoji(fakeMessage)
    assert type(err) == NotFound

@pytest.mark.asyncio
async def test_addConfirmEmojiInvalidArgument(monkeypatch):
    async def mock_add_reaction(*args, **kwargs):
        raise InvalidArgument()
    fakeMessage = MockMessage()
    monkeypatch.setattr(fakeMessage, "add_reaction", mock_add_reaction)
    err = await messages.addConfirmEmoji(fakeMessage)
    assert type(err) == InvalidArgument