import mysql.connector

class MySQL:

    def __init__(self):
        try:
            self.db_connect = None
            self.db_connect = mysql.connector.connect(user     = 'root'  , 
                                                      password = 'admin' ,
                                                      host     = 'csc2008.tplinkdns.com' ,
                                                      port     = '3307',
                                                      database = 'spotify')
            if self.db_connect.is_connected():
                self.db_cursor = self.db_connect.cursor()
                print("Connected to MySQL at port 3306!")
            else:
                raise ValueError('Unable to establish a connection to MySQL database!')
        except Exception as err :
            raise err
    def __del__(self):
        if self.db_connect != None:
            self.db_connect.close()
            self.db_connect = None
            print("MySQL Destroyed") 

    def query( self , sql_statements ):
        try:
            self.db_cursor.execute(sql_statements)
            colnames = self.db_cursor.column_names
            results  = self.db_cursor.fetchall()
            print(colnames)
            print(results)
            return(results)
        except Exception as e:
            print( e )

    def dbCursor( self  ):
        return(self.db_cursor)
    
    def dbCommit(self):
        return(self.db_connect.commit())
  

    def call( self , procName , args ):
        try:
            print(procName , args)
            self.db_cursor.callproc( procName ,  (args,) )
            results = self.db_cursor.stored_results()
            outputs = []
            for result in results:
                output = result.fetchall()
                print(output)
                outputs.extend(output)
            return(outputs)
        except Exception as e:
             print( e )