import sqlite3
import datetime

databaseConnections = {}

def dbConnect(guildID: int) -> sqlite3.Connection:
    dbPath = 'data/'+str(guildID)+'.db'
    URI = f'file:{dbPath}?mode=rw'
    connection = sqlite3.connect(URI, uri=True)
    return connection

def initializeDatabase(guildID: int) -> sqlite3.Connection:
    dbPath = 'data/'+str(guildID)+'.db'
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    try:
        dbCreatePlayersTable(connection,cursor)
        dbCreateGameTable(connection,cursor)
        connection.commit()
    except:
        connection.rollback()
        raise
    return connection
  
def dbCreatePlayersTable(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS players(
            playerid INTEGER PRIMARY KEY NOT NULL,
            discordid int NOT NULL,
            name varchar(50) NOT NULL
        )
        '''
    )
    
def dbCreateGameTable(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS games(
            gameid INTEGER PRIMARY KEY NOT NULL,
            date_played varchar(40) NOT NULL,
            game_name varchar(50) NOT NULL,
            chosen_by int NOT NULL,
            FOREIGN KEY(chosen_by) REFERENCES players(discordid)
            )
        '''
    )

def addGame(cursor,game, user):
    record = (datetime.datetime.now().isoformat(),game,user)
    cursor.execute(
        "INSERT INTO games (date_played, game_name, chosen_by) VALUES (?, ?, ?)", record
    )

def dbAddPlayerRecord(userid,name):
    con = dbConnect()
    record = (userid,name)
    con.cursor.execute(
        "INSERT INTO players (discordid, name) VALUES (?, ?)",record
    )