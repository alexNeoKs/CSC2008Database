from flask   import Flask
from mysql   import MySQL
from mongodb import MongoDB

mySQL   = MySQL()
mongoDB = MongoDB()
app     = Flask(__name__)

@app.route("/")
def run():
    return "{\"message\":\"Hello World!!!\"}"


if __name__ == "__main__":
    mySQL.test()
    mySQL.test()

    app.run( host="0.0.0.0" , port=int("3000") , debug=True )