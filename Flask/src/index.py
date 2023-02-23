import os
from flask   import Flask, render_template
from mysql   import MySQL
from mongodb import MongoDB


mySQL   = MySQL()
mongoDB = MongoDB()
app     = Flask( __name__ )

@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    mySQL.test()
    mongoDB.test()

    app.run( host="0.0.0.0" , port=int("3000") , debug=True )