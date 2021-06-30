import mysql.connector
from decouple import config

class DataBase():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = config('HOST'),
            user= config('USER'),
            password = config('PASS'),
            database = "centro_comercial"
        )
        self.cursor = self.mydb.cursor()
