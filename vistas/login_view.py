import tkinter as tk
from tkinter import messagebox
from database import Login

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.login_handler = Login()
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self, text="Inicio de Sesión", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self, text="Usuario:").pack()
        self.usuario_entry = tk.Entry(self, width=30)
        self.usuario_entry.pack(pady=5)
        
        tk.Label(self, text="Matricula:").pack()
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self, text="Ingresar", command=self.login, 
                 bg="blue", fg="white", width=15).pack(pady=10)
        
        tk.Button(self, text="Registrarse", command=self.go_to_register,
                 bg="gray", fg="white", width=15).pack(pady=5)
    
    def login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        result = self.login_handler.autenticar_usuario(usuario, password)
        
        if result['success']:
            user_data = result['user']
            messagebox.showinfo("Éxito", f"Bienvenido {user_data['nombre']}")
            
            # ✅ SIMPLE Y DIRECTO - Solo necesitamos el tipo_usuario
            if user_data['tipo_usuario'] == 1:
                self.controller.show_admin_view(user_data)
            else:
                self.controller.show_user_view(user_data)
        else:
            messagebox.showerror("Error", result['error'])
    
    def go_to_register(self):
        self.controller.show_register_view()