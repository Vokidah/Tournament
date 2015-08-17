-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament;

CREATE DATABASE tournament;

\c tournament;

create table player(
    id serial primary key,
    name text unique,
    wins int default 0,
    matches int default 0
    );

create table matches (
    winner int references player(id),
    loser int references player(id),
    check(winner!=loser)
    );
