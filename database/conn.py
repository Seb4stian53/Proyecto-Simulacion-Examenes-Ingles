import mysql.connector
from mysql.connector import Error
import os

class DatabaseConnection:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = ''
    NAME = 'simulador_ingles_pruebas'
    PORT = 3306
    
    def __init__(self):
        self.connection = None
        
    def get_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                database=self.NAME,
                port=self.PORT
            )
            return self.connection
        except Error as e:
            print(f'Error al conectar a la base {e}')
            return None
        
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            
db = DatabaseConnection()