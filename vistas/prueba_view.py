import tkinter as tk
from tkinter import messagebox
import time

class PruebaView(tk.Toplevel):
    def __init__(self, parent, controller, preguntas, on_complete_callback):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.preguntas = preguntas
        self.on_complete_callback = on_complete_callback

        # Variables de estado del examen
        self.n_preg_actual = 0
        self.respuestas_usuario = {}
        self.errores_por_categoria = {
            'beginner': 0,
            'elementary': 0,
            'pre-intermediate': 0,
            'intermediate': 0,
            'upper-intermediate': 0,
            'advanced': 0
        }
        self.tiempo_inicio = time.time()

        # Configuración de la ventana
        self.title("Evaluación de Inglés")
        self.geometry("700x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrar la ventana sobre la ventana principal
        self.transient(parent)
        self.grab_set()

        # Verificar si hay preguntas antes de construir la UI
        if not self.preguntas:
            messagebox.showerror("Error", "No hay preguntas para mostrar.", parent=self)
            self.destroy()
            return

        self.create_widgets()
        self.mostrar_pregunta_actual()

    def create_widgets(self):
        # Frame principal para mejor organización
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Widget para el número de pregunta
        self.label_progreso = tk.Label(main_frame, text="", font=("Arial", 10, "italic"))
        self.label_progreso.pack(anchor='ne')

        # Widget para la pregunta
        self.label_pregunta = tk.Label(main_frame, text="", font=("Arial", 14), wraplength=600, justify="left")
        self.label_pregunta.pack(pady=(10, 30), anchor='w')

        # Variable para los Radiobutton
        self.selected_option = tk.StringVar(value=None)
        
        # Opciones de respuesta
        opciones = [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]
        self.radio_buttons = {}
        for texto, valor in opciones:
            rb = tk.Radiobutton(main_frame, text="", variable=self.selected_option, value=valor, font=("Arial", 12), justify="left")
            rb.pack(anchor='w', padx=20, pady=5)
            self.radio_buttons[texto] = rb # Guardamos referencia para actualizar texto

        # Frame para los botones de navegación
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side="bottom", fill="x", pady=(20, 0))

        self.button_siguiente = tk.Button(button_frame, text="Siguiente", font=("Arial", 12), command=self.siguiente_pregunta)
        self.button_siguiente.pack(side="right")

    def mostrar_pregunta_actual(self):
        pregunta = self.preguntas[self.n_preg_actual]
        total_preguntas = len(self.preguntas)

        # Actualizar progreso
        self.label_progreso.config(text=f"Pregunta {self.n_preg_actual + 1} de {total_preguntas}")
        
        # Actualizar texto de la pregunta
        self.label_pregunta.config(text=pregunta['pregunta'])
        
        # Actualizar textos de las opciones
        self.radio_buttons['a'].config(text=pregunta.get('a', ''))
        self.radio_buttons['b'].config(text=pregunta.get('b', ''))
        self.radio_buttons['c'].config(text=pregunta.get('c', ''))
        self.radio_buttons['d'].config(text=pregunta.get('d', ''))
        
        # Restaurar la selección anterior si el usuario vuelve atrás (no implementado en este ejemplo)
        self.selected_option.set(self.respuestas_usuario.get(self.n_preg_actual))
        
        # Cambiar el texto del botón en la última pregunta
        if self.n_preg_actual == total_preguntas - 1:
            self.button_siguiente.config(text="Finalizar")
        else:
            self.button_siguiente.config(text="Siguiente")

    def siguiente_pregunta(self):
        # Guardar la respuesta actual
        respuesta_usuario = self.selected_option.get()
        if not respuesta_usuario:
            messagebox.showwarning("Sin respuesta", "Por favor, selecciona una opción.", parent=self)
            return
            
        self.respuestas_usuario[self.n_preg_actual] = respuesta_usuario

        # Mover a la siguiente pregunta
        self.n_preg_actual += 1

        if self.n_preg_actual < len(self.preguntas):
            self.mostrar_pregunta_actual()
        else:
            self.finalizar_evaluacion()

    def finalizar_evaluacion(self):
        # Calcular resultados detallados
        total_preguntas = len(self.preguntas)
        aciertos = 0
        
        for i, pregunta in enumerate(self.preguntas):
            if self.respuestas_usuario.get(i) == pregunta['respuesta']:
                aciertos += 1
            else:
                categoria_error = pregunta['categoria']
                if categoria_error in self.errores_por_categoria:
                    self.errores_por_categoria[categoria_error] += 1
        
        tiempo_total_segundos = int(time.time() - self.tiempo_inicio)
        calificacion = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0

        # TODO: Implementar la lógica para determinar la 'categoria_obtenida'
        # Basado en la cantidad de errores por categoría.
        categoria_obtenida = "Intermediate" # Ejemplo estático

        # Crear el diccionario de resultados completo
        resultados = {
            'calificacion': f"{calificacion:.2f}",
            'aciertos': aciertos,
            'errores_por_categoria': self.errores_por_categoria,
            'tiempo_total': tiempo_total_segundos,
            'categoria_obtenida': categoria_obtenida
        }

        # Llamar al callback con los resultados
        if self.on_complete_callback:
            self.on_complete_callback(resultados)

        # Mostrar resumen al usuario y cerrar
        messagebox.showinfo(
            "Resultados",
            f"Evaluación finalizada.\nAciertos: {aciertos}/{total_preguntas}\nCalificación: {calificacion:.2f}%\nTiempo: {tiempo_total_segundos} segundos.",
            parent=self
        )
        self.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Seguro que quieres abandonar la evaluación? El progreso no se guardará.", parent=self):
            self.destroy()