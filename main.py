# Este es el contenido de main.py (en la carpeta raíz)

import tkinter as tk

# --- IMPORTACIONES CORREGIDAS ---
# Ahora apuntan a la nueva carpeta 'vistas'
from vistas.login_view import LoginView
from vistas.register_view import RegisterView
from vistas.admin_view import AdminView
from vistas.user_view import AlumnoView 

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pruebas de Inglés")
        self.geometry("450x450")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginView, RegisterView, AdminView, AlumnoView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name, user_data=None):
        frame = self.frames[page_name]
        if user_data and hasattr(frame, 'set_user_data'):
            frame.set_user_data(user_data)
        frame.tkraise()
    
    # ... (el resto de tus métodos show_..._view) ...
    def show_login_view(self):
        self.show_frame("LoginView")

    def show_register_view(self):
        self.show_frame("RegisterView")

    def show_admin_view(self, user_data):
        self.show_frame("AdminView", user_data)

    def show_alumno_view(self, user_data):
        self.show_frame("AlumnoView", user_data)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()