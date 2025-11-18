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

    def _reemplazar_ultimo_intento(self, tipo_intento, matricula, resultados):
        """
        Método privado y TRANSACCIONAL que borra el último intento de un usuario
        (si existe) y guarda el nuevo con su detalle.
        """
        # Determinar nombres de tablas y columnas según el tipo
        if tipo_intento == 'prueba':
            tabla_resumen, tabla_detalle = 'pruebas', 'detalle_pruebas'
            id_col_resumen, id_col_detalle = 'id_prueba', 'id_detalle_prueba'
        elif tipo_intento == 'examen':
            tabla_resumen, tabla_detalle = 'examenes', 'detalle_examenes'
            id_col_resumen, id_col_detalle = 'id_examen', 'id_detalle_examen'
        else:
            return False

        connection = self.db.get_connection()
        if not connection:
            print(f"Error: No hay conexión para guardar el {tipo_intento}.")
            return False

        cursor = None
        try:
            cursor = connection.cursor()
            # --- INICIO DE LA TRANSACCIÓN ---
            connection.start_transaction()

            # 2. Insertar el nuevo resumen en la tabla principal (pruebas o examenes)
            errores = resultados.get('errores_por_categoria', {})
            query_resumen = f"""
                INSERT INTO {tabla_resumen} (
                    matricula, calificacion, aciertos,
                    errores_beginner, errores_elementary, errores_preintermediate,
                    errores_intermediate, errores_upperintermediate, errores_advanced,
                    tiempo_total, categoria, fecha_realizacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            values_resumen = (
                matricula, resultados.get('calificacion', 0.0), resultados.get('aciertos', 0),
                errores.get('beginner', 0), errores.get('elementary', 0),
                errores.get('pre-intermediate', 0), errores.get('intermediate', 0),
                errores.get('upper-intermediate', 0), errores.get('advanced', 0),
                resultados.get('tiempo_total', 0), resultados.get('categoria_obtenida', 'N/A')
            )
            cursor.execute(query_resumen, values_resumen)
            
            # 3. Obtener el ID del resumen que acabamos de insertar
            id_resumen_insertado = cursor.lastrowid
            
            # 4. Insertar cada pregunta en la tabla de detalle
            detalle_respuestas = resultados.get('detalle_respuestas', [])
            if detalle_respuestas:
                query_detalle = f"""
                    INSERT INTO {tabla_detalle} ({id_col_resumen}, id_pregunta, respuesta_usuario, es_correcta)
                    VALUES (%s, %s, %s, %s)
                """
                
                lista_valores_detalle = [
                    (id_resumen_insertado, d['id_pregunta'], d['respuesta_usuario'], d['es_correcta'])
                    for d in detalle_respuestas
                ]
                
                cursor.executemany(query_detalle, lista_valores_detalle)

            # --- Si todo salió bien, confirmar la transacción ---
            connection.commit()
            print(f"Nuevo intento de '{matricula}' guardado exitosamente en '{tabla_resumen}'.")
            return True

        except Error as e:
            # --- Si algo falló, revertir TODOS los cambios ---
            if connection:
                connection.rollback()
            print(f"Error en la transacción al guardar resultado: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.db.close_connection()

    def guardar_resultado_prueba(self, matricula, resultados):
        """
        Interfaz pública para guardar el último resultado en la tabla 'pruebas'.
        """
        return self._reemplazar_ultimo_intento('prueba', matricula, resultados)

    def guardar_resultado_examen(self, matricula, resultados):
        """
        Interfaz pública para guardar el último resultado en la tabla 'examenes'.
        """
        return self._reemplazar_ultimo_intento('examen', matricula, resultados) 
    
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