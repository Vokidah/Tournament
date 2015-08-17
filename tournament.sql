-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table player(
    id serial unique,
    name text unique,
    wins integer default 0,
    matches integer default 0,
    primary key(id)
    );

create table matches (
    first_player_id serial references player(id),
    second_player_id serial references player(id),
    winner integer,
    check(first_player_id!=second_player_id)
    );
