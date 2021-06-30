import sqlite3
import datetime

def dbConnect():
    connection = sqlite3.connect('data/gameNight.db')
    cur = connection.cursor()
    return connection,cur

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

def dbAddGameRecord(game, user):
    con,cur = dbConnect()
    record = (datetime.datetime.now().isoformat(),game,user)
    cur.execute(
        "INSERT INTO games (date_played, game_name, chosen_by) VALUES (?, ?, ?)", record
    )
    con.commit()
    con.close()

def dbAddPlayerRecord(userid,name):
    con,cur = dbConnect()
    record = (userid,name)
    cur.execute(
        "INSERT INTO players (discordid, name) VALUES (?, ?)",record
    )
    con.commit()
    con.close()