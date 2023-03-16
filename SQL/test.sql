USE spotify;
SELECT * FROM tmp1;
SELECT * FROM tmp2;

SELECT COUNT(*) FROM tmp1;
SELECT COUNT(*) FROM tmp2;

SELECT id, id1, id2 , artists, artist1 FROM albums , (SELECT tmp1.id as id1 , tmp2.id as id2 , tmp1.artist as artist1 FROM tmp1 LEFT  OUTER JOIN tmp2 ON tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord WHERE tmp2.id IS NULL) a WHERE albums.id = a.id1;
SELECT id, id1, id2 , artists, artist1 FROM albums , (SELECT tmp1.id as id1 , tmp2.id as id2 , tmp1.artist as artist1 FROM tmp1 RIGHT OUTER JOIN tmp2 ON tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord WHERE tmp1.id IS NULL) a WHERE albums.id = a.id2;

SELECT tmp1.id as song_id1 , tmp2.id as song_id2 , tmp1.artist as artist , tmp2.artist_id FROM tmp1 , tmp2 WHERE tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord;

DROP TABLE IF EXISTS normalized_song_lookup_artist;
CREATE TABLE normalized_song_lookup_artist AS ( SELECT DISTINCT id as song_id, artist_id  FROM tmp2 ORDER BY id,artist_id );

DROP TABLE IF EXISTS normalized_artists;
CREATE TABLE normalized_artists AS ( SELECT DISTINCT artist_id , artist FROM tmp1 , tmp2 WHERE tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord ORDER BY artist);

SELECT COUNT(*) FROM normalized_song_lookup_artist;
SELECT COUNT(*) FROM normalized_artists;

SELECT * FROM normalized_song_lookup_artist;
SELECT * FROM normalized_artists;

SELECT * FROM tmp_songs  WHERE tmp_songs.title IN ( 'Company', 
'Hello', 
'Sugar', 
'First Time',
'Here', 
'Marry You', 
'I Like It', 
'Say Something', 
'All I Ask', 
'Stitches',
'The Hills', 
'Just the Way You Are',
'Love Yourself', 
'We Are Never Ever Getting Back Together' ) ORDER BY tmp_songs.title;

SELECT * FROM tmp_albums WHERE tmp_albums.name IN ('Company', 
'Hello', 
'Sugar', 
'First Time',
'Here', 
'Marry You', 
'I Like It', 
'Say Something', 
'All I Ask', 
'Stitches',
'The Hills', 
'Just the Way You Are',
'Love Yourself', 
'We Are Never Ever Getting Back Together' ) ORDER BY tmp_albums.name;


