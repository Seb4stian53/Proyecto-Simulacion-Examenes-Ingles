import tkinter as tk
from tkinter import ttk

class RevisionView(tk.Toplevel):
    def __init__(self, parent, controller, detalle_evaluacion, tipo_evaluacion):
        super().__init__(parent)
        self.controller = controller
        self.detalle = detalle_evaluacion

        self.title(f"Revisión de {tipo_evaluacion}")
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()

        # --- Canvas y Scrollbar para contenido dinámico ---
        main_canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Poblar el frame con las preguntas ---
        self.create_pregunta_widgets(scrollable_frame)

    def create_pregunta_widgets(self, parent):
        for i, pregunta in enumerate(self.detalle):
            # Frame para cada pregunta, para agrupar visualmente
            pregunta_frame = ttk.LabelFrame(parent, text=f"Pregunta {i+1}", padding="10")
            pregunta_frame.pack(fill="x", padx=10, pady=10)

            # Texto de la pregunta
            ttk.Label(pregunta_frame, text=pregunta['pregunta'], wraplength=700, font=("Arial", 11, "bold")).pack(anchor="w")
            
            # --- LÓGICA DE RESALTADO MODIFICADA ---
            
            # Obtenemos las respuestas clave para esta pregunta
            # Usamos .lower() para evitar problemas con mayúsculas/minúsculas
            respuesta_usuario = pregunta['respuesta_usuario'].lower() if pregunta['respuesta_usuario'] else None
            respuesta_correcta = pregunta['respuesta_correcta'].lower()

            opciones = ['a', 'b', 'c', 'd']
            for opcion in opciones:
                texto_opcion = f"{opcion.upper()}. {pregunta[opcion]}"
                label_opcion = ttk.Label(pregunta_frame, text=texto_opcion, wraplength=680)
                label_opcion.pack(anchor="w", padx=15)

                # Regla 1: El usuario acertó
                if opcion == respuesta_usuario and opcion == respuesta_correcta:
                    label_opcion.config(foreground="green", font=("Arial", 10, "bold"))
                    # Añadimos un prefijo para que sea más visual
                    label_opcion.config(text=f"✔ {texto_opcion}")

                # Regla 2: El usuario se equivocó
                elif opcion == respuesta_usuario and opcion != respuesta_correcta:
                    label_opcion.config(foreground="red", font=("Arial", 10, "bold"))
                    label_opcion.config(text=f"✖ {texto_opcion}")
                
                # Regla 3: El usuario no eligió esta, pero era la correcta
                elif opcion == respuesta_correcta:
                    label_opcion.config(foreground="green")

            # Separador visual
            ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=10, pady=5)