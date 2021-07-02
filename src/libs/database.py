import os
import mysql.connector

class DataBase():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host  = os.environ['HOST'],         
            user  = os.environ['USER'],         
            password = os.environ['PASS'],      
            database = os.environ['DATABASE']   
        )
        self.cursor = self.mydb.cursor()

    def __del__(self):
        self.cursor.close()
        self.mydb.close()
