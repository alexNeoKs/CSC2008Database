SET SQL_SAFE_UPDATES = 0;
USE spotify;

drop table if exists album;
CREATE TABLE album AS 
(SELECT distinct album_id, album from tmp_albums);

drop table if exists explicit;
CREATE TABLE explicit AS 
(SELECT distinct id as song_id, explicit from tmp_albums);

drop table if exists danceability;
CREATE TABLE danceability AS 
(SELECT distinct id as song_id, danceability from tmp_albums);

drop table if exists energy;
CREATE TABLE energy AS 
(SELECT distinct id as song_id, energy from tmp_albums);

drop table if exists `key`;
CREATE TABLE `key` AS 
(SELECT distinct id as song_id, `key` from tmp_albums);

drop table if exists loudness;
CREATE TABLE loudness AS 
(SELECT distinct id as song_id, loudness from tmp_albums);

drop table if exists `mode`;
CREATE TABLE `mode` AS 
(SELECT distinct id as song_id, `mode` from tmp_albums);

drop table if exists speechiness;
CREATE TABLE speechiness AS 
(SELECT distinct id as song_id, speechiness from tmp_albums);

drop table if exists acousticness;
CREATE TABLE acousticness AS 
(SELECT distinct id as song_id, acousticness from tmp_albums);

drop table if exists instrumentalness;
CREATE TABLE instrumentalness AS 
(SELECT distinct id as song_id, instrumentalness from tmp_albums);

drop table if exists liveness;
CREATE TABLE liveness AS 
(SELECT distinct id as song_id, liveness from tmp_albums);

drop table if exists valence;
CREATE TABLE valence AS 
(SELECT distinct id as song_id, valence from tmp_albums);

drop table if exists tempo;
CREATE TABLE tempo AS 
(SELECT distinct id as song_id, tempo from tmp_albums);

drop table if exists song_album;
CREATE TABLE song_album AS 
(SELECT distinct id as song_id, album_id, track_number, disc_number from tmp_albums);

drop table if exists song;
CREATE TABLE song AS
(SELECT distinct id as song_id, `name`, duration_ms, time_signature, `year`, release_date from tmp_albums);

drop table if exists gender;
CREATE TABLE gender AS
(SELECT distinct artist, gender, `type` from tmp_artists);

ALTER TABLE acousticness MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE acousticness ADD PRIMARY KEY (song_id);

ALTER TABLE danceability MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE danceability ADD PRIMARY KEY (song_id);

ALTER TABLE energy MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE energy ADD PRIMARY KEY (song_id);

ALTER TABLE explicit MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE explicit ADD PRIMARY KEY (song_id);

ALTER TABLE instrumentalness MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE instrumentalness ADD PRIMARY KEY (song_id);

ALTER TABLE `key` MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE `key` ADD PRIMARY KEY (song_id);

ALTER TABLE liveness MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE liveness ADD PRIMARY KEY (song_id);

ALTER TABLE loudness MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE loudness ADD PRIMARY KEY (song_id);

ALTER TABLE `mode` MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE `mode` ADD PRIMARY KEY (song_id);

ALTER TABLE song MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE song MODIFY COLUMN name    VARCHAR(600);
ALTER TABLE song ADD PRIMARY KEY (song_id);

ALTER TABLE song_album MODIFY COLUMN song_id  VARCHAR(22);
ALTER TABLE song_album MODIFY COLUMN album_id VARCHAR(22);
ALTER TABLE song_album ADD PRIMARY KEY (song_id);

ALTER TABLE speechiness MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE speechiness ADD PRIMARY KEY (song_id);

ALTER TABLE tempo MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE tempo ADD PRIMARY KEY (song_id);

ALTER TABLE valence MODIFY COLUMN song_id VARCHAR(22);
ALTER TABLE valence ADD PRIMARY KEY (song_id);

ALTER TABLE normalized_artists            RENAME artist;
ALTER TABLE normalized_song_lookup_artist RENAME song_artist;

