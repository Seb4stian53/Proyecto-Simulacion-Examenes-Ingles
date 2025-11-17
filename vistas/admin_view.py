import tkinter as tk
from tkinter import messagebox # <-- IMPORTACIÓN CLAVE AÑADIDA

# --- Importaciones de tus otros módulos ---
from vistas.register_admin_view import RegisterAdminView
from database.conn import DatabaseConnection
from database.dashboard import DashboardManager
from vistas.dashboard_admin_view import DashboardAdminView 

class AdminView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Instanciación de los Manejadores ---
        # Es una buena práctica crear la instancia de conexión una vez y pasarla.
        # Si tu controlador (main.py) ya crea una, sería ideal recibirla.
        # Por ahora, la creamos aquí para que funcione.
        db_conn = DatabaseConnection()
        self.dashboard_manager = DashboardManager(db_conn)
        
        # Llamamos al método que crea todos los widgets para mantener el __init__ limpio.
        self.create_widgets()

    def create_widgets(self):
        """Crea y organiza todos los elementos visuales de la ventana."""
        
        tk.Label(self, text="Panel de Administración", 
                 font=("Arial", 16, "bold")).pack(pady=20)
        
        # Guardamos la etiqueta de bienvenida para poder actualizarla después.
        self.welcome_label = tk.Label(self, text="", font=("Arial", 12))
        self.welcome_label.pack(pady=5)
        
        tk.Label(self, text="Rol: Administrador", font=("Arial", 10)).pack(pady=(0, 20))
        
        # --- Botones de Funciones ---
        tk.Button(self, text="Ver Estadísticas Globales", command=self.show_dashboard, 
                  width=25, height=2, bg="navy", fg="white", font=("Arial", 10)).pack(pady=5)
                  
        tk.Button(self, text="Registrar Nuevo Administrador", command=self.go_to_register, 
                  width=25, height=2, font=("Arial", 10)).pack(pady=5)

        tk.Button(self, text="Cerrar Sesión", command=self.logout,
                  bg="tomato", fg="white").pack(side="bottom", pady=20)

    def set_user_data(self, user_data):
        """
        Este método es llamado por el controlador para actualizar la vista
        con los datos del usuario que ha iniciado sesión.
        """
        nombre_usuario = user_data.get('nombre', 'Usuario Desconocido')
        self.welcome_label.config(text=f"Bienvenido, {nombre_usuario}")

    def logout(self):
        """Limpia los datos de la vista y le pide al controlador que muestre el login."""
        self.welcome_label.config(text="")
        self.controller.show_login_view()
        
    def go_to_register(self):
        """Le pide al controlador que muestre la ventana de registro."""
        self.controller.show_register_admin_view()
        
    def show_dashboard(self):
        """
        Obtiene los datos de estadísticas globales y abre la ventana del dashboard.
        """
        # 1. Obtener los datos desde el DashboardManager
        stats_data = self.dashboard_manager.obtener_stats_admin()

        # 2. Si los datos se obtuvieron, lanzar la ventana del dashboard
        if stats_data:
            DashboardAdminView(parent=self, controller=self.controller, stats_data=stats_data)
        else:
            messagebox.showerror("Error", "No se pudieron cargar las estadísticas globales. Revisa la conexión o si hay datos en la base de datos.")