import tkinter as tk

# El nombre de la clase ahora es 'AlumnoView' para coincidir con lo que 'main.py' espera importar.
class AlumnoView(tk.Frame):
    
    # 1. El __init__ ya no pide 'user_data' al momento de la creación.
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Llamamos al método que crea todos los elementos visuales (widgets).
        self.create_widgets()
    
    def create_widgets(self):
        """Crea todos los widgets de la vista, dejando vacíos los que dependen de los datos del usuario."""
        
        tk.Label(self, text="Panel de Alumno", 
                font=("Arial", 16)).pack(pady=20)
        
        # 2. Creamos las etiquetas vacías y las guardamos en self para actualizarlas después.
        self.welcome_label = tk.Label(self, text="")
        self.welcome_label.pack()
        
        self.matricula_label = tk.Label(self, text="")
        self.matricula_label.pack()
        
        # Funciones para usuario normal
        tk.Button(self, text="Mi Perfil", width=20).pack(pady=5)
        tk.Button(self, text="Realizar Examen", width=20).pack(pady=5) # Ejemplo
        
        tk.Button(self, text="Cerrar Sesión", command=self.logout,
                 bg="red", fg="white").pack(pady=20)
    
    # 3. Este método es llamado por el controlador para "llenar" la vista con datos.
    def set_user_data(self, user_data):
        """Recibe los datos del usuario y actualiza las etiquetas de la vista."""
        self.welcome_label.config(text=f"Bienvenido: {user_data['nombre']}")
        self.matricula_label.config(text=f"Matrícula: {user_data['matricula']}")

    def logout(self):
        """Limpia los datos de la pantalla y regresa a la vista de login."""
        # Es una buena práctica limpiar los datos antes de cambiar de vista.
        self.welcome_label.config(text="")
        self.matricula_label.config(text="")
        
        self.controller.show_login_view()