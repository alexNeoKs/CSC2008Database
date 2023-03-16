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
