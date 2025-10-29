from .conn import db
from mysql.connector import Error

class Login:
    def __init__(self):
        self.db = db
        
    def autenticar_usuario(self, usuario, matricula):
        connection = self.db.get_connection()
        connection = self.db.get_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexion'}
        
        try: 
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE usuario = %s AND matricula = %s"
            values = (usuario, matricula)
            cursor.execute(query, values)
            usuario_data = cursor.fetchone()
            
            if usuario_data:
                return {
                    'success': True,
                    'user': usuario_data
                }
            else:
                return {'success': False, 'error': 'Usuario o matricula incorrectos'}
        
        except Error as e:
            return {'success': False, 'error': str(e)}
        
        finally:
            cursor.close()
            self.db.close_connection()