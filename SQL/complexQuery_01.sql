DELIMITER $
CREATE PROCEDURE spotify.FindSongsAndArtistsByAlbumName( IN albumName VARCHAR(100) )
BEGIN
    SELECT songs.title, GROUP_CONCAT(DISTINCT artists.artist) AS artists, artists.city_1
    FROM songs
    JOIN albums ON songs.title = albums.name
    JOIN artists ON albums.artists LIKE CONCAT('%',artists.artist , '%')
    WHERE albums.album = albumName
    GROUP BY songs.title, artists.city_1;
END$
DELIMITER ;
CALL FindSongsAndArtistsByAlbumName('silence');
CALL FindSongsAndArtistsByAlbumName('Rainbow');