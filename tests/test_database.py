import sqlite3
from _pytest.monkeypatch import monkeypatch
import pytest
import utils.database as database
from sqlite3 import OperationalError, Cursor

@pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(sqlite3.Cursor, "Pong", "Terlen",None)])
def test_addGame():
    # successful test case
    # input: cursor, game name, player
    # output: None
    assert database.addGame(test_cur, test_name, test_player) == None

def test_addGameOperationalError(monkeypatch):
    # failure test case
    # input: cursor, game name, player
    # exception: sqlite3.OperationalError
    def mock_addGameOperationalError(*args, **kwargs):
        raise sqlite3.OperationalError("Mock disconnection error")
    monkeypatch.setattr(database, "addGame", mock_addGameOperationalError)
    with pytest.raises(sqlite3.OperationalError):
        assert database.addGame(validCur, gameName, player) == None

def test_addGameIntegrityError(monkeypatch):
    # failure test case
    # input: cursor,  game name, player who doesn't yet exist in the players table
    # exception: sqlite3.IntegrityError
    def mock_addGameIntegrityError(*args, **kwargs):
         raise sqlite3.IntegrityError("Violation of foreign key requirement")
    monkeypatch.setattr(database, "addGame", mock_addGameIntegrityError)
    with pytest.raises(sqlite3.IntegrityError):
        assert database.addGame(validCur, gameName, player) == None




def test_addPlayer():
    pass