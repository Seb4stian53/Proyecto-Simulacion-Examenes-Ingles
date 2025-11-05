from .conn import db
from mysql.connector import Error

class Alumno_querys:
    def __init__(self, db_conn):
        self.db = db_conn

    def enviar_formulario(self, matricula, calificacion, aciertos,
                          errores_begginer, errores_elementary, errores_preintermediate,
                          errores_intermediate, errores_upperintermediate, errores_advanced,
                          tiempo_total, categoria):
        connection = self.db.get_connection()
        if connection is None:
            print("Error en la conexion")
            return {'success': False, 'error': 'No hay conexion'}

        try:
            cursor = connection.cursor()
            query = ("INSERT INTO pruebas(matricula, calificacion, aciertos, "
                     "errores_begginer, errores_elementary, errores_preintermediate, "
                     "errores_intermediate, errores_upperintermediate, errores_advanced, "
                     "tiempo_total, categoria) "
                     "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            values = (matricula, calificacion, aciertos,
                      errores_begginer, errores_elementary, errores_preintermediate,
                      errores_intermediate, errores_upperintermediate, errores_advanced,
                      tiempo_total, categoria)
            cursor.execute(query, values)
            connection.commit()                # <- IMPORTANTE para INSERT
            return {'success': True, 'lastrowid': cursor.lastrowid}
        except Error as e:
            error_msg = str(e)
            if 'Duplicate entry' in error_msg:
                return {'success': False, 'error': 'La matricula o el usuario ya existen'}
            return {'success': False, 'error': f'Error al registrar usuario: {error_msg}'}
        finally:
            cursor.close()
            self.db.close_connection()

if __name__ == "__main__":
    handler = Alumno_querys(db)                 # crea instancia con el objeto db
    resultado = handler.enviar_formulario(1,1,1,1,1,1,1,1,1,1,"A")  # incluir categoria
    print(resultado)
