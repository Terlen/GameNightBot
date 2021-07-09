import sqlite3
from _pytest.monkeypatch import monkeypatch
import pytest
import utils.database as database

class mockConnection:
    rollback_called = False
    commit_called = False
    def __init__(self, data=None):
        self.data = data
    def cursor(self):
        cursor = mockCursor(self, self.data)
        return cursor
    def commit(self, *args, **kwargs):
        self.commit_called = True
        return None
    def rollback(self, *args, **kwargs):
        self.rollback_called = True

class mockCursor:
    def __init__(self, parent=mockConnection(), data=None):
        self.data = data
        self.connection = parent
    def execute(self, *args, **kwargs):
        return self.data

def mock_OperationalError(*args, **kwargs):
            raise sqlite3.OperationalError("Mock disconnection error")

def mock_IntegrityError(*args, **kwargs):
            raise sqlite3.IntegrityError("Violation of foreign key requirement")
    
class Test_addGame_Unit:
    @pytest.mark.parametrize("cursor, name, player, expected", [(mockCursor(), "Pong", "Terlen", None)])
    def test_addGame(self, cursor, name, player, expected):
        # successful test case
        # input: cursor, game name, player
        # output: None
        assert database.addGame(cursor, name, player) == expected

    @pytest.mark.parametrize("cursor, name, player, expected", [(mockCursor(), "Pong", "Terlen",None)])
    def test_addGameOperationalError(self, monkeypatch, cursor, name, player, expected):
        # failure test case
        # input: cursor, game name, player
        # exception: sqlite3.OperationalError
        monkeypatch.setattr(cursor, "execute", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert database.addGame(cursor, name, player) == expected

    @pytest.mark.parametrize("cursor, name, player, expected", [(mockCursor(), "Pong", "Fake",None)])
    def test_addGameIntegrityError(self, monkeypatch, cursor, name, player, expected):
        # failure test case
        # input: cursor,  game name, player who doesn't yet exist in the players table
        # exception: sqlite3.IntegrityError
        monkeypatch.setattr(mockCursor, "execute", mock_IntegrityError)
        with pytest.raises(sqlite3.IntegrityError):
            assert database.addGame(cursor, name, player) == expected

class Test_Unit_dbConnect:
    
    def mock_Connect(self,*args, **kwargs):
       return mockConnection()

    # success test case
    # input: guildID: int
    # output: sqlite3.Connection
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_dbConnect(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", self.mock_Connect)
        assert isinstance(database.dbConnect(guildID), mockConnection)

    # failure test case: unexpected disconnect
    # input: guildID: int
    # raise sqlite3.OperationalException
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_dbConnectOperationalError(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert isinstance(database.dbConnect(guildID), mockConnection)

