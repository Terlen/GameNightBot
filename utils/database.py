from typing import List, Dict
from discord import Guild
import sqlite3
import datetime

# def databaseExceptionHandler(function):
#     def handler(*args, **kwargs):
#         try:
#             return function(*args, **kwargs)
#         except sqlite3.OperationalError:
#             raise 
#     return handler
#, TypeError, sqlite3.DatabaseError, sqlite3.IntegrityError, sqlite3.ProgrammingError, sqlite3.NotSupportedError) as err:
databaseConnections = {}
#@exception_handler
def dbConnect(guildList: List[Guild]) -> Dict[int, sqlite3.Connection]:
    connections = {guild.id: sqlite3.connect("data/"+str(guild.id)+".db") for guild in guildList}
    #for guild in guildList:
    #connection = sqlite3.connect(str())
    return connections

#@exception_handler
def getCursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    return connection.cursor()

def dbCreateGameTable(con,cur):
# Build game history table
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS games(
            gameid INTEGER PRIMARY KEY NOT NULL,
            date_played varchar(40) NOT NULL,
            game_name varchar(50) NOT NULL,
            chosen_by int NOT NULL,
            FOREIGN KEY(chosen_by) REFERENCES players(discordid)
            )
        '''
    )
    con.commit()

def dbCreatePlayersTable(con,cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS players(
            playerid INTEGER PRIMARY KEY NOT NULL,
            discordid int NOT NULL,
            name varchar(50) NOT NULL
        )
        '''
    )
    con.commit()

def addGame(cursor,game, user):
    record = (datetime.datetime.now().isoformat(),game,user)
    cursor.execute(
        "INSERT INTO games (date_played, game_name, chosen_by) VALUES (?, ?, ?)", record
    )

def dbAddPlayerRecord(userid,name):
    con,cur = dbConnect()
    record = (userid,name)
    cur.execute(
        "INSERT INTO players (discordid, name) VALUES (?, ?)",record
    )
    con.commit()
    con.close()