from .conn import db
from mysql.connector import Error

class Registrar:
    def __init__(self):
        self.db = db
    
    def registrar_usuario(self, matricula, tipo, nombre, usuario):
        connection = self.db.get_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexion'}
        
        try: 
        