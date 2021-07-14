import sqlite3
from _pytest.monkeypatch import monkeypatch
import pytest
import utils.database as database

class mockConnection:
    def __init__(self, data=None):
        self.data = data
    def cursor(self):
        cursor = mockCursor(self, self.data)
        return cursor
    def rollback(self):
        pass
    def commit(self):
        pass

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

def mock_ProgrammingError(*args, **kwargs):
            raise sqlite3.ProgrammingError("Table already exists or not found")

def mock_Connect(self,*args, **kwargs):
       return mockConnection()

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
    # success test case
    # input: guildID: int
    # output: sqlite3.Connection
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_dbConnect(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        assert isinstance(database.dbConnect(guildID), mockConnection)

    # failure test case: unexpected disconnect
    # input: guildID: int
    # raise sqlite3.OperationalException
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_dbConnectOperationalError(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert isinstance(database.dbConnect(guildID), mockConnection)

class Test_Unit_dbCreatePlayersTable:
    connection = mockConnection()
    cursor = connection.cursor()
    # Success test case
    # input: Connection: mockConnection, cursor: mockCursor
    # output: None
    @pytest.mark.parametrize("connection, cursor",[(connection, cursor)])
    def test_dbCreatePlayersTable(self, monkeypatch, connection, cursor):
        assert database.dbCreatePlayersTable(connection, cursor) is None
    
    # failure test case
    # input: Connection: mockConnection, cursor: mockCursor
    # raise: sqlite3.OperationalError
    @pytest.mark.parametrize("connection, cursor",[(connection, cursor)])
    def test_dbCreatePlayersTable_OperationalError(self, monkeypatch, connection, cursor):
        monkeypatch.setattr(cursor, "execute", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert database.dbCreatePlayersTable(connection, cursor) is None
            

    # failure test case
    # input: Connection: mockConnection, cursor: mockCursor
    # raise sqlite3.IntegrityError
    @pytest.mark.parametrize("connection, cursor", [(connection, cursor)])
    def test_dbCreatePlayersTable_IntegrityError(self, monkeypatch, connection, cursor):
        monkeypatch.setattr(cursor, "execute", mock_IntegrityError)
        with pytest.raises(sqlite3.IntegrityError):
            assert database.dbCreatePlayersTable(connection, cursor) is None

class Test_Unit_dbCreateGameTable:
    connection = mockConnection()
    cursor = connection.cursor()
    # Success test case
    # input: Connection: mockConnection, cursor: mockCursor
    # output: None
    @pytest.mark.parametrize("connection, cursor",[(connection, cursor)])
    def test_dbCreateGameTable(self, monkeypatch, connection, cursor):
        assert database.dbCreateGameTable(connection, cursor) is None
    
    # failure test case
    # input: Connection: mockConnection, cursor: mockCursor
    # raise: sqlite3.OperationalError
    @pytest.mark.parametrize("connection, cursor",[(connection, cursor)])
    def test_dbCreateGameTable_OperationalError(self, monkeypatch, connection, cursor):
        monkeypatch.setattr(cursor, "execute", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert database.dbCreateGameTable(connection, cursor) is None
            

    # failure test case
    # input: Connection: mockConnection, cursor: mockCursor
    # raise sqlite3.IntegrityError
    @pytest.mark.parametrize("connection, cursor", [(connection, cursor)])
    def test_dbCreateGameTable_IntegrityError(self, monkeypatch, connection, cursor):
        monkeypatch.setattr(cursor, "execute", mock_IntegrityError)
        with pytest.raises(sqlite3.IntegrityError):
            assert database.dbCreateGameTable(connection, cursor) is None

class Test_Unit_initializeDatabase:
    # Successful test case
    # input: guildID: int
    # output: sqlite3.connection
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", lambda *args, **kwargs: None)
        monkeypatch.setattr(database, "dbCreateGameTable", lambda *args, **kwargs: None)
        assert isinstance(database.initializeDatabase(guildID), mockConnection)

    # Failure test case: OperationalError when creating db file
    # input: guildID: int
    # raise: sqlite3.OperationalError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_OperationalError_dbConnect(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_OperationalError)
        monkeypatch.setattr(database, "dbCreatePlayersTable", lambda *args, **kwargs: None)
        monkeypatch.setattr(database, "dbCreateGameTable", lambda *args, **kwargs: None)
        with pytest.raises(sqlite3.OperationalError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)
    
    # Failure test case: IntegrityError when creating db file
    # input: guildID: int
    # raise: sqlite3.IntegrityError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_IntegrityError_dbConnect(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_IntegrityError)
        monkeypatch.setattr(database, "dbCreatePlayersTable", lambda *args, **kwargs: None)
        monkeypatch.setattr(database, "dbCreateGameTable", lambda *args, **kwargs: None)
        with pytest.raises(sqlite3.IntegrityError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)
    
    # Failure test case: OperationalError when creating players table
    # input: guildID: int
    # raise: sqlite3.IntegrityError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_OperationalError_createPlayers(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", mock_OperationalError)
        monkeypatch.setattr(database, "dbCreateGameTable", lambda *args, **kwargs: None)
        with pytest.raises(sqlite3.OperationalError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)
    
    # Failure test case: IntegrityError when creating players table
    # input: guildID: int
    # raise: sqlite3.IntegrityError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_IntegrityError_createPlayers(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", mock_IntegrityError)
        monkeypatch.setattr(database, "dbCreateGameTable", lambda *args, **kwargs: None)
        with pytest.raises(sqlite3.IntegrityError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)

    # Failure test case: ProgrammingError when creating players table
    # input: guildID: int
    # raise: sqlite3.ProgrammingError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_ProgrammingError_createPlayers(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", mock_ProgrammingError)
        monkeypatch.setattr(database, "dbCreateGameTable", lambda *args, **kwargs: None)
        with pytest.raises(sqlite3.ProgrammingError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)
    
    # Failure test case: OperationalError when creating game table
    # input: guildID: int
    # raise: sqlite3.OperationalError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_OperationalError_createGameTable(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", lambda *args, **kwargs: None)
        monkeypatch.setattr(database, "dbCreateGameTable", mock_OperationalError)
        with pytest.raises(sqlite3.OperationalError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)

    # Failure test case: IntegrityError when creating game table
    # input: guildID: int
    # raise: sqlite3.IntegrityError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_IntegrityError_createGameTable(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", lambda *args, **kwargs: None)
        monkeypatch.setattr(database, "dbCreateGameTable", mock_IntegrityError)
        with pytest.raises(sqlite3.IntegrityError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)
    
    # Failure test case: ProgrammingError when adding creating game table
    # input: guildID: int
    # raise: sqlite3.ProgrammingError
    @pytest.mark.parametrize("guildID", [(1234)])
    def test_initializeDatabase_ProgrammingError_createGameTable(self, monkeypatch, guildID):
        monkeypatch.setattr(sqlite3, "connect", mock_Connect)
        monkeypatch.setattr(database, "dbCreatePlayersTable", lambda *args, **kwargs: None)
        monkeypatch.setattr(database, "dbCreateGameTable", mock_ProgrammingError)
        with pytest.raises(sqlite3.ProgrammingError):
            assert isinstance(database.initializeDatabase(guildID), mockConnection)