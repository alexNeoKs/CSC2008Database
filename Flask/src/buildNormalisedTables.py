import re
import mysql.connector
#-------------------------------------------------------------------------------------------------------------------------------------------

def getItem( comma_separated_string ):
    result = []

    consistent_string = comma_separated_string.replace("\"","\'")

    test1 = re.split(r"'\s,\s'", consistent_string.strip()[1:-1] )

    for item1 in test1:
        if item1.strip() not in ( ',' , ' ,' , ', ', ' , ', '' ) :
            test2 = re.split(r"',\s'", item1 )
            for item2 in test2:
                if item2.strip() not in ( ',' , ' ,' , ', ', ' , ', '' ) :
                    test3 = re.split(r"'\s,'", item2 )
                    for item3 in test3:
                        if item3.strip() not in ( ',' , ' ,' , ', ', ' , ', '' ) :
                            test4 = re.split(r"','", item3 )
                            for item4 in test4:
                                if item4.strip() not in ( ',' , ' ,' , ', ', ' , ', '' ) :
                                    result.append( item4 )
    return result

#-------------------------------------------------------------------------------------------------------------------------------------------

def connectMySQL():
    try:
        db_connect = None
        db_connect = mysql.connector.connect(user     = 'root'   , 
                                             password = 'admin'  ,
                                             host     = 'sql'    , # try either 'localhost' or 'sql'
                                             port     = '3306'   ,
                                             database = 'spotify')
        return db_connect
    except Exception as err :
        try:
            db_connect = None
            db_connect = mysql.connector.connect(user     = 'root'      , 
                                                 password = 'admin'     ,
                                                 host     = 'localhost' , # try either 'localhost' or 'sql'
                                                 port     = '3306'      ,
                                                 database = 'spotify'   )
            return db_connect
        except Exception as err :
            print( err )

#-------------------------------------------------------------------------------------------------------------------------------------------

def build_Albums( db_connect ):

    db_cursor = db_connect.cursor()
    # delete all temporary tables
    deleteTable1 = "DROP TABLE IF EXISTS tmp1;"
    deleteTable2 = "DROP TABLE IF EXISTS tmp2;"
    db_cursor.execute(deleteTable1)
    db_cursor.execute(deleteTable2)
    db_connect.commit()
    
    createTable1 = "CREATE TABLE tmp1 ( id VARCHAR(22) NOT NULL , ord INT(11) NOT NULL , artist    VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL , PRIMARY KEY (id , ord) );"
    createTable2 = "CREATE TABLE tmp2 ( id VARCHAR(22) NOT NULL , ord INT(11) NOT NULL , artist_id VARCHAR(22)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL , PRIMARY KEY (id , ord) );"
    db_cursor.execute(createTable1)
    db_cursor.execute(createTable2)
    db_connect.commit()

    # query from non-1NF table albums
    sql_statements = "SELECT id , artists , artist_ids FROM tmp_albums;"
    db_cursor.execute(sql_statements)
    colnames = db_cursor.column_names
    results  = db_cursor.fetchall()

    running_total2 = 0
    rmb_to_commit  = 0
    for result in results: 
        _id         = str( result[0] )
        artist_ids  = getItem( str( result[2] )[1:-1] )
        count       = 1
        for artist_id in artist_ids:
            _artist = str( artist_id.strip() )
            _artist = _artist.replace("\\","\\\\").replace("\"","\\\"").replace("\'","\\\'")
            insertRow = "INSERT INTO tmp2 VALUES ( '{}' , {} , \"{}\" );".format( _id , count, _artist )
            #print( insertRow )
            db_cursor.execute( insertRow )
            count += 1
            running_total2 += 1
            if rmb_to_commit < 10000:
                rmb_to_commit  += 1
            else:
                rmb_to_commit = 0
                db_connect.commit()
    db_connect.commit()

    running_total1 = 0
    rmb_to_commit  = 0
    for result in results:
        _id         = str( result[0] )
        artists     = getItem( str( result[1] )[1:-1] )
        count       = 1
        for artist in artists:
            _artist = str( artist.strip() )
            _artist = _artist.replace("\\","\\\\").replace("\"","\\\"").replace("\'","\\\'")
            insertRow = "INSERT INTO tmp1 VALUES ( '{}' , {} , \"{}\" );".format( _id , count , _artist )
            #print( insertRow )
            db_cursor.execute( insertRow )
            count += 1
            running_total1 += 1
            if rmb_to_commit < 10000:
                rmb_to_commit  += 1
            else:
                rmb_to_commit = 0
                db_connect.commit()
    db_connect.commit()
    
    print(running_total1, " records inserted into tmp1")
    print(running_total2, " records inserted into tmp2")

    deleteTable1 = "DROP TABLE IF EXISTS normalized_song_lookup_artist;"
    deleteTable2 = "DROP TABLE IF EXISTS normalized_artists;"
    db_cursor.execute(deleteTable1)
    db_cursor.execute(deleteTable2)
    db_connect.commit()

    createTable1 = "CREATE TABLE normalized_song_lookup_artist AS ( SELECT DISTINCT id as song_id, artist_id  FROM tmp2 ORDER BY id,artist_id );"
    createTable2 = "CREATE TABLE normalized_artists AS ( SELECT DISTINCT artist_id , artist FROM tmp1 , tmp2 WHERE tmp1.id = tmp2.id AND tmp1.ord = tmp2.ord ORDER BY artist);"
    db_cursor.execute(createTable1)
    db_cursor.execute(createTable2)
    db_connect.commit()

#-------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # test = " 'N\'Dambi', 'Keb\' Mo\'' ,'a' , 'b, c','d ,e' , 'f , g' , 'h' , \"Scott Bradlee's Postmodern Jukebox\", 'Morgan James' , \"Da' T.R.U.T.H.\", 'Jin', 'The Ambassador' "
    # test = getItem( test )
   
    # for i in test:
    #     print(i)

    db_connect = connectMySQL()
    if db_connect.is_connected():
        
        build_Albums( db_connect )
        db_connect.close()

#-------------------------------------------------------------------------------------------------------------------------------------------