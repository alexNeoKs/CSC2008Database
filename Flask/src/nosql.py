from pymongo import MongoClient,ASCENDING,DESCENDING

class MongoDB:

    def __init__(self):       
        try:   
            self.mongoClient = self.connect()
            if self.mongoClient != None:
                self.mongoDatabase   = self.mongoClient["spotify"]
                self.mongoCollection = self.mongoDatabase["tmp_albums"]
                print( self.mongoCollection.name , type( self.mongoCollection ) )
            else:
                raise ValueError('Unable to establish a connection to MongoDB database!')
        except Exception as err :
            raise err
        
    def __del__(self):
        self.disconnect()
    
    def connect(self):
        try:
            mongoClient = MongoClient("mongodb://admin:password@nosql:27017")
            return mongoClient
        except Exception as err :
            try:
                mongoClient = MongoClient("mongodb://admin:password@host.docker.internal:27017")
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

    # def FindArtistsAndAlbumsBySongName(self,songName):
    #     try:
    #         if self.mongoClient != None:
    #             query =  songName 
    #             results = self.mongoCollection.find( { 'name' : { '$regex' :  query } } )
    #             counter = 0
    #             try:
    #                 for result in results:
    #                     counter += 1
    #                     for field in result:
    #                         print( field , " : " , result[field] )
    #             except Exception as err:
    #                 print(err)
    #             print( counter , " record(s) found!" )
    #             return results
    #         else:
    #             return None
    #     except Exception as err:
    #         print( err )
    #         return None

    def FindArtistsAndAlbumsBySongName(self, songName):
        if (self.mongoClient == None or songName == ""):
            return None
        return list (self.mongoClient['spotify']['song'].aggregate([
            {
                '$match': {
                    'name': {"$regex":songName}
                }
            }, {
                '$lookup': {
                    'from': 'song_album', 
                    'localField': 'song_id', 
                    'foreignField': 'song_id', 
                    'as': 'result'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'song_id': 1, 
                    'name': 1, 
                    'year': 1, 
                    'album_id': {
                        '$map': {
                            'input': '$result', 
                            'as': 'song', 
                            'in': '$$song.album_id'
                        }
                    }, 
                    'track_number': {
                        '$map': {
                            'input': '$result', 
                            'as': 'song', 
                            'in': '$$song.track_number'
                        }
                    }, 
                    'disc_number': {
                        '$map': {
                            'input': '$result', 
                            'as': 'song', 
                            'in': '$$song.disc_number'
                        }
                    }
                }
            }, {
                '$lookup': {
                    'from': 'album', 
                    'localField': 'album_id', 
                    'foreignField': 'album_id', 
                    'as': 'album'
                }
            }, {
                '$lookup': {
                    'from': 'song_artist', 
                    'localField': 'song_id', 
                    'foreignField': 'song_id', 
                    'as': 'artist'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'song_id': 1, 
                    'name': 1, 
                    'year': 1, 
                    'album_id': 1, 
                    'track_number': 1, 
                    'disc_number': 1, 
                    'album': {
                        '$map': {
                            'input': '$album', 
                            'as': 'album', 
                            'in': '$$album.album'
                        }
                    }, 
                    'artist': {
                        '$map': {
                            'input': '$artist', 
                            'as': 'artist', 
                            'in': '$$artist.artist_id'
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$artist'
                }
            }, {
                '$lookup': {
                    'from': 'artist', 
                    'localField': 'artist', 
                    'foreignField': 'artist_id', 
                    'as': 'artist'
                }
            }, {
                '$project': {
                    'name': 1, 
                    'year': 1, 
                    'track_number': 1, 
                    'disc_number': 1, 
                    'album': 1, 
                    'artist': {
                        '$map': {
                            'input': '$artist', 
                            'as': 'artist', 
                            'in': '$$artist.artist'
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$disc_number'
                }
            }, {
                '$unwind': {
                    'path': '$track_number'
                }
            }, {
                '$unwind': {
                    'path': '$album'
                }
            }, {
                '$unwind': {
                    'path': '$artist'
                }
            }
        ])
        )

    def FindSongsAndAlbumsByArtistName(self, artistName):
        if (self.mongoClient == None or artistName == ""):
            return None
        return list(self.mongoClient['spotify']['artist'].aggregate([
            {
                '$match': {
                    'artist': artistName
                }
            }, {
                '$lookup': {
                    'from': 'song_artist', 
                    'localField': 'artist_id', 
                    'foreignField': 'artist_id', 
                    'as': 'artist_song_list'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'artist_id': 1, 
                    'artist': 1, 
                    'song_id': {
                        '$map': {
                            'input': '$artist_song_list', 
                            'as': 'song', 
                            'in': '$$song.song_id'
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$song_id'
                }
            }, {
                '$lookup': {
                    'from': 'song', 
                    'localField': 'song_id', 
                    'foreignField': 'song_id', 
                    'as': 'song_detail'
                }
            }, {
                '$project': {
                    'artist_id': 1, 
                    'artist': 1, 
                    'song_id': {
                        '$map': {
                            'input': '$song_detail', 
                            'as': 'song', 
                            'in': '$$song.song_id'
                        }
                    }, 
                    'name': {
                        '$map': {
                            'input': '$song_detail', 
                            'as': 'song', 
                            'in': '$$song.name'
                        }
                    }, 
                    'year': {
                        '$map': {
                            'input': '$song_detail', 
                            'as': 'song', 
                            'in': '$$song.year'
                        }
                    }
                }
            }, {
                '$lookup': {
                    'from': 'song_album', 
                    'localField': 'song_id', 
                    'foreignField': 'song_id', 
                    'as': 'album_id'
                }
            }, {
                '$project': {
                    'artist_id': 1, 
                    'artist': 1, 
                    'song_id': 1, 
                    'name': 1, 
                    'year': 1, 
                    'album_id': {
                        '$map': {
                            'input': '$album_id', 
                            'as': 'album', 
                            'in': '$$album.album_id'
                        }
                    }, 
                    'track_number': {
                        '$map': {
                            'input': '$album_id', 
                            'as': 'album', 
                            'in': '$$album.track_number'
                        }
                    }, 
                    'disc_number': {
                        '$map': {
                            'input': '$album_id', 
                            'as': 'album', 
                            'in': '$$album.disc_number'
                        }
                    }
                }
            }, {
                '$lookup': {
                    'from': 'album', 
                    'localField': 'album_id', 
                    'foreignField': 'album_id', 
                    'as': 'album_id'
                }
            }, {
                '$project': {
                    'artist': 1, 
                    'name': 1, 
                    'year': 1, 
                    'album': {
                        '$map': {
                            'input': '$album_id', 
                            'as': 'album', 
                            'in': '$$album.album'
                        }
                    }, 
                    'track_number': 1, 
                    'disc_number': 1
                }
            }, {
                '$unwind': {
                    'path': '$name'
                }
            }, {
                '$unwind': {
                    'path': '$year'
                }
            }, {
                '$unwind': {
                    'path': '$track_number'
                }
            }, {
                '$unwind': {
                    'path': '$disc_number'
                }
            }, {
                '$unwind': {
                    'path': '$album'
                }
            }
        ])
        )

    def FindSongsAndArtistsByAlbumName(self, albumName):
        if (self.mongoClient == None or albumName == ""):
            return None
        return list(self.mongoClient['spotify']['album'].aggregate([
            {
                '$match': {
                    'album': {"$regex":albumName}
                }
            }, {
                '$lookup': {
                    'from': 'song_album', 
                    'localField': 'album_id', 
                    'foreignField': 'album_id', 
                    'as': 'song_detail'
                }
            }, {
                '$unwind': {
                    'path': '$song_detail'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'album': 1, 
                    'song_id': '$song_detail.song_id', 
                    'track_number': '$song_detail.track_number', 
                    'disc_number': '$song_detail.disc_number'
                }
            }, {
                '$lookup': {
                    'from': 'song_artist', 
                    'localField': 'song_id', 
                    'foreignField': 'song_id', 
                    'as': 'artist_id'
                }
            }, {
                '$unwind': {
                    'path': '$artist_id'
                }
            }, {
                '$project': {
                    'song_id': 1, 
                    'album': 1, 
                    'track_number': 1, 
                    'disc_number': 1, 
                    'artist_id': '$artist_id.artist_id'
                }
            }, {
                '$lookup': {
                    'from': 'artist', 
                    'localField': 'artist_id', 
                    'foreignField': 'artist_id', 
                    'as': 'artist'
                }
            }, {
                '$lookup': {
                    'from': 'song', 
                    'localField': 'song_id', 
                    'foreignField': 'song_id', 
                    'as': 'name'
                }
            }, {
                '$project': {
                    'name': {
                        '$map': {
                            'input': '$name', 
                            'as': 'song', 
                            'in': '$$song.name'
                        }
                    }, 
                    'year': {
                        '$map': {
                            'input': '$name', 
                            'as': 'song', 
                            'in': '$$song.year'
                        }
                    }, 
                    'disc_number': 1, 
                    'track_number': 1, 
                    'album': 1, 
                    'artist': {
                        '$map': {
                            'input': '$artist', 
                            'as': 'artist', 
                            'in': '$$artist.artist'
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$artist'
                }
            }, {
                '$unwind': {
                    'path': '$name'
                }
            }, {
                '$unwind': {
                    'path': '$year'
                }
            }
        ])
        )

    def test(self):
        try:
            
            result = self.FindSongsAndAlbumsByArtistName("Maroon")
            print(result)
            print("MongoDB Tested")
        except Exception as err:
            return print( err )
