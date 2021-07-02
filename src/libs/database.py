import mysql.connector

class DataBase():
    def __init__(self, host, user, passwd, db):
        self.mydb = mysql.connector.connect(
            host  = host,         
            user  = user,         
            password = passwd,      
            database = db   
        )
        self.cursor = self.mydb.cursor()

    def __del__(self):
        self.database.close()
                
