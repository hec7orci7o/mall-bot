import mysql.connector
import os
# from decouple import config

class DataBase():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host  = os.environ['HOST'],         # host = config('HOST'),
            user  = os.environ['USER'],         # user = config('USER'),
            password = os.environ['PASS'],      # password = config('PASS'),  
            database = os.environ['DATABASE']   # database = "centro_comercial"
        )
        self.cursor = self.mydb.cursor()
