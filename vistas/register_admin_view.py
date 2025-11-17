import tkinter as tk
from tkinter import messagebox
from database.registrar_admin import RegistrarAdmin

class RegisterAdminView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.registrar = RegistrarAdmin()
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self, text="Registro de Usuario", font=("Arial", 16)).pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("Matrícula:", "matricula_entry"),
            ("Nombre Completo:", "nombre_entry"), 
            ("Usuario:", "usuario_entry"),
        ]
        
        self.entries = {}
        for label, entry_name in fields:
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self, width=30)
            if "password" in entry_name:
                entry.config(show="*")
            entry.pack(pady=5)
            self.entries[entry_name] = entry
        
        # Botones
        tk.Button(self, text="Registrar", command=self.register,
                 bg="green", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Volver al Login", command=self.go_to_login,
                 bg="gray", fg="white", width=15).pack(pady=5)
    
    def register(self):
        # Obtener datos
        matricula = self.entries['matricula_entry'].get()
        nombre = self.entries['nombre_entry'].get()
        usuario = self.entries['usuario_entry'].get()
        
        # Validaciones
        if not all([matricula, nombre, usuario]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Registrar usuario (tipo 0 = usuario normal)
        result = self.registrar.registrar_admin(matricula, nombre, usuario)
        
        if result['success']:
            messagebox.showinfo("Éxito", result['message'])
            self.go_to_login()
        else:
            messagebox.showerror("Error", result['error'])
    
    def go_to_login(self):
        self.controller.show_login_view()