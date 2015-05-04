#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import itertools
from operator import itemgetter
from itertools import izip

"""contains operations like creating connection with db ,insert,delete,update
etc"""
__license__ = "Prakash"


def insertBye(idOfPlayer, tournament):
    """increments wins and total matches of the player by 1 as it is a bye.
    """
    DB, c = connect()
    c.execute(""" UPDATE player_tournament_stats SET (WINS) =
                ((player_tournament_stats.WINS + 1)) ,(TOTAL_MATCHES) =
                ((player_tournament_stats.TOTAL_MATCHES + 1))
                    WHERE (PLAYER_ID=%s) and (tournament_id=%s)
                    """, [(idOfPlayer), (tournament)])
    DB.commit()
    DB.close()


def reportWinner(tournamentId):
    """returns the winner of the tournament"""
    DB, c = connect()
    c.execute("""select PLAYER_NAME from PLAYERS where P_ID=
              (select PLAYER_ID  from  player_tournament_stats where wins =
              (select MAX(wins) from player_tournament_stats) and
              (tournament_id =%s));""", [tournamentId])
    row = c.fetchall()
    [(name)] = row
    DB.commit()
    DB.close()
    print row[0][0]


def restartSequence():
    """reintialises the id values of table player_tournament_stats,
    PLAYERS,FIXTURES,PLAYER_REGISTERED to 1 """
    DB, c = connect()
    c.execute("ALTER SEQUENCE player_tournament_stats_ID_seq RESTART WITH 1;")
    c.execute("ALTER SEQUENCE PLAYERS_P_ID_seq RESTART WITH 1;")
    c.execute("ALTER SEQUENCE FIXTURES_ID_seq RESTART WITH 1;")
    c.execute("ALTER SEQUENCE PLAYER_REGISTERED_ID_seq RESTART WITH 1;")
    DB.commit()
    DB.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=swiss_tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("connection failed due to inncorrect db name")


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    query = "delete from player_tournament_stats;"
    c.execute(query)
    c.execute("delete from FIXTURES;")
    DB.commit()
    DB.close()


def deleteTournament():
    """Remove all the players registerd for the tournament."""
    DB, c = connect()
    c.execute("delete from PLAYER_REGISTERED;")
    query = "delete from tournament;"
    c.execute(query)
    DB.commit()
    DB.close()


def registerPlayerForTournament(playerName, tId):
    """adds players id value into player_registered table"""
    DB, c = connect()
    c.execute("select p_id from PLAYERS where(PLAYER_NAME=%s);", [playerName])
    player = c.fetchall()
    c.execute("""insert into PLAYER_REGISTERED(PLAYER_ID,TOURNAMENT_ID) VALUES
                (%s,%s)""", [(player[0][0]), (tId)])
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    deleteMatches()
    DB, c = connect()
    query = "delete from players;"
    c.execute(query)
    DB.commit()
    DB.close()


def countPlayers(tournamentId):
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("""select count(player_id) as players_count from PLAYER_REGISTERED
                 where (TOURNAMENT_ID=%s);""", [tournamentId])
    noOfRows = c.fetchone()
    DB.commit()
    DB.close()
    return noOfRows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.
    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    c.execute("insert into players(player_name) VALUES (%s)", [name])
    DB.commit()
    DB.close()


def playerStandings(tournamentId):
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    """ PLAYERS_STANDINGS is a view """
    c.execute("""select * from PLAYERS_STANDINGS WHERE (tournament_id=%s);
                 """, [tournamentId])
    row = c.fetchall()
    DB.commit()
    DB.close()
    return row


