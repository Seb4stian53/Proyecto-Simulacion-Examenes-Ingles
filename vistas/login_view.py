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
        # Header rojo
        header_frame = tk.Frame(self, bg="#E51C23")
        header_frame.grid(row=0, column=0, sticky="nsew")
        title_label = tk.Label(header_frame, text="Test of English Basic & Intermediate", 
                               bg="#E51C23", fg="white", font=("Arial", 30, "bold"))
        title_label.pack(expand=True)

        # Cuerpo blanco
        body_frame = tk.Frame(self, bg="white")
        body_frame.grid(row=1, column=0, sticky="nsew")
        body_frame.columnconfigure(0, weight=1)
        body_frame.rowconfigure(0, weight=1)
        form_frame = tk.Frame(body_frame, bg="white")
        form_frame.grid(row=0, column=0)

        # Espacio superior
        tk.Label(form_frame, bg="white").pack(pady=40)

        # Campos de entrada
        self.usuario_entry = self.create_input_block(form_frame, "User")  # Usuario visible
        self.password_entry = self.create_input_block(form_frame, "Tuition", show="*")  # Matrícula oculta

        # Botón de login
        NORMAL_COLOR = "#00B020"
        self.login_button = tk.Button(
            form_frame,
            text="Login",
            bg=NORMAL_COLOR,
            fg="white",
            activebackground=NORMAL_COLOR,
            activeforeground="white",
            font=("Arial", 18, "bold"),
            bd=0,
            relief="flat",
            width=12,
            command=self.login
        )
        self.login_button.pack(pady=10)

        # Botón de registro
        self.register_button = tk.Button(
            form_frame,
            text="Registrarse",
            bg="gray",
            fg="white",
            activebackground="gray",
            activeforeground="white",
            font=("Arial", 18, "bold"),
            bd=0,
            relief="flat",
            width=12,
            command=self.go_to_register
        )
        self.register_button.pack(pady=5)

        # Hover efecto para botones
        def on_enter_login(event, button):
            button.config(bg="#009018", activebackground="#009018")

        def on_leave_login(event, button):
            button.config(bg=NORMAL_COLOR, activebackground=NORMAL_COLOR)

        def on_enter_register(event, button):
            button.config(bg="#808080", activebackground="#808080")  # Gris oscuro para hover de Register

        def on_leave_register(event, button):
            button.config(bg="gray", activebackground="gray")  # Color original del botón de Register

        # Vinculamos el hover a los botones después de que sean creados
        self.login_button.bind("<Enter>", lambda e: on_enter_login(e, self.login_button))
        self.login_button.bind("<Leave>", lambda e: on_leave_login(e, self.login_button))
        
        self.register_button.bind("<Enter>", lambda e: on_enter_register(e, self.register_button))
        self.register_button.bind("<Leave>", lambda e: on_leave_register(e, self.register_button))

    def create_input_block(self, parent, label_text, show=None):
        label = tk.Label(
            parent,
            text=label_text,
            bg="white",
            fg="#777777",
            font=("Arial", 20, "bold")
        )
        label.pack(pady=(0, 10))

        bg_frame = tk.Frame(parent, bg="#DDDDDD", width=600, height=45)
        bg_frame.pack(pady=(0, 30))
        bg_frame.pack_propagate(False)

        entry = tk.Entry(
            bg_frame,
            bd=0,
            relief="flat",
            font=("Arial", 16),
            bg="#DDDDDD",
            show=show
        )
        entry.pack(fill="both", expand=True, padx=10, pady=5)

        return entry

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
                self.controller.show_alumno_view(user_data)
        else:
            messagebox.showerror("Error", result['error'])

    def go_to_register(self):
        self.controller.show_register_view()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login View")
    root.geometry("690x520")
    app = LoginView(root, controller=None)
    app.pack(fill="both", expand=True)
    root.mainloop()