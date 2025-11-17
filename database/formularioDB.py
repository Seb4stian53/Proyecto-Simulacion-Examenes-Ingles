import random
import pandas as pd
from mysql.connector import Error

class FormularioManager:
    def __init__(self, db_connection):
        """
        Recibe una instancia de la clase DatabaseConnection para usarla.
        """
        self.db = db_connection

    def generar_cuestionario_db(self, estructura_examen):
        """
        Obtiene una lista de preguntas aleatorias desde la base de datos.
        - estructura_examen: Diccionario {'categoria': cantidad, ...}
          Ej: {'beginner': 3, 'elementary': 3, ...}
        """
        connection = self.db.get_connection()
        if not connection:
            print("Error: No se pudo conectar a la base de datos.")
            return None

        cursor = None
        lista_completa_preguntas = []
        try:
            cursor = connection.cursor(dictionary=True)
            for categoria, cantidad in estructura_examen.items():
                # Nota: El nombre de la columna en la tabla 'preguntas' es 'categoria'
                query = "SELECT * FROM preguntas WHERE categoria = %s ORDER BY RAND() LIMIT %s"
                values = (categoria, cantidad)
                cursor.execute(query, values)
                
                preguntas_obtenidas = cursor.fetchall()
                if len(preguntas_obtenidas) < cantidad:
                    print(f"Advertencia: Se pidieron {cantidad} preguntas de '{categoria}', pero solo se encontraron {len(preguntas_obtenidas)}.")
                
                lista_completa_preguntas.extend(preguntas_obtenidas)
            
            random.shuffle(lista_completa_preguntas)
            return lista_completa_preguntas

        except Error as e:
            print(f"Error de base de datos al generar cuestionario: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            self.db.close_connection()

    def _guardar_resultado(self, nombre_tabla, matricula, resultados):
        """
        Método privado para guardar un resultado en la tabla especificada ('pruebas' o 'examenes').
        - resultados: Un diccionario con toda la información requerida por la tabla.
        """
        connection = self.db.get_connection()
        if not connection:
            print(f"Error: No hay conexión para guardar en la tabla {nombre_tabla}.")
            return False

        cursor = None
        try:
            cursor = connection.cursor()
            
            # Mapeamos los nombres de categoría a los nombres de columna de errores
            errores = resultados.get('errores_por_categoria', {})
            
            query = f"""
                INSERT INTO {nombre_tabla} (
                    matricula, calificacion, aciertos,
                    errores_beginner, errores_elementary, errores_preintermediate,
                    errores_intermediate, errores_upperintermediate, errores_advanced,
                    tiempo_total, categoria, fecha_realizacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            
            values = (
                matricula,
                resultados.get('calificacion', 0.0),
                resultados.get('aciertos', 0),
                errores.get('beginner', 0),
                errores.get('elementary', 0),
                errores.get('pre-intermediate', 0),
                errores.get('intermediate', 0),
                errores.get('upper-intermediate', 0),
                errores.get('advanced', 0),
                resultados.get('tiempo_total', 0),
                resultados.get('categoria_obtenida', 'N/A')
            )
            
            cursor.execute(query, values)
            connection.commit()
            print(f"Resultado guardado exitosamente en la tabla '{nombre_tabla}'.")
            return True

        except Error as e:
            print(f"Error al guardar resultado en '{nombre_tabla}': {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.db.close_connection()

    #def guardar_resultado_prueba(self, matricula, resultados):
    #    """
    #    Interfaz pública para guardar un resultado en la tabla 'pruebas'.
    #    """
    #    return self._guardar_resultado('pruebas', matricula, resultados)

    #def guardar_resultado_examen(self, matricula, resultados):
    #    """
    #    Interfaz pública para guardar un resultado en la tabla 'examenes'.
    #    """
    #    return self._guardar_resultado('examenes', matricula, resultados)
    
    def obtener_preguntas_como_dataframe(self):

        connection = self.db.get_connection()
        if not connection:
            print("Error: No se pudo conectar a la base de datos.")
            return None

        cursor = None
        try:
            query = "SELECT * FROM preguntas"
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            
            lista_preguntas = cursor.fetchall()
            
            if not lista_preguntas:
                return None
            
            # Convertimos la lista de diccionarios a un DataFrame de Pandas
            df = pd.DataFrame(lista_preguntas)
            # Renombramos las columnas de la BD a las que tu código espera
            df = df.rename(columns={'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'respuesta': 'respuestas'})
            df = df.fillna("")
            return df

        except Error as e:
            print(f"Error al obtener preguntas como DataFrame: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            self.db.close_connection()