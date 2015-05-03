-- Table definitions for the tournament project.
--contains sql commands for creating tables,triggers and views


CREATE DATABASE tournament;

\c tournament;

CREATE  TABLE PLAYERS (
  P_ID SERIAL PRIMARY KEY ,
  PLAYER_NAME VARCHAR(45) NULL);
----------------------------------  
CREATE TABLE player_records (
  ID SERIAL PRIMARY KEY,
  PLAYER_ID integer references PLAYERS(P_ID),
  WINS integer DEFAULT NULL,
  TOTAL_MATCHES integer DEFAULT NULL
) 
		  

-----------------------------------------
CREATE OR REPLACE FUNCTION insertIntoPlayerRecords()
  RETURNS trigger AS
$$
BEGIN
         INSERT INTO player_records(PLAYER_ID,WINS,TOTAL_MATCHES)
         VALUES(NEW.P_ID,0,0);
 
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER AUTO_INSERT_TRIGGER
  AFTER INSERT
  ON PLAYERS
  FOR EACH ROW
  EXECUTE PROCEDURE insertIntoPlayerRecords();

----------------------------------------
------------views
CREATE VIEW PLAYERS_STANDINGS AS
select PLAYERS.P_ID ,PLAYERS.PLAYER_NAME,player_records.WINS,
              player_records.TOTAL_MATCHES from player_records left join players
              on player_records.PLAYER_ID = players.P_ID order by player_records.wins desc;

CREATE VIEW WINNER AS
    select PLAYER_NAME from PLAYERS where P_ID= (select PLAYER_ID  from player_records where wins =(select MAX(wins) from player_records));	
