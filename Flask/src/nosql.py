from pymongo import MongoClient,ASCENDING,DESCENDING

class MongoDB:

    def __init__(self):       
        try:   
            self.mongoClient = self.connect()
            if self.mongoClient != None:
                self.mongoDatabase   = self.mongoClient["spotify"]
                self.mongoCollection = self.mongoDatabase["tmp_albums"]
                print( self.mongoCollection.name , type( self.mongoCollection ) )
                self.disconnect()
            else:
                raise ValueError('Unable to establish a connection to MongoDB database!')
        except Exception as err :
            raise err
        
    def __del__(self):
        self.disconnect()
    
    def connect(self):
        try:
            mongoClient = MongoClient("mongodb://admin:password@localhost:27019")
            return mongoClient
        except Exception as err :
            try:
                mongoClient = MongoClient("mongodb://admin:password@nosql:27019")
                return mongoClient
            except Exception as err :
                return None
    
    def disconnect(self):
        try:
            if self.mongoClient != None:
                self.mongoClient.close()
                self.mongoClient = None
                self.mongoDatabase = None
                self.mongoCollection = None
        except Exception as err:
            print(err)

    def FindArtistsAndAlbumsBySongName(self,songName):
        try:
            self.mongoClient = self.connect()
            if self.mongoClient != None:
                self.mongoDatabase   = self.mongoClient["spotify"]
                self.mongoCollection = self.mongoDatabase["tmp_albums"]
                query =  songName 
                results = self.mongoCollection.find( { 'name' : { '$regex' :  query } } )
                self.disconnect()
                counter = 0
                try:
                    for result in results:
                        counter += 1
                except Exception as err:
                    print(err)
                print( counter , " record(s) found!" )
                return results
            else:
                return None
        except Exception as err:
            print( err )
            return None

    def test(self):
        try:
            self.mongoClient = self.connect()
            self.mongoDatabase   = self.mongoClient["spotify"]
            print( self.mongoDatabase.list_collection_names() )
            self.disconnect()
            print("MongoDB Tested")
        except Exception as err:
            return print( err )
