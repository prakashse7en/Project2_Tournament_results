#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
"""contains operations like creating connection with db ,insert,delete,update etc"""
__license__ = "Prakash"

import psycopg2

def reportWinner():
    """returns the winner of the tournament"""
    DB = connect()
    c = DB.cursor()
    
    #WINNER is a view
    c.execute("""select * from WINNER;""")
    row = c.fetchall()
    
    [(name)] = row
   
    DB.commit()
    DB.close()
    print "winner is",row[0][0]

def restartSequence():
    """reintialises the id values of table PLAYER_RECORDS,PLAYERS,FIXTURES to 1 """
    DB = connect();
    c = DB.cursor()
    
    c.execute("ALTER SEQUENCE PLAYERS_P_ID_seq RESTART WITH 1;")
    DB.commit()
    DB.close()    
    """Restart the sequemce from 1."""


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect();
    c = DB.cursor()
    query = "delete from player_records;"
    c.execute(query)
    DB.commit()
    DB.close()    
    """Remove all the match records from the database."""


def deletePlayers():
    """Remove all the player records from the database."""
    deleteMatches()
    DB = connect();
    c = DB.cursor()
    query = "delete from players;"
    c.execute(query)
    DB.commit()
    DB.close()    

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect();
    c = DB.cursor()
    c.execute("select count(*) as players_count from PLAYERS;")
    noOfRows = c.fetchone()
    #print noOfRows[0]
    
    DB.commit()
    DB.close()
    return noOfRows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect();
    c = DB.cursor()
    c.execute("insert into players(player_name) VALUES (%s)", [name])
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect();
    c = DB.cursor()
    
    """ PLAYERS_STANDINGS is a view """
    c.execute("""select * from PLAYERS_STANDINGS;""")
    row = c.fetchall()
    #print noOfRows[0]
    """
    while row is not None:
        print row[0], row[2]
        row = c.fetchone()
    """
    
    DB.commit()
    DB.close()
    return row


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect();
    c = DB.cursor()
    
    c.execute (""" UPDATE player_records SET (WINS) = ((player_records.WINS + 1)) , (TOTAL_MATCHES) = ((player_records.TOTAL_MATCHES + 1)) WHERE (PLAYER_ID=%s) """, [winner])
    c.execute (""" UPDATE player_records SET (TOTAL_MATCHES) = ((player_records.TOTAL_MATCHES + 1)) WHERE (PLAYER_ID=%s) """, [loser])
    DB.commit()
    DB.close()
    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect();
    c = DB.cursor()
    c.execute("""select * from PLAYERS_STANDINGS;""")
    rowsFetched = c.fetchall()
    #print len(rowsFetched)
    
    listOfFixtures = []
    j = 0
    
    for i in range(0, (len(rowsFetched)/2)):
        
        fixtureSet =  (rowsFetched[j][0],rowsFetched[j][1],rowsFetched[j+1][0],rowsFetched[j+1][1])
        listOfFixtures.append(fixtureSet)
        
        j = j+2
   
    
    DB.commit()
    DB.close()
    return listOfFixtures

