import tkinter as tk
from tkinter import messagebox
import random

from database.conn import DatabaseConnection
from database.formularioDB import FormularioManager
from database.validar_intentos import IntentosManager
from database.dashboard import DashboardManager
from vistas.dashboard_alumno_view import DashboardAlumnoView
from vistas.prueba_view_og import PruebaViewOriginal

class AlumnoView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        db_conn = DatabaseConnection()
        self.formulario_manager = FormularioManager(db_conn)
        self.intentos_manager = IntentosManager(db_conn)
        self.dashboard_manager = DashboardManager(db_conn)

        self.user_data = {}
        self.create_widgets()
        
    def generar_lista_preguntas_20(self):
        num_preguntas = []
        num_preguntas.extend(random.sample(range(1, 10), 3))
        num_preguntas.extend(random.sample(range(11, 25), 3))
        num_preguntas.extend(random.sample(range(26, 40), 4))
        num_preguntas.extend(random.sample(range(41, 60), 5))
        num_preguntas.extend(random.sample(range(61, 70), 3))
        num_preguntas.extend(random.sample(range(71, 80), 2))
        random.shuffle(num_preguntas)
        return num_preguntas

    def generar_lista_preguntas_40(self):
        num_preguntas = []
        num_preguntas.extend(random.sample(range(1, 10), 6))
        num_preguntas.extend(random.sample(range(11, 25), 6))
        num_preguntas.extend(random.sample(range(26, 40), 8))
        num_preguntas.extend(random.sample(range(41, 60), 10))
        num_preguntas.extend(random.sample(range(61, 70), 6))
        num_preguntas.extend(random.sample(range(71, 80), 4))
        random.shuffle(num_preguntas)
        return num_preguntas

    def create_widgets(self):
        tk.Label(self, text="Panel de Alumno", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.welcome_label = tk.Label(self, text="", font=("Arial", 12))
        self.welcome_label.pack(pady=5)
        
        self.matricula_label = tk.Label(self, text="", font=("Arial", 10))
        self.matricula_label.pack(pady=(0, 20))
        
        tk.Button(self, text="Realizar Prueba (20 Preguntas)", command=self.realizarPrueba, width=30, height=2, font=("Arial", 10)).pack(pady=5)
        tk.Button(self, text="Realizar Examen (40 Preguntas)", command=self.realizarExamen, width=30, height=2, font=("Arial", 10)).pack(pady=5)
        tk.Button(self, text="Ver Mi Rendimiento", command=self.show_dashboard, 
                  width=30, height=2, font=("Arial", 10), bg="cornflowerblue", fg="white").pack(pady=5)

        tk.Button(self, text="Cerrar Sesión", command=self.logout, bg="tomato", fg="white").pack(side="bottom", pady=20)

    def set_user_data(self, user_data):
        self.user_data = user_data
        self.welcome_label.config(text=f"Bienvenido, {self.user_data.get('nombre', '')}")
        self.matricula_label.config(text=f"Matrícula: {self.user_data.get('matricula', '')}")

    def logout(self):
        self.user_data = {}
        self.welcome_label.config(text="")
        self.matricula_label.config(text="")
        self.controller.show_login_view()

    def realizarPrueba(self):
        # Identificar al alumno actual.
        matricula = self.user_data.get('matricula')
        if not matricula:
            messagebox.showerror("Error de Usuario", "No se pudo identificar la matrícula del alumno.")
            return

        # Validar si el alumno aún tiene intentos disponibles para la prueba.
        intentos_result = self.intentos_manager.obtener_intentos_prueba(matricula)
        if not intentos_result['success']:
            messagebox.showerror("Error de Base de Datos", intentos_result['error'])
            return
        
        LIMITE_PRUEBAS = 5
        if intentos_result.get('intentos', 0) >= LIMITE_PRUEBAS:
             messagebox.showwarning("Límite Alcanzado", f"Ya has alcanzado el límite de {LIMITE_PRUEBAS} intentos.")
             return

        # Cargar todas las preguntas desde la base de datos a un DataFrame.
        df_preguntas = self.formulario_manager.obtener_preguntas_como_dataframe()
        if df_preguntas is None:
            messagebox.showerror("Error", "No se pudieron cargar las preguntas desde la base de datos.")
            return

        # Generar la lista de números de preguntas específica para esta prueba.
        lista_preguntas_numeros = self.generar_lista_preguntas_20()

        # Definir la acción a realizar al finalizar la prueba (guardar los resultados).
        def on_prueba_complete(resultados):
            print("Guardando resultados de la prueba...")
            self.formulario_manager._guardar_resultado('pruebas', matricula, resultados)

        # Lanzar la ventana de la prueba con los datos y la acción final.
        PruebaViewOriginal(parent=self, controller=self.controller,
                             dataframe_preguntas=df_preguntas,
                             lista_numeros_preguntas=lista_preguntas_numeros,
                             on_complete_callback=on_prueba_complete)
                             
    def realizarExamen(self):
        matricula = self.user_data.get('matricula')
        if not matricula:
            messagebox.showerror("Error de Usuario", "No se pudo identificar la matrícula del alumno.")
            return

        intentos_result = self.intentos_manager.obtener_intentos_examen(matricula)
        if not intentos_result['success']:
            messagebox.showerror("Error de Base de Datos", intentos_result['error'])
            return
            
        LIMITE_EXAMENES = 2
        if intentos_result.get('intentos', 0) >= LIMITE_EXAMENES:
             messagebox.showwarning("Límite Alcanzado", f"Ya has alcanzado el límite de {LIMITE_EXAMENES} intentos.")
             return

        df_preguntas = self.formulario_manager.obtener_preguntas_como_dataframe()
        if df_preguntas is None:
            messagebox.showerror("Error", "No se pudieron cargar las preguntas desde la base de datos.")
            return

        lista_preguntas_numeros = self.generar_lista_preguntas_40()

        def on_examen_complete(resultados):
            print("Guardando resultados del examen...")
            self.formulario_manager._guardar_resultado('examenes', matricula, resultados)

        PruebaViewOriginal(parent=self, controller=self.controller,
                             dataframe_preguntas=df_preguntas,
                             lista_numeros_preguntas=lista_preguntas_numeros,
                             on_complete_callback=on_examen_complete)
        
    def show_dashboard(self):
        matricula = self.user_data.get('matricula')
        if not matricula:
            messagebox.showerror("Error", "No se ha podido identificar al usuario.")
            return

        # 1. Obtener los datos desde el DashboardManager
        stats_data = self.dashboard_manager.obtener_stats_alumno(matricula)

        # 2. Si los datos se obtuvieron, lanzar la ventana del dashboard
        if stats_data:
            DashboardAlumnoView(parent=self, controller=self.controller, stats_data=stats_data)
        else:
            messagebox.showerror("Error", "No se pudieron cargar las estadísticas de rendimiento.")