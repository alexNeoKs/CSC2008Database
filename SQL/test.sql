USE spotify;
SELECT * FROM tmp1;
SELECT * FROM tmp2;

SELECT COUNT(*) FROM tmp1;
SELECT COUNT(*) FROM tmp2;

SELECT COUNT(*) FROM tmp_albums;

SELECT artists FROM albums;

SELECT id, id1, id2 , artists, artist1 FROM albums , (SELECT tmp1.id as id1 , tmp2.id as id2 , tmp1.artist as artist1 FROM tmp1 LEFT  OUTER JOIN tmp2 ON tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord WHERE tmp2.id IS NULL) a WHERE albums.id = a.id1;
SELECT id, id1, id2 , artists, artist1 FROM albums , (SELECT tmp1.id as id1 , tmp2.id as id2 , tmp1.artist as artist1 FROM tmp1 RIGHT OUTER JOIN tmp2 ON tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord WHERE tmp1.id IS NULL) a WHERE albums.id = a.id2;

SELECT COUNT(*) FROM ( SELECT tmp1.id AS id1 , tmp2.id AS id2 , tmp1.ord AS ord1 , tmp2.ord AS ord2 , tmp1.artist , tmp2.artist_id FROM tmp1 LEFT OUTER JOIN tmp2 ON tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord) a;



SELECT COUNT(*) FROM ( SELECT tmp1.id as id1 , tmp2.id as id2 , tmp1.artist as artist , tmp2.artist_id FROM tmp1 , tmp2 WHERE tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord ) a;

SELECT tmp1.id as id1 , tmp2.id as id2 , tmp1.artist as artist , tmp2.artist_id FROM tmp1 , tmp2 WHERE tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord;
SELECT * FROM albums WHERE id ='4hrc6rZG6AXD9KmeYaen6C';

SELECT DISTINCT id as song_id, artist_id  FROM tmp2 ORDER BY id,artist_id;
SELECT COUNT(*) FROM (SELECT DISTINCT id as song_id, artist_id  FROM tmp2 ORDER BY id,artist_id) a;

CREATE TABLE normalized_artists AS (
SELECT DISTINCT artist_id , artist FROM tmp1 , tmp2 WHERE tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord ORDER BY artist);

SELECT * FROM normalized_artists;

SELECT  DISTINCT albums.id, albums.name, songs.title, artist, artists FROM albums , songs WHERE albums.name = songs.title ORDER BY albums.name, songs.title; 

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

SELECT * FROM songs;
SELECT DISTINCT title, COUNT(title) FROM songs GROUP BY title ORDER BY COUNT(title) DESC;

SELECT * FROM tmp_artists;