def reportMatch(winner, loser, tId):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tId: tournament id in which match is played
    """
    DB, c = connect()
    c.execute(""" UPDATE player_tournament_stats SET (WINS) =
              ((player_tournament_stats.WINS + 1)) ,
            (TOTAL_MATCHES) = ((player_tournament_stats.TOTAL_MATCHES + 1))
            WHERE (PLAYER_ID=%s) """, [winner])
    c.execute(""" UPDATE player_tournament_stats SET (TOTAL_MATCHES) =
              ((player_tournament_stats.TOTAL_MATCHES + 1))
              WHERE (PLAYER_ID=%s) """, [loser])
    c.execute(""" insert into FIXTURES(TEAM_1,TEAM_2,TOURNAMENT_ID)
                VALUES (%s,%s,%s)""", [(winner), (loser), (tId)])
    DB.commit()
    DB.close()


def distintWinsValue(tournamentId):
    """Return wins which is common for more than one player .
    Args:
      tournamentId: tournament id in which match is played
    """
    DB, c = connect()
    """ PLAYERS_WITH_COMMONWINS is a view """
    c.execute("""select distinct wins from player_tournament_stats where wins in
                (select wins from player_tournament_stats where
                tournament_id in (select wins  from player_tournament_stats
                where (tournament_id = %s)) group by wins having count(*) > 1)
                order by wins desc;""", [tournamentId])
    distinctWinsList = c.fetchall()
    DB.commit()
    DB.close()
    return distinctWinsList


def playersStandingsOMWSimple(winNo, tournamentId):
    """get the player id based on win and tournament ids and
    get the corresponding matches played against from FIXTURES table
        for each player played against calculate his strength.
        Strength Calulation for player played against = total wins
        of opponent player's played against
        once all players strength is calculated rank it based on wins
    Args:
    winNo - win value
    tournamentId: tournament id in which match is played
    """
    DB, c = connect()
    """ PLAYERS_WITH_COMMONWINS is a view """
    c.execute("""select player_id from player_tournament_stats  WHERE (wins=%s)
              and (TOURNAMENT_ID = %s) """, [(winNo), (tournamentId)])
    playerIds = c.fetchall()
    buffer_total_wins = 0
    playersWinsDict = {}
    playerIdFromI = 0
    for i in range(0, len(playerIds)):
        c.execute("""select case when (team_1  = %s)  then team_2 else team_1
                 end as opposing_team from fixtures where ((team_1  = %s) or
                 (team_2 = %s)) and (TOURNAMENT_ID = %s);
                 """, [(playerIds[i]),
                       (playerIds[i]),
                       (playerIds[i]),
                       (tournamentId)])
        rows = c.fetchall()
        buffer_total_wins = 0
        playerIdFromI = 0
        for j in range(0, len(rows)):
            c.execute("""select wins from player_tournament_stats where
                     (PLAYER_ID=%s) and (TOURNAMENT_ID = %s);
                     """, [(rows[j]), (tournamentId)])
            eachPlayerTotWins = c.fetchall()
            eachWinsVal, = eachPlayerTotWins[0]
            playerIdFromI, = (playerIds[i])
            buffer_total_wins = eachWinsVal + buffer_total_wins
        playersWinsDict[playerIdFromI] = buffer_total_wins
        sortedValuesByWins = sorted(playersWinsDict.items(),
                                    key=itemgetter(1),
                                    reverse=True)
    DB.commit()
    DB.close()
    return sortedValuesByWins


def getRankBasedOnWins(tournamentId):
    """"rank the players over maximum wins and return the players position
    Args:
    tournamentId: tournament id in which match is played
    """
    DB, c = connect()
    c.execute("""SELECT PLAYER_ID, rank() OVER (ORDER BY wins DESC)
                FROM player_tournament_stats where (tournament_id=%s);
                """, [tournamentId])
    rowsFetched = c.fetchall()
    DB.commit()
    DB.close()
    return rowsFetched


def swissPairings(tournamentId):
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
    DB, c = connect()
    c.execute("""select * from PLAYERS_STANDINGS WHERE
             (tournament_id=%s);""", [tournamentId])
    rowsFetched = c.fetchall()
    listOfFixtures = []
    j = 0
    for i in range(0, (len(rowsFetched)/2)):
        fixtureSet = (rowsFetched[j][0],
                      rowsFetched[j][1],
                      rowsFetched[j+1][0],
                      rowsFetched[j+1][1])
        listOfFixtures.append(fixtureSet)
        j = j+2
    DB.commit()
    DB.close()
    return listOfFixtures


def getOpponent(playerId, tournamentId, playerToBeRemoved):
    """ return the opponent player Id based on total matches played ,
    wins and tournament
    Args:
    playerId - id of the player
    tournamentId: tournament id in which match is played
    playerToBeRemoved - id of the player whose value need to be
    removed from the list of values from fetched from db
    based on total matches played ,wins and tournament
    """
    DB, c = connect()
    c.execute("""select total_matches from player_tournament_stats
                 where (player_id = %s);""", [(playerId)])
    totalMatches = c.fetchall()
    c.execute("""select player_id from player_tournament_stats where wins
                in (select wins from player_tournament_stats where
                (player_id = %s) and (tournament_id=%s)) and
                (player_id != %s) and (tournament_id=%s) and
                (total_matches=%s);
                """, [(playerId),
                      (tournamentId),
                      (playerId),
                      (tournamentId),
                      (totalMatches[0])])
    opponentIds = c.fetchall()
    if not opponentIds:
        opponentIds = getPlayerWithNearestWin(playerId,
                                              tournamentId,
                                              playerToBeRemoved,
                                              totalMatches)
    DB.commit()
    DB.close()
    opponentIds = removeOpponentIds(playerToBeRemoved, opponentIds)
    opponentIds = removeDuplicateOpponents(playerId, opponentIds, tournamentId)
    if not opponentIds:
        opponentIds = getPlayerWithNearestWin(playerId,
                                              tournamentId,
                                              playerToBeRemoved,
                                              totalMatches)
    return opponentIds


def getPlayerWithNearestWin(playerId,
                            tournamentId,
                            playerToBeRemoved,
                            totalMatches):
    """when no opponent is found for the player an opponent with nearest wins
    is picked and returned
     Args:
    playerId - id of the player
    tournamentId: tournament id in which match is played
    playerToBeRemoved - id of the player whose value need to be removed from
    the list of values from fetched from db
    based on total matches played ,wins and tournament
    totalMatches - total matches played in the tournament
    """
    DB, c = connect()
    c.execute("""select player_id from player_tournament_stats where wins <
            (select wins from player_tournament_stats where (player_id = %s)
            and (tournament_id=%s)) and (player_id != %s)
            and (tournament_id=%s) and (total_matches=%s)
            order by wins;""", [(playerId),
                                (tournamentId),
                                (playerId),
                                (tournamentId),
                                (totalMatches[0])])
    opponentIds = c.fetchall()
    DB.commit()
    DB.close()
    opponentIds = removeOpponentIds(playerToBeRemoved, opponentIds)
    opponentIds = removeDuplicateOpponents(playerId, opponentIds, tournamentId)
    return opponentIds


def removeOpponentIds(playerToBeRemoved, opponentIds):
    """ remove the ids from opponentIds as this id has already played a match
    against him
    Args:
    playerToBeRemoved - id of the player whose value need to be removed from
    the list of values from fetched from db
    based on total matches played ,wins and tournament
    opponentIds - list of ids be played against the player
    """
    if playerToBeRemoved is not None:
        playerValue = [item for item in opponentIds if playerToBeRemoved in item]
        if playerValue:
            opponentIds.remove(playerValue[0])
    return opponentIds


def getPerfectOpponent(opponentIds, tournamentId):
    """ return the opponent player ids sorted based in their strength
        Strength = retreive players played against by each opponent id ,
        total all the wins , compare with
        the rest of opponent ids and sort them based on maximum wins and return
    Args:
    tournamentId: tournament id in which match is played
    opponentIds - list of ids be played against the player
    """
    DB, c = connect()
    playerIds = opponentIds
    # below variable is used to calculate the total wins
    buffer_total_wins = 0
    playersWinsDict = {}
    playerIdFromI = 0
    for i in range(0, len(playerIds)):
        c.execute("""select case when (team_1  = %s)  then team_2 else team_1 end
                    as opposing_team from fixtures where ((team_1  = %s) or
                    (team_2 = %s)) and (TOURNAMENT_ID = %s);
                    """, [(playerIds[i]),
                          (playerIds[i]),
                          (playerIds[i]),
                          (tournamentId)])
        rows = c.fetchall()
        buffer_total_wins = 0
        playerIdFromI = 0
        for j in range(0, len(rows)):
            c.execute("""select wins from player_tournament_stats where
            (PLAYER_ID=%s) and (TOURNAMENT_ID = %s);  """, [(rows[j]),
                                                            (tournamentId)])
            eachPlayerTotWins = c.fetchall()
            eachWinsVal, = eachPlayerTotWins[0]
            playerIdFromI, = (playerIds[i])
            buffer_total_wins = eachWinsVal + buffer_total_wins
        playersWinsDict[playerIdFromI] = buffer_total_wins
        sortedValuesByWins = sorted(playersWinsDict.items(),
                                    key=itemgetter(1),
                                    reverse=True)
    DB.commit()
    DB.close()
    return sortedValuesByWins


def removeDuplicateOpponents(playerId, opponentIds, tournamentId):
    """ remove duplicate opponents with help of rows retreived from Fixtures
    based on player Id
    Args:
    playerId - id of the player
    opponentIds - list of ids be played against the player
    tournamentId: tournament id in which match is played
    """
    DB, c = connect()
    c.execute("""select case when (team_1  = %s)  then team_2 else team_1 end
       as opposing_team from fixtures where ((team_1  = %s) or (team_2 = %s))
       and (TOURNAMENT_ID = %s); """, [(playerId),
                                       (playerId),
                                       (playerId),
                                       (tournamentId)])
    rows = c.fetchall()
    bufferRows = [list(i) for i in rows]
    bufferOpponentIds = [list(i) for i in opponentIds]
    bufferListToBeRemoved = []
    for i in range(0, len(bufferRows)):
        for j in range(0, len(bufferOpponentIds)):
            if(bufferRows[i] == bufferOpponentIds[j]):
                bufferListToBeRemoved.append(bufferOpponentIds[j][0])
    if(len(bufferListToBeRemoved) > 0):
        for i in range(0, (len(bufferListToBeRemoved))):
            print bufferOpponentIds
            bufferOpponentIds.remove([bufferListToBeRemoved[i]])
    opponentIds = list(tuple(tuple(i) for i in bufferOpponentIds))
    DB.commit()
    DB.close()
    return opponentIds


def getWinsInEntireTournament(playerId):
    """ returns the total wins of the player in all tournaments played
    Args:
    playerId - player id of the player"""
    DB, c = connect()
    c.execute("""select sum(wins) from player_tournament_stats where
               (player_id=%s) """, [playerId])
    wins = c.fetchall()
    # print noOfRows[0]
    DB.commit()
    DB.close()
    print "wins is =", wins[0][0]


def createTournament(tournamentNumber):
    """ create a tournament based on tournament number given as input
    Args:
    tournamentNumber: tournament id in which match is played
    """
    DB, c = connect()
    c.execute("insert into tournament(T_ID) VALUES (%s)", [tournamentNumber])
    DB.commit()
    DB.close()
