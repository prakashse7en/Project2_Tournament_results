-- Table definitions for the tournament project.
--contains sql commands for creating tables,triggers and views


CREATE DATABASE swiss_tournament;

\c swiss_tournament;

CREATE  TABLE PLAYERS (
  P_ID SERIAL PRIMARY KEY ,
  PLAYER_NAME VARCHAR(45) NULL);
---------------------------------- 
CREATE TABLE TOURNAMENT (
  ID SERIAL,
  T_ID integer NOT NULL PRIMARY KEY
);
---------------------------------- 
CREATE TABLE PLAYER_REGISTERED (
  ID SERIAL PRIMARY KEY,
  PLAYER_ID integer references PLAYERS(P_ID),
  TOURNAMENT_ID integer NOT NULL references TOURNAMENT(T_ID)
);
------------------------------------- 

CREATE TABLE player_tournament_stats (
  ID SERIAL PRIMARY KEY,
  PLAYER_ID integer references PLAYERS(P_ID),
  WINS integer DEFAULT NULL,
  TOTAL_MATCHES integer DEFAULT NULL,
  TOURNAMENT_ID integer references TOURNAMENT(T_ID)
); 
---------------------------------------------
CREATE TABLE FIXTURES (
  ID SERIAL PRIMARY KEY,
  TEAM_1 integer references PLAYERS(P_ID),
  TEAM_2 integer references PLAYERS(P_ID),
  TOURNAMENT_ID integer references TOURNAMENT(T_ID)  
);

-----------------------------------------
CREATE OR REPLACE FUNCTION insertIntoPlayerRecords()
  RETURNS trigger AS
$$
BEGIN
         INSERT INTO player_tournament_stats(PLAYER_ID,WINS,TOTAL_MATCHES,TOURNAMENT_ID)
         VALUES(NEW.PLAYER_ID,0,0,NEW.TOURNAMENT_ID);
 
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER AUTO_INSERT_TRIGGER
  AFTER INSERT
  ON PLAYER_REGISTERED
  FOR EACH ROW
  EXECUTE PROCEDURE insertIntoPlayerRecords();
  
------------------------
-------------queries
CREATE VIEW PLAYERS_STANDINGS AS
select player_tournament_stats.PLAYER_ID,PLAYERS.PLAYER_NAME,player_tournament_stats.WINS,player_tournament_stats.TOTAL_MATCHES,player_tournament_stats.TOURNAMENT_ID from player_tournament_stats inner join PLAYERS on  player_tournament_stats.PLAYER_ID = players.P_ID  order by player_tournament_stats.wins desc,player_tournament_stats.PLAYER_ID asc;


create view PLAYERS_WITH_COMMON_WINS AS
select wins from player_tournament_stats where wins in (
    select wins from player_tournament_stats group by wins having count(*) > 1

        ) order by wins desc;
