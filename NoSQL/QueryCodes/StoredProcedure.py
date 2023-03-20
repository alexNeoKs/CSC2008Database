import pymongo

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

# Find Songs And Artists By Album Name (Function: MongoDB)
def FindSongsAndArtistsByAlbumName(mongoClient, albumName):
    if (mongoClient == None or albumName == ""):
        return None
    return list(mongoClient['spotify']['album'].aggregate([
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

# Find Artists And Albums By Song Name (Function: MongoDB)
def FindArtistsAndAlbumsBySongName(mongoClient, songName):
    if (mongoClient == None or songName == ""):
        return None
    return list (mongoClient['spotify']['song'].aggregate([
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

# Find Songs And Albums By Artist Name (Function: MongoDB)
def FindSongsAndAlbumsByArtistName(mongoClient, artistName):
    if (mongoClient == None or artistName == ""):
        return None
    return list(mongoClient['spotify']['artist'].aggregate([
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


# Main
if __name__ == "__main__":
    # Connect to MongoDB
    myMongoClient = connectMongo()

    # Get Schema from MongoDB
    myMongoDB = myMongoClient["spotify"]
    # Get collection count
    print("MongoDB Collection Count: " + str(len(myMongoDB.list_collection_names())))

    result = FindSongsAndAlbumsByArtistName(myMongoClient,"Maroon")
    print(result)
    print(len(result))


    myMongoClient.close()
