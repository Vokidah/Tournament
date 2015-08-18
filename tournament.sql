-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
IF EXISTS tournament;
DROP DATABASE tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE player(
    id serial PRIMARY KEY,
    name text UNIQUE,
    wins int DEFAULT 0,
    matches int DEFAULT 0
    );

CREATE TABLE matches(
    winner int REFERENCES player(id),
    loser int REFERENCES player(id),
    CHECK(winner!=loser)
    );
