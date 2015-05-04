#!/usr/bin/env python
#
# Test cases for tournament.py
import math
from tournament import *
from operator import itemgetter

"""Contains methods to get winner of the tournament,get rank of each players at
the end of tournament,perform swiss pairings etc."""

__license__ = "Prakash"


def testDeleteMatches():
    """this methid is used delete matches table"""
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    """this method is used to delete matches,tournament,players table"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    """this method is used to test count functionality"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    c = countPlayers(1)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    """this method is used to test registration process"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    createTournament(1)
    registerPlayer("Chandra Nalaar")
    registerPlayerForTournament("Chandra Nalaar", 1)
    c = countPlayers(1)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    """this method is used count the players that are registered/deleted"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    createTournament(1)
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    registerPlayerForTournament("Markov Chaney", 1)
    registerPlayerForTournament("Joe Malik", 1)
    registerPlayerForTournament("Mao Tsu-hsi", 1)
    registerPlayerForTournament("Atlanta Hope", 1)
    c = countPlayers(1)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deleteMatches()
    deleteTournament()
    deletePlayers()
    c = countPlayers(1)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    """this method is used to test standings of players before match is
    started"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    createTournament(1)
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    registerPlayerForTournament("Melpomene Murray", 1)
    registerPlayerForTournament("Randy Schwartz", 1)
    # SPECIFY TOURNAMENT ID TO GET THE PLAYER STANDINGS IN THAT TOURNAMENT
    standings = playerStandings(1)
    if len(standings) < 2:
        raise ValueError("""Players should appear in playerStandings even
        before they have played any matches.""")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1, tid1),
     (id2, name2, wins2, matches2, tid2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("""Registered players' names should
                            appear in standings, even if they
                            have no matches played.""")
    print """6. Newly registered players appear in the standings
             with no matches."""


def testReportMatches():
    "this method is used to create a match between two players"
    deleteMatches()
    deleteTournament()
    deletePlayers()
    restartSequence()
    # specify tournament
    createTournament(1)
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayerForTournament("Bruno Walton", 1)
    registerPlayerForTournament("Boots O'Neal", 1)
    registerPlayerForTournament("Cathy Burton", 1)
    registerPlayerForTournament("Diane Grant", 1)
    # specify tournament to get standings
    standings = playerStandings(1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # specify tournament in which match is played
    reportMatch(id1, id2, 1)
    reportMatch(id3, id4, 1)
    standings = playerStandings(1)
    for (i, n, w, m, t) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("""Each match loser should have
                                zero wins recorded.""")
    print "7. After a match, players have updated standings."


def testPairings():
    """this method is used to test swiss pairings
    """
    deleteMatches()
    deleteTournament()
    deletePlayers()
    restartSequence()
    createTournament(1)
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayerForTournament("Twilight Sparkle", 1)
    registerPlayerForTournament("Fluttershy", 1)
    registerPlayerForTournament("Applejack", 1)
    registerPlayerForTournament("Pinkie Pie", 1)
    standings = playerStandings(1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, 1)
    reportMatch(id3, id4, 1)
    # specify tournament id for which swiss pairing is done
    pairings = swissPairings(1)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def getWinnerOfTournament():
    """This method is used to return winner of the swiss pairing tournament
    Here list of players are registered
    first round alone players are played against consecutive ids
    from second round players are played against opponents having similar match
    wins ,total matches and in same tournament.
    each round players are played against different set of players they are
    matched
    Duplicate opponents are removed player with nearby win value is chosen
    finally once all the rounds are completed player with maximum wins is
    reported"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    restartSequence()
    createInputs(1)
    standings = playerStandings(1)
    tournamentId = 1
    for i in range(0, (int(math.log(len(standings), 2)))):
        standings = playerStandings(1)
        """i is for iteration for rounds"""
        if(i == 0):
            """j is for iteration in number of matches for single round"""
            for j in range(0, (len(standings)), 2):
                reportMatch(standings[j][0], standings[j+1][0], 1)
        else:
            playerToBeRemoved = None
            for j in range(0, (len(standings)/2)):
                opponentIds = getOpponent(standings[j][0],
                                          1, playerToBeRemoved)
                if (len(opponentIds) > 0):
                    playersPositions = getPerfectOpponent(opponentIds,
                                                          tournamentId)
                    rankingDict = {}
                    rankingDict = rankBasedOnPlayerPosition(rankingDict,
                                                            playersPositions)
                    sortedValuesByWins = sorted(rankingDict.items(),
                                                key=itemgetter(1))
                    randomPlayerId = getEligiblePlayer(sortedValuesByWins)
                    reportMatch(standings[j][0], randomPlayerId[0], 1)
                    # code to remove the played people
                    playerToBeRemoved = randomPlayerId[0]
                    tupleTobeRemoved = [i for i, v in enumerate(standings)
                                        if v[0] == randomPlayerId[0]]
                    standings.remove(standings[tupleTobeRemoved[0]])
                else:
                    reportMatch(standings[j][0], opponentIds[0], 1)
                    playerToBeRemoved = opponentIds[0]
                    tupleTobeRemoved = [i for i, v in enumerate(standings)
                                        if v[0] == opponentIds[0]]
                    standings.remove(standings[tupleTobeRemoved[0]])
    print "9. Winner is found."
    reportWinner(1)


def getEligiblePlayer(sortedValuesByWins):
    """ when there are more than one opponent ranking 1st,this method will
    return a single opponent id from list of common opponents
    Args:
    sortedValuesByWins - contains the opponent player id and position
"""
    count = 0
    for i in range(len(sortedValuesByWins)):
        if(sortedValuesByWins[i][1] == 1):
            count += 1
            randomIValue = i-1
    if(count > 1):
        return sortedValuesByWins[randomIValue]
    else:
        return sortedValuesByWins[randomIValue]


def oddNumberRegistration():
    """This method is used to test swiss pairings based on odd number of players
    here odd number of players is created and the first player is given bye and
    swiss pairing is tested for the same number of players"""
    deleteMatches()
    deleteTournament()
    deletePlayers()
    restartSequence()
    createTournament(1)
    registerPlayer("Prakash")
    registerPlayer("Rajesh")
    registerPlayer("Suresh")
    registerPlayer("Praveen")
    registerPlayer("bala")
    registerPlayerForTournament("Prakash", 1)
    registerPlayerForTournament("Rajesh", 1)
    registerPlayerForTournament("Suresh", 1)
    registerPlayerForTournament("Praveen", 1)
    registerPlayerForTournament("bala", 1)
    standings = playerStandings(1)
    # number of players registered for a tournament
    count = countPlayers(1)
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    """ assuming first player is given bye and rounds---> first run the single
    round without first player
            then run for all players"""
    if(count % 2 != 0):
        insertBye(id1, 1)
        # j is for iteration in number of matches for single round
        for j in range(1, (len(standings)), 2):
            reportMatch(standings[j][0], standings[j+1][0], 1)
    # i is for iteration in number of rounds
    for i in range(0, (int(math.log(len(standings), 2)))):
        standings = playerStandings(1)
        # j is for iteration in number of matches for single round
        for j in range(0, (len(standings)), 2):
            if(j == (len(standings) - 1)):
                break
            else:
                reportMatch(standings[j][0], standings[j+1][0], 1)
    print "12. odd number registration winner is ."
    reportWinner(1)


def createInputs(tournamentId):
    """This method is used to create inputs based on tournament id
    Args:
    tournamentId - id of the tournament played
    """
    createTournament(tournamentId)
    registerPlayer("Prakash")
    registerPlayer("Rajesh")
    registerPlayer("Suresh")
    registerPlayer("Praveen")
    registerPlayer("bala")
    registerPlayer("naveen")
    registerPlayer("karthik")
    registerPlayer("natesan")
    registerPlayerForTournament("Prakash", tournamentId)
    registerPlayerForTournament("Rajesh", tournamentId)
    registerPlayerForTournament("Suresh", tournamentId)
    registerPlayerForTournament("Praveen", tournamentId)
    registerPlayerForTournament("bala", tournamentId)
    registerPlayerForTournament("naveen", tournamentId)
    registerPlayerForTournament("karthik", tournamentId)
    registerPlayerForTournament("natesan", tournamentId)


def rankBasedOnOMW():
    """method is used to rank the players based on OMW.
    Here players with common wins are retreived and
    they are ranked based on OMW,
    i.e ,total wins of each opponenets players played against
    is calculated and the total value is used to rank the players with common
    wins,player inputs is used from getWinnerOfTournament()"""
    # get players rank list dictionary based on number of wins
    playersByRankList = getRankBasedOnWins(1)
    """need to take length of disting wins and print standing among players
    with common wins"""
    distinctWinsList = distintWinsValue(1)
    for k in range(0, len(distinctWinsList)):
        playersPositions = playersStandingsOMWSimple(distinctWinsList[k], 1)
        rankingDict = {}
        rankingDict = rankBasedOnPlayerPosition(rankingDict, playersPositions)
        # displaying the dict ordering values by descending order
        sortedValuesByWins = sorted(rankingDict.items(), key=itemgetter(1))
        playersByRankList = reorderPositions(playersByRankList,
                                             sortedValuesByWins)
    displayFinalList(playersByRankList)


def rankBasedOnPlayerPosition(rankingDict, playersPositions):
    """Method is used to rank the players based on player postion
    Args:
    rankingDict - dictionary used to store current value of ranks
    playersPositions - list containing player id and player rank
    """
    rankValue = 1
    prevPlayerValue = 0
    prevPlayerRankValue = 1
    bufferRankValue = 0
    count = 0
    for i in range(0, (len(playersPositions))):
        if(i >= 1):
            if(playersPositions[i][1] == prevPlayerValue):
                rankValue = prevPlayerRankValue
            else:
                rankValue = countPlayersRank(rankingDict, prevPlayerRankValue)
        rankingDict[playersPositions[i][0]] = rankValue
        prevPlayerValue = playersPositions[i][1]
        prevPlayerRankValue = rankValue
    return rankingDict


def countPlayersRank(rankingDict, prevPlayerRankValue):
    """method is used to count players with common rank
    Args:
    prevPlayerRankValue - rank value for previous player
    rankingDict - dictionary containing the players id and rank value
    """
    count = 0
    for key, elem in rankingDict.items():
        if(elem == prevPlayerRankValue):
            count += 1
    return prevPlayerRankValue + count


def displayFinalList(playersByRankList):
    """method is used to display the final postions of the players based on the
    wins.
    Args:
    playersByRankList - orginal list of players fetched from db
                        in which players with common winns are ordered"""
    bufferPlayersByRankList = [list(i) for i in playersByRankList]
    for i in range(0, len(playersByRankList)):
        bufferPlayersByRankList[i][1] = str(bufferPlayersByRankList[i][1]) + ' Position'
    print '10.printing the final standing list based on OMW'
    print bufferPlayersByRankList


def reorderPositions(playersByRankList, sortedValuesByWins):
    """method is used to reorder the positions of players with common wins based
    on values present in sortedValuesByWins
    Args:
    playersByRankList - orginal list of players fetched from
    db in which players with common winns are un ordered
    sortedValuesByWins - ordered list of players with common wins"""
    bufferPlayersByRankList = [list(i) for i in playersByRankList]
    bufferSortedValuesByWins = [list(i) for i in sortedValuesByWins]
    for i in range(0, len(playersByRankList)):
        for j in range(0, len(sortedValuesByWins)):
            if(bufferPlayersByRankList[i][0] == bufferSortedValuesByWins[j][0] and bufferSortedValuesByWins[j][1] != 1):
                bufferPlayersByRankList[i][1] = bufferPlayersByRankList[i][1] + bufferSortedValuesByWins[j][1]-1
    # convert back to tuple
    return list(tuple(tuple(i) for i in bufferPlayersByRankList))


def multipleTournament():
    """method used to test multiple tournaments"""
    createInputs(2)
    print "11.Total wins of a player with id 5 in both the tournament "
    getWinsInEntireTournament(5)


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
    # new methods for getting swiss pairing winner
    getWinnerOfTournament()
    rankBasedOnOMW()
    multipleTournament()
    oddNumberRegistration()

