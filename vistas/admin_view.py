import tkinter as tk

class AdminView(tk.Frame):
    # 1. El __init__ ya no pide 'user_data'. Se crea "vacío".
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Creamos las etiquetas (widgets) pero sin texto de usuario todavía.
        # Las guardamos como atributos de la clase (ej. self.welcome_label)
        # para poder acceder a ellas y modificarlas más tarde.
        
        tk.Label(self, text="Panel de Administración", 
                 font=("Arial", 16)).pack(pady=20)
        
        self.welcome_label = tk.Label(self, text="")
        self.welcome_label.pack()
        
        tk.Label(self, text="Tipo: Administrador").pack()
        
        # Botones de funciones
        tk.Button(self, text="Registrar Administrador", width=20).pack(pady=5)
        tk.Button(self, text="Reportes", width=20).pack(pady=5)
        
        tk.Button(self, text="Cerrar Sesión", command=self.logout,
                  bg="red", fg="white").pack(pady=20)

    # 2. Este método es llamado por el controlador JUSTO ANTES de mostrar la vista.
    def set_user_data(self, user_data):
        """Recibe los datos del usuario y actualiza las etiquetas de la vista."""
        self.welcome_label.config(text=f"Bienvenido: {user_data['nombre']}")

    def logout(self):
        # Limpiamos la etiqueta de bienvenida para el próximo inicio de sesión
        self.welcome_label.config(text="")
        self.controller.show_login_view()