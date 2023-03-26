import mysql.connector
import pymongo

# Connect to mysql
def connectMySQL():
    try:
        db_connect = None
        db_connect = mysql.connector.connect(user     = 'admin'   , #deafult is root
                                             password = 'password'  ,
                                             host     = 'sql'    , # try either 'localhost' or 'sql'
                                             port     = '3306'   , #default is 3306
                                             database = 'spotify')
        return db_connect
    except Exception as err :
        try:
            db_connect = None
            db_connect = mysql.connector.connect(user     = 'admin'      , #deafult is root
                                                 password = 'password'     ,
                                                 host     = 'localhost' , # try either 'localhost' or 'sql'
                                                 port     = '3306'      ,  #default is 3306
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
        # Check if the "song_id" field exists in a document
        song_id = mycol.find_one({"song_id": {"$exists": True}})
        if song_id:
            mycol.create_index([("song_id",1)])
            print("Indexed column: 'song_id'")
        # Check if the "album_id" field exists in a document
        album_id = mycol.find_one({"album_id": {"$exists": True}})
        if album_id:
            mycol.create_index([("album_id",1)])
            print("Indexed column: 'album_id'")
        # Check if the "artist_id" field exists in a document
        artist_id = mycol.find_one({"artist_id": {"$exists": True}})
        if artist_id:
            mycol.create_index([("artist_id",1)])
            print("Indexed column: 'artist_id'")
        # Check if the "artist" field exists in a document
        artist = mycol.find_one({"artist": {"$exists": True}})
        if artist:
            mycol.create_index([("artist",1)])
            print("Indexed column: 'artist'")
        id = mycol.find_one({"id": {"$exists": True}})
        if id:
            mycol.create_index([("id",1)])
            print("Indexed column: 'id'")

# Main
if __name__ == "__main__":
    # Connect to MySQL
    mySqlDB = connectMySQL()
    # Connect to MongoDB
    myMongoClient = connectMongo()

    # Drop database called spotify
    #myMongoClient.drop_database("spotify")

    # Get Schema from MongoDB
    myMongoDB = myMongoClient["spotify"]

    # Get collection count
    print("MongoDB Collection Count: " + str(len(myMongoDB.list_collection_names())))

    # List of tables to migrate
    tableList = ["tmp_albums"]

    # Loop through tables
    for table in tableList:
        # Get data from MySQL
        myresult = getMySQLData(mySqlDB, table)
        # Push data to MongoDB
        pushMongoData(myMongoDB, table, myresult)

    #Print complete message
    print("Migration Complete")
    print("MongoDB Collection Count: " + str(len(myMongoDB.list_collection_names())))

    #close all connection
    mySqlDB.close()
    myMongoClient.close()
