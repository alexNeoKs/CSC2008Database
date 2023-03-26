from pymongo import MongoClient,ASCENDING,DESCENDING

class MongoDB:

    def __init__(self):

        try:
            self.mongoClient = None
            self.mongoClient = MongoClient("mongodb://admin:password@localhost:27019/?authMechanism=DEFAULT")
        except Exception as err :
            try:
                self.mongoClient = None
                self.mongoClient = MongoClient("mongodb://admin:password@127.0.0.1:27019/?authMechanism=DEFAULT")
            except Exception as err :
                raise err
            
        self.mongoDatabase   = self.mongoClient["spotify"]
        self.mongoCollection = self.mongoDatabase["tmp_albums"]
        print( self.mongoCollection.name , type( self.mongoCollection ) )


    def FindArtistsAndAlbumsBySongName(self,songName):
        results = self.mongoCollection.find( { 'name' : { '$regex' : '/'+songName+'/i' } } )
        for result in results:
            print(result , " : ", results[result])


    def test(self):
        # results = self.mongoCollection.find_one({})
        # for result in results:
        #     print(result , " : ", results[result])
        print("testing FindArtistsAndAlbumsBySongName('Piano Man')")
        self.FindArtistsAndAlbumsBySongName("Piano Man")
        print("finished testing")
        print("MongoDB Tested")

