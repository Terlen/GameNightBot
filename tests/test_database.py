import sqlite3
from _pytest.monkeypatch import monkeypatch
import pytest
import utils.database as database
from sqlite3 import OperationalError, Cursor

class mockCursor:
        @classmethod
        def execute(*args, **kwargs):
            return None

class Test_addGame_Unit:
    @pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(mockCursor, "Pong", "Terlen",None)])
    def test_addGame(self, test_cur, test_name, test_player, expected):
        # successful test case
        # input: cursor, game name, player
        # output: None
        assert database.addGame(test_cur, test_name, test_player) == expected

    @pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(mockCursor, "Pong", "Terlen",None)])
    def test_addGameOperationalError(self, monkeypatch, test_cur, test_name, test_player, expected):
        # failure test case
        # input: cursor, game name, player
        # exception: sqlite3.OperationalError
        def mock_addGameOperationalError(*args, **kwargs):
            raise sqlite3.OperationalError("Mock disconnection error")
        monkeypatch.setattr(mockCursor, "execute", mock_addGameOperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert database.addGame(test_cur, test_name, test_player) == expected

    @pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(mockCursor, "Pong", "Fake",None)])
    def test_addGameIntegrityError(self, monkeypatch, test_cur, test_name, test_player, expected):
        # failure test case
        # input: cursor,  game name, player who doesn't yet exist in the players table
        # exception: sqlite3.IntegrityError
        def mock_addGameIntegrityError(*args, **kwargs):
            raise sqlite3.IntegrityError("Violation of foreign key requirement")
        monkeypatch.setattr(mockCursor, "execute", mock_addGameIntegrityError)
        with pytest.raises(sqlite3.IntegrityError):
            assert database.addGame(test_cur, test_name, test_player) == expected


def test_addPlayer():
    pass