from mysql.connector import Error

class DashboardManager:
    def __init__(self, db_connection):
        self.db = db_connection

    # --- MÉTODOS PARA EL DASHBOARD DEL ALUMNO ---

    def obtener_stats_alumno(self, matricula):
        connection = self.db.get_connection()
        if not connection: return None
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            stats = {}

            # --- STATS DE PRUEBAS ---
            cursor.execute("SELECT COUNT(*) as total, AVG(calificacion) as promedio, MAX(calificacion) as mejor_nota FROM pruebas WHERE matricula = %s", (matricula,))
            res_pruebas = cursor.fetchone()
            stats['total_pruebas'] = res_pruebas['total'] or 0
            stats['promedio_pruebas'] = float(res_pruebas['promedio'] or 0.0)
            stats['mejor_nota_prueba'] = float(res_pruebas['mejor_nota'] or 0.0) # <-- NUEVO KPI

            # Nivel más común en Pruebas
            cursor.execute("SELECT categoria, COUNT(*) as cuenta FROM pruebas WHERE matricula = %s GROUP BY categoria ORDER BY cuenta DESC LIMIT 1", (matricula,))
            res_nivel_comun_p = cursor.fetchone()
            stats['nivel_comun_prueba'] = res_nivel_comun_p['categoria'] if res_nivel_comun_p else 'N/A' # <-- NUEVO KPI

            # Errores por categoría en Pruebas (para la nueva gráfica)
            query_errores_p = """
                SELECT 
                    SUM(errores_beginner) as beginner, SUM(errores_elementary) as elementary,
                    SUM(errores_preintermediate) as 'pre-intermediate', SUM(errores_intermediate) as intermediate,
                    SUM(errores_upperintermediate) as 'upper-intermediate', SUM(errores_advanced) as advanced
                FROM pruebas WHERE matricula = %s
            """
            cursor.execute(query_errores_p, (matricula,))
            res_errores_p = cursor.fetchone()
            stats['errores_por_categoria_pruebas'] = {
                cat: int(val) if val else 0 for cat, val in res_errores_p.items()
            } if res_errores_p else {} # <-- NUEVOS DATOS PARA GRÁFICA

            # --- STATS DE EXÁMENES ---
            cursor.execute("SELECT COUNT(*) as total_examenes, MAX(calificacion) as mejor_nota FROM examenes WHERE matricula = %s", (matricula,))
            res_examenes_max = cursor.fetchone()
            stats['total_examenes'] = res_examenes_max['total_examenes'] or 0
            stats['mejor_nota_examen'] = float(res_examenes_max['mejor_nota'] or 0.0)

            cursor.execute("SELECT categoria, COUNT(*) as cuenta FROM examenes WHERE matricula = %s GROUP BY categoria ORDER BY cuenta DESC LIMIT 1", (matricula,))
            res_nivel_comun = cursor.fetchone()
            stats['nivel_comun_examen'] = res_nivel_comun['categoria'] if res_nivel_comun else 'N/A'

            # Errores por categoría en Exámenes (se mantiene igual)
            query_errores_examenes = """
                SELECT 
                    SUM(errores_beginner) as beginner, SUM(errores_elementary) as elementary,
                    SUM(errores_preintermediate) as 'pre-intermediate', SUM(errores_intermediate) as intermediate,
                    SUM(errores_upperintermediate) as 'upper-intermediate', SUM(errores_advanced) as advanced
                FROM examenes WHERE matricula = %s
            """
            cursor.execute(query_errores_examenes, (matricula,))
            res_errores_examenes = cursor.fetchone()
            stats['errores_por_categoria_examenes'] = {
                cat: int(val) if val else 0 for cat, val in res_errores_examenes.items()
            } if res_errores_examenes else {}
            
            return stats
        except Error as e:
            print(f"Error al obtener stats del alumno: {e}")
            return None
        finally:
            if cursor: cursor.close()
            self.db.close_connection()
            
    # --- MÉTODOS PARA EL DASHBOARD DEL ADMINISTRADOR ---
    
    def obtener_stats_admin(self):
        connection = self.db.get_connection()
        if not connection: return None
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            stats = {}

            # 1. Stats Generales de Pruebas (Sin cambios)
            cursor.execute("SELECT COUNT(*) as total, AVG(calificacion) as promedio FROM pruebas")
            res_pruebas = cursor.fetchone()
            stats['total_pruebas_global'] = res_pruebas['total'] or 0
            stats['promedio_pruebas_global'] = float(res_pruebas['promedio'] or 0.0)
            
            # 2. Stats Generales de Exámenes (Sin cambios)
            cursor.execute("SELECT AVG(calificacion) as promedio, (SUM(CASE WHEN calificacion >= 70 THEN 1 ELSE 0 END) / COUNT(*)) * 100 as tasa_aprobacion FROM examenes")
            res_examenes = cursor.fetchone()
            stats['promedio_examenes_global'] = float(res_examenes['promedio'] or 0.0)
            stats['tasa_aprobacion_global'] = float(res_examenes['tasa_aprobacion'] or 0.0)
            
            # --- NUEVAS CONSULTAS PARA GRÁFICAS DE ADMIN ---

            # 3. Datos para la gráfica de barras de niveles en PRUEBAS
            cursor.execute("SELECT categoria, COUNT(*) as cuenta FROM pruebas WHERE categoria IS NOT NULL GROUP BY categoria")
            stats['distribucion_niveles_pruebas'] = cursor.fetchall()

            # 4. Datos para la gráfica de barras de niveles en EXÁMENES
            cursor.execute("SELECT categoria, COUNT(*) as cuenta FROM examenes WHERE categoria IS NOT NULL GROUP BY categoria")
            stats['distribucion_niveles_examenes'] = cursor.fetchall()

            # 5. Datos para la gráfica de pastel de errores en PRUEBAS
            query_errores_p_global = """
                SELECT 
                    SUM(errores_beginner) as beginner, SUM(errores_elementary) as elementary,
                    SUM(errores_preintermediate) as 'pre-intermediate', SUM(errores_intermediate) as intermediate,
                    SUM(errores_upperintermediate) as 'upper-intermediate', SUM(errores_advanced) as advanced
                FROM pruebas
            """
            cursor.execute(query_errores_p_global)
            res_errores_p = cursor.fetchone()
            stats['total_errores_categoria_pruebas'] = {
                cat: int(val) if val else 0 for cat, val in res_errores_p.items()
            } if res_errores_p else {}

            # 6. Datos para la gráfica de pastel de errores en EXÁMENES
            query_errores_e_global = """
                SELECT 
                    SUM(errores_beginner) as beginner, SUM(errores_elementary) as elementary,
                    SUM(errores_preintermediate) as 'pre-intermediate', SUM(errores_intermediate) as intermediate,
                    SUM(errores_upperintermediate) as 'upper-intermediate', SUM(errores_advanced) as advanced
                FROM examenes
            """
            cursor.execute(query_errores_e_global)
            res_errores_e = cursor.fetchone()
            stats['total_errores_categoria_examenes'] = {
                cat: int(val) if val else 0 for cat, val in res_errores_e.items()
            } if res_errores_e else {}

            return stats
        except Error as e:
            print(f"Error al obtener stats de admin: {e}")
            return None
        finally:
            if cursor: cursor.close()
            self.db.close_connection()
            
    def obtener_historial_alumno(self, matricula):
        """
        Obtiene una lista con el resumen de todas las pruebas y exámenes de un alumno.
        """
        connection = self.db.get_connection()
        if not connection: return None
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Usamos UNION ALL para combinar los resultados de ambas tablas en una sola consulta
            query = """
                (SELECT id_prueba as id, 'Prueba' as tipo, calificacion, fecha_realizacion 
                 FROM pruebas WHERE matricula = %s)
                UNION ALL
                (SELECT id_examen as id, 'Examen' as tipo, calificacion, fecha_realizacion 
                 FROM examenes WHERE matricula = %s)
                ORDER BY fecha_realizacion DESC
            """
            values = (matricula, matricula)
            cursor.execute(query, values)
            historial = cursor.fetchall()
            return historial

        except Error as e:
            print(f"Error al obtener el historial del alumno: {e}")
            return None
        finally:
            if cursor: cursor.close()
            self.db.close_connection()

    def obtener_detalle_evaluacion(self, tipo_evaluacion, id_evaluacion):
        """
        Obtiene todas las preguntas, respuestas de usuario y correctas para una
        evaluación específica (prueba o examen).
        """
        # Determinar qué tablas de detalle usar basándose en el tipo
        if tipo_evaluacion == 'Prueba':
            tabla_detalle = 'detalle_pruebas'
            col_id = 'id_prueba'
        elif tipo_evaluacion == 'Examen':
            tabla_detalle = 'detalle_examenes'
            col_id = 'id_examen'
        else:
            return None

        connection = self.db.get_connection()
        if not connection: return None
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            # La consulta JOIN nos trae toda la información que necesitamos de una vez
            query = f"""
                SELECT p.pregunta, p.a, p.b, p.c, p.d, p.respuesta as respuesta_correcta, 
                       d.respuesta_usuario, d.es_correcta
                FROM {tabla_detalle} d
                JOIN preguntas p ON d.id_pregunta = p.id_pregunta
                WHERE d.{col_id} = %s
            """
            values = (id_evaluacion,)
            cursor.execute(query, values)
            detalle = cursor.fetchall()
            return detalle

        except Error as e:
            print(f"Error al obtener el detalle de la evaluación: {e}")
            return None
        finally:
            if cursor: cursor.close()
            self.db.close_connection()