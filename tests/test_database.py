import sqlite3
from _pytest.monkeypatch import monkeypatch
import pytest
import utils.database as database

class mockConnection:
    def __init__(self, data=None):
        self.data = data
    def cursor(self,*args, **kwargs):
        return mockCursor(self.data)

class mockCursor:
    def __init__(self, data=None):
        self.data = data
    def execute(self, *args, **kwargs):
        return self.data

def mock_OperationalError(*args, **kwargs):
            raise sqlite3.OperationalError("Mock disconnection error")

def mock_addGameIntegrityError(*args, **kwargs):
            raise sqlite3.IntegrityError("Violation of foreign key requirement")
    
class Test_addGame_Unit:
    @pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(mockCursor(), "Pong", "Terlen",None)])
    def test_addGame(self, test_cur, test_name, test_player, expected):
        # successful test case
        # input: cursor, game name, player
        # output: None
        assert database.addGame(test_cur, test_name, test_player) == expected

    @pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(mockCursor(), "Pong", "Terlen",None)])
    def test_addGameOperationalError(self, monkeypatch, test_cur, test_name, test_player, expected):
        # failure test case
        # input: cursor, game name, player
        # exception: sqlite3.OperationalError
        monkeypatch.setattr(mockCursor, "execute", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert database.addGame(test_cur, test_name, test_player) == expected

    @pytest.mark.parametrize("test_cur,test_name,test_player, expected", [(mockCursor(), "Pong", "Fake",None)])
    def test_addGameIntegrityError(self, monkeypatch, test_cur, test_name, test_player, expected):
        # failure test case
        # input: cursor,  game name, player who doesn't yet exist in the players table
        # exception: sqlite3.IntegrityError
        monkeypatch.setattr(mockCursor, "execute", mock_addGameIntegrityError)
        with pytest.raises(sqlite3.IntegrityError):
            assert database.addGame(test_cur, test_name, test_player) == expected

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

def test_addPlayer():
    pass