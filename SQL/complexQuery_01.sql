SELECT songs.title, GROUP_CONCAT(DISTINCT artists.artist) AS artists, artists.city_1
FROM songs
JOIN albums ON songs.title = albums.name
JOIN artists ON albums.artists LIKE CONCAT('%',artists.artist , '%')
WHERE albums.album = 'Silence'
GROUP BY songs.title, artists.city_1;