DELETE FROM artist WHERE artist_id = '1G9G7WwrXka3Z1r7aIDjI7';
ALTER TABLE artist ADD PRIMARY KEY (artist_id);
INSERT INTO artist VALUES ( '1G9G7WwrXka3Z1r7aIDjI7' , 'Outkast' );
ALTER TABLE artist ADD INDEX artist_name ( artist );

ALTER TABLE song_artist ADD PRIMARY KEY (song_id,artist_id);
ALTER TABLE song_artist ADD INDEX song   ( song_id   );
ALTER TABLE song_artist ADD INDEX artist ( artist_id );

ALTER TABLE song_album ADD INDEX disc_track ( disc_number , track_number );
ALTER TABLE song_album ADD INDEX song   ( song_id  );
ALTER TABLE song_album ADD INDEX album  ( album_id );

ALTER TABLE song   ADD INDEX song_name ( `name` );
ALTER TABLE album  ADD INDEX album_name ( album );

DELIMITER $
CREATE PROCEDURE spotify.FindSongsAndAlbumsByArtistName( IN artistName VARCHAR(255) )
BEGIN
	SELECT 
	song.`name`,
	song.`year`,
	song_album.`disc_number`,
	song_album.`track_number`,
	album.`album`,
    a.`artist` 
	FROM 
	( SELECT artist.`artist`, song_artist.`song_id` 
	  FROM       artist 
	  INNER JOIN song_artist ON artist.`artist_id` = song_artist.`artist_id` 
	  WHERE (artist.`artist`) LIKE (CONCAT('%', artistName ,'%')) ) a 
	  INNER JOIN song       ON a.`song_id`      = song.`song_id` 
	  INNER JOIN song_album ON a.`song_id`      = song_album.`song_id`
	  INNER JOIN album      ON album.`album_id` = song_album.`album_id`
	  ORDER BY a.`artist`, song.`year` DESC, album.`album` , song_album.`disc_number`, song_album.`track_number`;
END$
DELIMITER ;

DELIMITER $
CREATE PROCEDURE spotify.FindSongsAndArtistsByAlbumName( IN albumName VARCHAR(255) )
BEGIN
	SELECT  
	song.`name`,
	song.`year`,
	a.`disc_number`,
	a.`track_number`,
	a.`album`,
	artist.`artist` 
	FROM 
	( SELECT  album.`album`, song_album.`song_id`,song_album.`disc_number`,song_album.`track_number`
	FROM album 
	INNER JOIN song_album ON album.`album_id` = song_album.`album_id`
	WHERE (album.`album`) LIKE (CONCAT('%', albumName ,'%')) ) a
	INNER JOIN song        ON a.`song_id`       = song.`song_id` 
	INNER JOIN song_artist ON a.`song_id`       = song_artist.`song_id`
	INNER JOIN artist      ON artist.`artist_id`= song_artist.`artist_id`
	ORDER BY a.`album`, artist.`artist`, song.`year` DESC,  a.`disc_number`, a.`track_number`;
END$
DELIMITER ;

DELIMITER $
CREATE PROCEDURE spotify.FindArtistsAndAlbumsBySongName( IN songName VARCHAR(255) )
BEGIN
	SELECT 
	song.`name`,
	song.`year`,
	song_album.`disc_number` ,
	song_album.`track_number`,
	album.`album`,
	artist.`artist` 
	FROM song 
	INNER JOIN song_artist ON song.`song_id`     = song_artist.`song_id` 
	INNER JOIN artist      ON artist.`artist_id` = song_artist.`artist_id`
	INNER JOIN song_album  ON song.`song_id`     = song_album.`song_id` 
	INNER JOIN album       ON album.`album_id`   = song_album.`album_id` 
	WHERE (song.`name`) LIKE (CONCAT('%', songName ,'%')) ;
END$
DELIMITER ;

