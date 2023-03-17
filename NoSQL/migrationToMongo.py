import mysql.connector
import pymongo

# Connect to mysql
def connectMySQL():
    try:
        db_connect = None
        db_connect = mysql.connector.connect(user     = 'admin'   , 
                                             password = 'password'  ,
                                             host     = 'sql'    , # try either 'localhost' or 'sql'
                                             port     = '3307'   ,
                                             database = 'spotify')
        return db_connect
    except Exception as err :
        try:
            db_connect = None
            db_connect = mysql.connector.connect(user     = 'admin'      , 
                                                 password = 'password'     ,
                                                 host     = 'localhost' , # try either 'localhost' or 'sql'
                                                 port     = '3307'      ,
                                                 database = 'spotify'   )
            return db_connect
        except Exception as err :
            print( err )

# Connect to mongo
def connectMongo():
    try:
        db_connect = None
        db_connect = pymongo.MongoClient("mongodb://admin:password@127.0.0.1:27019/?authMechanism=DEFAULT")
        return db_connect
    except Exception as err :
        try:
            db_connect = None
            db_connect = pymongo.MongoClient("mongodb://admin:password@localhost:27019/?authMechanism=DEFAULT")
            return db_connect
        except Exception as err :
            print( err )


# Get data from MySQL Table
def getMySQLData(mydb, tableName):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM spotify." + tableName + ";")
    myresult = mycursor.fetchall()
    return myresult

# Push data to MongoDB
def pushMongoData(mydb, tableName, myresult):
    mycol = mydb[tableName]
    if len(myresult) > 0:
        x = mycol.insert_many(myresult)
        print(tableName + ": " + str(len(x.inserted_ids)))


# Main
if __name__ == "__main__":
    # Connect to MySQL
    mySqlDB = connectMySQL()
    # Connect to MongoDB
    myMongoClient = connectMongo()

    # Get Schema from MongoDB
    myMongoDB = myMongoClient["spotify"]

    # List of tables to migrate
    tableList = ["acousticness", "album", "danceability", "energy", "explicit","gender","instrumentalness","key","liveness","loudness","mode","normalized_artists", "normalized_song_lookup_artist","song","song_album","speechiness","tempo","valence"]

    # Loop through tables
    for table in tableList:
        # Get data from MySQL
        myresult = getMySQLData(mySqlDB, table)
        # Push data to MongoDB
        pushMongoData(myMongoDB, table, myresult)
