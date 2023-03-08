SELECT songs.title, songs.top_genre, GROUP_CONCAT(DISTINCT albums.album) AS album , GROUP_CONCAT(DISTINCT artists.artist) AS artists
FROM songs
JOIN albums ON songs.title = albums.name
JOIN artists ON albums.artists LIKE CONCAT('%',artists.artist ,'%')
WHERE artists.artist = 'Adele'
GROUP BY songs.title, songs.top_genre;