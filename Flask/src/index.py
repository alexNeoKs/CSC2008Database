import os
import numpy  as np
import pandas as pd
from   flask  import Flask, render_template, jsonify, request
from   sql    import MySQL
from   nosql  import MongoDB
try:
    mySQL = None
    mySQL = MySQL()
except Exception as err:
    print(err)
try:
    mongoDB = None
    mongoDB = MongoDB()
except Exception as err:
    print(err)
try:
    app  = None
    app  = Flask( __name__ )

    @app.route("/")
    def home():
        return render_template('index.html')
    
    @app.route("/addSong")
    def addSong():
        return render_template('addSong.html')
    
    @app.route("/searchSQLDatabase")
    def searchSQLDatabase():
        return render_template('searchSQLDatabase.html')
    
    # use this API to call MySQL stored procedure
    @app.route("/sql/call", methods=["POST"])
    def sql_call():
        procName = request.json['procName']
        args = request.json['args']
        results = mySQL.call( procName, args )
        return { 'results' : results }
    
    # FOR DEVELOPMENT / TESTING USE ONLY , 
    # use this API to pass SQL queries directly into MySQL 
    # do not use in production to avoid SQL injection!)
    @app.route("/sql/query", methods=["POST"])
    def sql_query():
        sql_statements = request.json['sql_statements']
        results = mySQL.query(sql_statements)
        return { 'results' : results }
    
    
except Exception as err:
    print(err)
if __name__ == "__main__":
    if mySQL is not None and mongoDB is not None and app is not None:
        mongoDB.test()
        arr = np.array([1, 2, 3, 4, 5])
        print(arr)
        print(type(arr))
        app.run( host="0.0.0.0" , port=int("3000") , debug=True )