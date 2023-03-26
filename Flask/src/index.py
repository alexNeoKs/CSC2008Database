import os
import numpy  as np
import pandas as pd
import datetime
from   flask  import Flask, render_template, jsonify, request, redirect,url_for
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
    def index():
        return redirect(url_for('login'))
    
    @app.route("/login", methods = ['GET','POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            mySQL.dbCursor().execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
            account = mySQL.dbCursor().fetchone()
            if account:
                return redirect(url_for('home'))

            else:
                pass

        return render_template('login.html')
    
    @app.route("/signup", methods = ['GET','POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            password_repeat = request.form['password-repeat']
            if(password == password_repeat):
                print("Reach")
                mySQL.dbCursor().execute("INSERT INTO accounts (username,password) VALUES (%s,%s)", (username, password))
                mySQL.dbCommit()
                return redirect(url_for('login'))
            else:
                print("Reach no")
                return render_template('signup.html')

        return render_template('signup.html')
    
    @app.route("/home")
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
        if "arg2" in request.json and "arg1" in request.json and "procName" in request.json:
            procName = request.json['procName']
            arg1     = request.json['arg1']
            arg2     = request.json['arg2']
            startTime = datetime.datetime.now()
            results  = mySQL.call2( procName, arg1 , arg2 )
            endTime = datetime.datetime.now()
            deltaTime = endTime - startTime
            ms        = int(deltaTime.total_seconds() * 1000)
            return { 'results' : results , 'elapsed' : ms }
        elif "arg1" in request.json and "procName" in request.json:
            procName = request.json['procName']
            arg1     = request.json['arg1']
            startTime = datetime.datetime.now()
            results  = mySQL.call1( procName, arg1 )
            endTime = datetime.datetime.now()
            deltaTime = endTime - startTime
            ms        = int(deltaTime.total_seconds() * 1000)
            return { 'results' : results , 'elapsed' : ms }
        else:
            return { 'results' : "" , 'elapsed' : 0 }


    @app.route("/nosql/call", methods=["POST"])
    def nosql_call():
        if "arg2" in request.json and "arg1" in request.json and "procName" in request.json:
            procName = request.json['procName']
            arg1     = request.json['arg1']
            arg2     = request.json['arg2']
            # do nothing
        elif "arg1" in request.json and "procName" in request.json:
            procName = request.json['procName']
            arg1     = request.json['arg1']
            results = ""
            try:
                if   "FindArtistsAndAlbumsBySongName" in procName:
                    startTime = datetime.datetime.now()
                    results = mongoDB.FindArtistsAndAlbumsBySongName(arg1)
                    endTime = datetime.datetime.now()
                    deltaTime = endTime - startTime
                    ms        = int(deltaTime.total_seconds() * 1000)
                    return  { 'results' : results , 'elapsed' : ms }
                elif "FindSongsAndAlbumsByArtistName" in procName:
                    startTime = datetime.datetime.now()
                    results = mongoDB.FindSongsAndAlbumsByArtistName(arg1)
                    endTime = datetime.datetime.now()
                    deltaTime = endTime - startTime
                    ms        = int(deltaTime.total_seconds() * 1000)
                    return  { 'results' : results , 'elapsed' : ms }
                elif "FindSongsAndArtistsByAlbumName" in procName:
                    startTime = datetime.datetime.now()
                    results = mongoDB.FindSongsAndArtistsByAlbumName(arg1)
                    endTime = datetime.datetime.now()
                    deltaTime = endTime - startTime
                    ms        = int(deltaTime.total_seconds() * 1000)
                    return  { 'results' : results , 'elapsed' : ms }
                else:
                    return  { 'results' : "" , 'elapsed' : 0  }
            except Exception as err:
                print(err)
                return { 'results' : "" , 'elapsed' : 0 }

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