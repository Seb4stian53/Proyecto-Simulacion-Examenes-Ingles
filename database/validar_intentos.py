from mysql.connector import Error

class IntentosManager:
    def __init__(self, db_connection):
        """
        Recibe una instancia de DatabaseConnection en lugar de usar una global.
        """
        self.db = db_connection

    def _obtener_intentos(self, nombre_tabla, matricula):
        """
        Método privado para no repetir código. Cuenta los intentos en cualquier tabla.
        """
        connection = self.db.get_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a la base de datos.'}

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT COUNT(*) as total FROM {nombre_tabla} WHERE matricula = %s"
            values = (matricula,)
            
            cursor.execute(query, values)
            resultado = cursor.fetchone()
            
            intentos = resultado['total'] if resultado else 0
            return {'success': True, 'intentos': intentos}

        except Error as e:
            return {'success': False, 'error': f"Error de SQL: {e}"}
        finally:
            if cursor:
                cursor.close()
            self.db.close_connection()

    def obtener_intentos_prueba(self, matricula):
        """
        Interfaz pública para obtener los intentos de la tabla 'pruebas'.
        """
        return self._obtener_intentos('pruebas', matricula)

    def obtener_intentos_examen(self, matricula):
        """
        Interfaz pública para obtener los intentos de la tabla 'examenes'.
        """
        return self._obtener_intentos('examenes', matricula)