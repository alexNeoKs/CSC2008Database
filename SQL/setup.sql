#-- SHOW VARIABLES LIKE "sql_safe_updates";
#-- SHOW VARIABLES LIKE "local_infile";

SET SQL_SAFE_UPDATES = 0;
SET GLOBAL local_infile=1;
USE spotify;

DROP TABLE IF EXISTS tmp_albums;
DROP TABLE IF EXISTS tmp_songs;
DROP TABLE IF EXISTS tmp_artists;

CREATE TABLE `tmp_albums` (
  `id` varchar(1024) DEFAULT NULL,
  `name` varchar(2048) DEFAULT NULL,
  `album` varchar(2048) DEFAULT NULL,
  `album_id` varchar(2048) DEFAULT NULL,
  `artists` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `artist_ids` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `track_number` int(11) DEFAULT NULL,
  `disc_number` int(11) DEFAULT NULL,
  `explicit` varchar(10) DEFAULT NULL,
  `danceability` float DEFAULT NULL,
  `energy` float DEFAULT NULL,
  `key` tinyint(4) DEFAULT NULL,
  `loudness` float DEFAULT NULL,
  `mode` tinyint(4) DEFAULT NULL,
  `speechiness` float DEFAULT NULL,
  `acousticness` float DEFAULT NULL,
  `instrumentalness` float DEFAULT NULL,
  `liveness` float DEFAULT NULL,
  `valence` float DEFAULT NULL,
  `tempo` float DEFAULT NULL,
  `duration_ms` int(11) DEFAULT NULL,
  `time_signature` tinyint(4) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `release_date` varchar(50) DEFAULT NULL
) ENGINE=InnoDB;

LOAD DATA INFILE '/var/lib/mysql-files/albums.csv' 
REPLACE INTO TABLE `spotify`.`tmp_albums` 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(`id`, `name`, `album`, `album_id`, `artists`, `artist_ids`, `track_number`, `disc_number`, `explicit`, `danceability`, 
`energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, 
`duration_ms`, `time_signature`, `year`, `release_date`);

CREATE TABLE `tmp_songs` (
	`index` INT(11) NULL,
	`title` VARCHAR(2048) NULL DEFAULT NULL,
	`artist` VARCHAR(255) NULL DEFAULT NULL,
	`top_genre` VARCHAR(255) NULL DEFAULT NULL,
	`year` INT(11) NULL DEFAULT NULL,
	`bpm` INT(11) NULL DEFAULT NULL,
	`energy` INT(11) NULL DEFAULT NULL,
	`dance` INT(11) NULL DEFAULT NULL,
	`decibel` INT(11) NULL DEFAULT NULL,
	`liveliness` INT(11) NULL DEFAULT NULL,
	`val` INT(11) NULL DEFAULT NULL,
	`duration` INT(11) NULL DEFAULT NULL,
	`acoustics` INT(11) NULL DEFAULT NULL,
	`spch` INT(11) NULL DEFAULT NULL,
	`pop` INT(11) NULL DEFAULT NULL
) ENGINE=InnoDB;

LOAD DATA INFILE '/var/lib/mysql-files/songs.csv' 
REPLACE INTO TABLE `spotify`.`tmp_songs` 
CHARACTER SET latin2
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(`index`,`title`,`artist`,`top_genre`,`year`,
`bpm`,`energy`,`dance`,`decibel`,`liveliness`,
`val`,`duration`,`acoustics`,`spch`,`pop`);

CREATE TABLE `tmp_artists` (
	`rank` INT(11) NULL,
	`index` INT(11) NULL,
	`artist` VARCHAR(255) NULL DEFAULT NULL,
	`gender` VARCHAR(50) NULL DEFAULT NULL,
	`age` INT(11) NULL DEFAULT NULL,
	`type` VARCHAR(50) NULL DEFAULT NULL,
	`country` VARCHAR(50) NULL DEFAULT NULL,
	`city_1` VARCHAR(255) NULL DEFAULT NULL,
	`district_1` VARCHAR(255) NULL DEFAULT NULL,
	`city_2` VARCHAR(255) NULL DEFAULT NULL,
	`district_2` VARCHAR(255) NULL DEFAULT NULL,
	`city_3` VARCHAR(255) NULL DEFAULT NULL,
	`district_3` VARCHAR(255) NULL DEFAULT NULL
) ENGINE=InnoDB;

LOAD DATA INFILE '/var/lib/mysql-files/artists.csv' 
REPLACE INTO TABLE `spotify`.`tmp_artists` 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
ESCAPED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(`rank`,`index`,`artist`,`gender`,`age`,`type`,
 `country`,`city_1`,`district_1`,`city_2`,`district_2`,`city_3`,`district_3`);

DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS artists;

CREATE TABLE albums AS 
( SELECT DISTINCT tmp_albums.* FROM tmp_albums, tmp_songs, tmp_artists WHERE tmp_albums.name = tmp_songs.title AND tmp_songs.artist = tmp_artists.artist );

CREATE TABLE songs AS 
( SELECT DISTINCT tmp_songs.* FROM tmp_albums, tmp_songs, tmp_artists WHERE tmp_albums.name = tmp_songs.title AND tmp_songs.artist = tmp_artists.artist );

CREATE TABLE artists AS 
( SELECT DISTINCT tmp_artists.* FROM tmp_albums, tmp_songs, tmp_artists WHERE tmp_albums.name = tmp_songs.title AND tmp_songs.artist = tmp_artists.artist );

#-- DROP TABLE IF EXISTS tmp_albums;
#-- DROP TABLE IF EXISTS tmp_songs;
#-- DROP TABLE IF EXISTS tmp_artists;