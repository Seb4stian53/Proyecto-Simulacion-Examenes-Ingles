from .conn import db
from mysql.connector import Error



class alumnos_querys:
    def __init__(self):
        self.db = db

    def enviar_formulario(self, matricula, calificacion, aciertos, errores_begginer, errores_elementary, errores_preintermediate, errores_intermediate, errores_upperintermediate, errores_advanced, tiempo_total, categoria):
        connection = self.db.get_connection()
        if connection is None:
            print("Error en la conexion")
            return
    
        try:
            cursor = connection.cursor()
            query = "INSERT INTO pruebas(matricula, calificacion, aciertos, errores_begginer, errores_elementary, errores_preintermediate, errores_intermediate, errores_upperintermediate, errores_advanced, tiempo_total, categoria) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = ( matricula, calificacion, aciertos, errores_begginer, errores_elementary, errores_preintermediate, errores_intermediate, errores_upperintermediate, errores_advanced, tiempo_total, categoria)
            #query = str("INSERT INTO pruebas ("+matricula+","+ calificacion+","+aciertos+","+errores_begginer+","+errores_elementary+","+errores_preintermediate+","+errores_intermediate+","+errores_upperintermediate+","+errores_advanced+","+tiempo_total+","+categoria+","+fecha_realizacion)
            cursor.execute(query, values)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            error_msg = str(e)
            if 'Duplicate entry' in error_msg:
                return {'success': False, 'error': 'La matricula o el usuario ya existen'}
            return {'success': False, 'error': f'Error al registrar usuario: {error_msg}'}
        
        finally:
            cursor.close()
            self.db.close_connection()

    enviar_formulario(1,1,1,1,1,1,1,1,1,1,1)

