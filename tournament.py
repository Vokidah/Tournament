#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from player;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) as num from player;")
    num = c.fetchone()[0]
    db.close()
    return num

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into player(name) values(%s);", (bleach.clean(name),))
    db.commit()
    db.close()


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
    list = []
    db = connect()
    c = db.cursor()
    c.execute("select * from player;")
    players = c.fetchall()
    for player in players:
        list.append(player)
    db.close()
    return list



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches(first_player_id,second_player_id,winner) values(%s,%s,%s)",
              (winner,loser,winner))
    c.execute("update player set wins=(select wins from player where id=%s)+1 where id = %s",
              (winner,winner))
    c.execute("update player set matches=(select matches from player where id=%s)+1 where id = %s",
              (winner,winner))
    c.execute("update player set matches=(select matches from player where id=%s)+1 where id = %s",
              (loser,loser))
    db.commit()
    db.close()


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
    db = connect()
    c = db.cursor()
    list = []
    c.execute("select max(player.wins) from player")
    max_wins = c.fetchone()[0]+1
    for i in range(0,max_wins):
        c.execute("select id,name from player where wins=%s",str(i))
        my_list=[]
        for id,name in c.fetchall():
            my_list.append(id)
            my_list.append(name)
        list.append(tuple(my_list))
    return list


