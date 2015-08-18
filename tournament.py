#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    return db, c

def execute_query(query, variables=(), fetch = False, commit = False):
    # Template for execution queries
    db, c = connect()
    c.execute(query, variables)
    if fetch:
        fetched = c.fetchall()
        if len(fetched) == 1:
            fetched = fetched[0]
    else:
        fetched = None
    if commit:
        db.commit()
    db.close()
    return fetched

def deleteMatches():
    """Remove all the match records from the database."""
    query = "delete from matches;"
    execute_query(query, commit = True)

def deletePlayers():
    """Remove all the player records from the database."""
    query = "delete from player;"
    execute_query(query, commit = True)

def countPlayers():
    """Returns the number of players currently registered."""

    # Counting all our players who are already registered in our database
    query = "select count(*) as num from player;"

    return execute_query(query, fetch=True)[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Adding new player in our tournament database
    query = "insert into player(name) values(%s);"

    # checking our name for correctness
    variables = (bleach.clean(name),)
    execute_query(query, variables, commit=True)

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
    final_list = []

    # Just getting all players
    query = "select * from player order by wins asc;"

    players = execute_query(query, fetch=True)
    for player in players:
        final_list.append(player)
    return final_list



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # select winner and loser in matches table
    query = "insert into matches(winner,loser) values(%s,%s)"
    variables = (winner, loser)
    execute_query(query, variables, commit=True)

    # updating winner`s count of wins
    query = "update player set wins=(select wins from player where id=%s)+1 where id = %s"
    variables = (winner, winner)
    execute_query(query, variables, commit=True)

    # updating count of matches for both players

    query = "update player set matches=(select matches from player where id=%s)+1 where id = %s"
    variables = (loser, loser)
    execute_query(query, variables, commit=True)

    query = "update player set matches=(select matches from player where id=%s)+1 where id = %s"
    variables = (winner, winner)
    execute_query(query, variables, commit=True)



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
    final_list = []
    my_list = []
    players = playerStandings()
    for (number, name, wins, matches) in players:
        my_list.append(number)
        my_list.append(name)
        if len(my_list) == 4:
            final_list.append(tuple(my_list))
            my_list = []
    print(final_list)
    return final_list
