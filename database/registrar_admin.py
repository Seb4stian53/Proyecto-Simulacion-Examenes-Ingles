from .conn import db
from mysql.connector import Error

class RegistrarAdmin:
    def __init__(self):
        self.db = db
    
    def registrar_admin(self, matricula, nombre, usuario):
        connection = self.db.get_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexion'}
        
        try: 
            cursor = connection.cursor()
            query = "INSERT INTO users (matricula, tipo_usuario, nombre, usuario) VALUES (%s, %s, %s, %s)"
            values = (matricula, 1, nombre, usuario)
            
            cursor.execute(query, values)
            connection.commit()
            return {'success': True, 'message': 'Administrador registrado exitosamente'}
        
        except Error as e:
            error_msg = str(e)
            if 'Duplicate entry' in error_msg:
                return {'success': False, 'error': 'La matricula o el usuario ya existen'}
            return {'success': False, 'error': f'Error al registrar administrador: {error_msg}'}
        
        finally:
            cursor.close()
            self.db.close_connection()