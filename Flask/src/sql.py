import mysql.connector

class MySQL:

    def __init__(self):
        try:
            self.db_connect = None
            self.db_connect = mysql.connector.connect(user     = 'root'  , 
                                                      password = 'admin' ,
                                                      host     = 'sql' ,
                                                      port     = '3306',
                                                      #host     = 'csc2008.tplinkdns.com' ,
                                                      #port     = '3307',
                                                      database = 'spotify')
        except Exception as err :
            try:
                self.db_connect = None
                self.db_connect = mysql.connector.connect(user     = 'root'  , 
                                                          password = 'admin' ,
                                                          host     = 'localhost' ,
                                                          port     = '3306',
                                                          #host     = 'csc2008.tplinkdns.com' ,
                                                          #port     = '3307',
                                                          database = 'spotify')
            except Exception as err :
                raise err
        
        if self.db_connect.is_connected():
            self.db_cursor = self.db_connect.cursor()
            print("Connected to MySQL at port 3306!")
        else:
            raise ValueError('Unable to establish a connection to MySQL database!')

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
  

    def call1( self , procName , arg1 ):
        try:
            print(procName , arg1)
            self.db_cursor.callproc( procName ,  (arg1,) )
            results = self.db_cursor.stored_results()
            outputs = []
            for result in results:
                output = result.fetchall()
                print(output)
                outputs.extend(output)
            return(outputs)
        except Exception as e:
             print( e )


    def call2( self , procName , arg1 , arg2 ):
        try:
            print(procName ,  arg1 , arg2)
            self.db_cursor.callproc( procName ,  (arg1,arg2,) )
            results = self.db_cursor.stored_results()
            outputs = []
            for result in results:
                output = result.fetchall()
                print(output)
                outputs.extend(output)
            return(outputs)
        except Exception as e:
             print( e )

    def call3( self , procName , arg1 , arg2 , arg3 ):
        try:
            print(procName ,  arg1 , arg2 , arg3)
            self.db_cursor.callproc( procName ,  (arg1,arg2,arg3,) )
            results = self.db_cursor.stored_results()
            outputs = []
            for result in results:
                output = result.fetchall()
                print(output)
                outputs.extend(output)
            return(outputs)
        except Exception as e:
             print( e )