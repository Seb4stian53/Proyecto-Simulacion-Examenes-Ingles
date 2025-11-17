import tkinter as tk
from tkinter import messagebox
import time

class PruebaViewOriginal(tk.Toplevel):
    def __init__(self, parent, controller, dataframe_preguntas, lista_numeros_preguntas, on_complete_callback):
        super().__init__(parent)
        self.controller = controller
        self.df = dataframe_preguntas
        self.num_preguntas = lista_numeros_preguntas
        self.on_complete_callback = on_complete_callback

        # Variables de estado
        self.n_preg = 0
        self.errores = [0, 0, 0, 0, 0, 0]
        self.tiempo_inicio = time.time()
        self.timer_id = None
        self.TIEMPO_POR_PREGUNTA = 60 # 60 segundos por pregunta
        self.tiempo_restante = self.TIEMPO_POR_PREGUNTA
        

        # Configuración de la ventana
        self.title("Cuestionario de inglés")
        self.geometry("700x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.mostrar_pregunta()

    def create_widgets(self):
        self.label_progreso = tk.Label(self, text="", font=("Arial", 10, "italic"))
        self.label_progreso.pack(pady=(10, 0))
        
        self.label_pregunta = tk.Label(self, text="", font=("Arial", 14), wraplength=650, justify="left")
        self.label_pregunta.pack(pady=(10, 30))

        self.label_tiempo = tk.Label(self, text=f"Tiempo restante: {self.TIEMPO_POR_PREGUNTA}s", font=("Arial", 10, "bold"))
        self.label_tiempo.pack(pady=10)

        self.selected_option = tk.StringVar(value=None)

        pregunta_vacia = self.df.iloc[self.num_preguntas[0]] # Usamos la primera para inicializar
        self.radioa = tk.Radiobutton(self, variable=self.selected_option, text="", value='a')
        self.radiob = tk.Radiobutton(self, variable=self.selected_option, text="", value='b')
        self.radioc = tk.Radiobutton(self, variable=self.selected_option, text="", value='c')
        self.radiod = tk.Radiobutton(self, variable=self.selected_option, text="", value='d')

        self.radioa.pack(anchor='w', padx=50)
        self.radiob.pack(anchor='w', padx=50)
        self.radioc.pack(anchor='w', padx=50)
        self.radiod.pack(anchor='w', padx=50)
        
        self.button_siguiente = tk.Button(self, text="Siguiente", command=self.on_button_click)
        self.button_siguiente.pack(pady=20)


    def obtener_categoria(self, num_pregunta):
        if 0 < num_pregunta <= 10: return 0
        elif num_pregunta <= 25: return 1
        elif num_pregunta <= 40: return 2
        elif num_pregunta <= 60: return 3
        elif num_pregunta <= 70: return 4
        elif num_pregunta <= 80: return 5

    def validar_respuesta(self, n_preg, respuesta):
        if self.df['respuestas'].iloc[n_preg-1] == respuesta:
            return True
        else:
            categoria = self.obtener_categoria(n_preg)
            self.errores[categoria] += 1
            return False

    def obtener_clasificacion(self):
        categorias = [("Beginner", 0, 2),("Elementary", 1, 3),("Pre-intermediate", 2, 3),("Intermediate", 3, 4),("Upper-intermediate", 4, 2),("Advanced", 5, 2)]
        for nombre, indice, limite in categorias:
            if self.errores[indice] >= limite:
                return nombre
        return "Advanced"

    def actualizar_tiempo(self):
        """Decrementa el contador y actualiza la etiqueta."""
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.label_tiempo.config(text=f"Tiempo restante: {self.tiempo_restante}s")
            # Llamar a esta función de nuevo después de 1 segundo (1000ms)
            self.timer_id = self.after(1000, self.actualizar_tiempo)
        else:
            # Si el tiempo llega a cero, simula un clic en el botón Siguiente
            self.on_button_click(tiempo_agotado=True)

    def mostrar_pregunta(self):
        """Carga los datos de la pregunta actual e inicia el temporizador."""
        if self.timer_id:
            self.after_cancel(self.timer_id) # Cancela el temporizador anterior

        pregunta = self.df.iloc[self.num_preguntas[self.n_preg]]
        
        # Actualizar la interfaz
        self.label_progreso.config(text=f"Pregunta {self.n_preg + 1} de {len(self.num_preguntas)}")
        texto_pregunta = str(pregunta['pregunta']).replace("\\n", "\n")
        self.label_pregunta.config(text=f"{self.n_preg + 1}. {texto_pregunta}")
        self.radioa.config(text=pregunta['a'])
        self.radiob.config(text=pregunta['b'])
        self.radioc.config(text=pregunta['c'])
        self.radiod.config(text=pregunta['d'])
        self.selected_option.set(None) # Deseleccionar opción

        # Reiniciar temporizador
        self.tiempo_restante = self.TIEMPO_POR_PREGUNTA
        self.label_tiempo.config(text=f"Tiempo restante: {self.tiempo_restante}s")
        self.timer_id = self.after(1000, self.actualizar_tiempo) # Iniciar el nuevo timer

    def on_button_click(self, tiempo_agotado=False):
        """Maneja el clic en Siguiente o el tiempo agotado."""
        
        respuesta_seleccionada = self.selected_option.get()
        
        # Si el usuario no seleccionó nada Y no se agotó el tiempo, mostramos advertencia.
        if not respuesta_seleccionada and not tiempo_agotado:
            messagebox.showwarning("Atención", "Debes seleccionar una respuesta.", parent=self)
            return
        
        # Validar la respuesta (si se seleccionó una, si no, se toma como incorrecta)
        if respuesta_seleccionada:
            self.validar_respuesta(self.num_preguntas[self.n_preg] + 1 , respuesta_seleccionada)
        else:
            # Si el tiempo se agotó y no hubo respuesta, se valida con una respuesta vacía o incorrecta
            self.validar_respuesta(self.num_preguntas[self.n_preg] + 1 , "SIN_RESPUESTA") # Se registrará como error

        # Cancelar el temporizador actual antes de avanzar
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.n_preg += 1

        if self.n_preg < len(self.num_preguntas):
            self.mostrar_pregunta() # Pasa a la siguiente pregunta
        else:
            self.finalizar_cuestionario() # Finaliza si no hay más preguntas

    def finalizar_cuestionario(self):
        """Calcula y devuelve los resultados finales."""
        
        if self.timer_id: # Doble chequeo por si acaso
            self.after_cancel(self.timer_id)
            
        cant_errores = sum(self.errores)
        total_preguntas = len(self.num_preguntas)
        aciertos = total_preguntas - cant_errores
        promedio = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0
        categoria = self.obtener_clasificacion()
        tiempo_total = int(time.time() - self.tiempo_inicio)
        
        # Mapeamos errores para FormManager
        errores_dict = {
            'beginner': self.errores[0], 'elementary': self.errores[1],
            'pre-intermediate': self.errores[2], 'intermediate': self.errores[3],
            'upper-intermediate': self.errores[4], 'advanced': self.errores[5]
        }

        resultados = {
            'calificacion': f"{promedio:.2f}",
            'aciertos': aciertos,
            'errores_por_categoria': errores_dict,
            'tiempo_total': tiempo_total,
            'categoria_obtenida': categoria
        }
        
        self.on_complete_callback(resultados)
        
        if promedio >= 70:
            estado_aprobacion = "¡Aprobado!"
            titulo_mensaje = "¡Felicidades!"
        else:
            estado_aprobacion = "No Aprobado"
            titulo_mensaje = "Resultados Finales"

        mensaje_final = (
            f"Resultado: {estado_aprobacion}\n\n"
            f"Calificación Final: {promedio:.2f}%\n"
            f"Nivel Determinado: {categoria}"
        )

        tk.messagebox.showinfo(titulo_mensaje, mensaje_final, parent=self)
        
        self.destroy()

    def on_closing(self):
        """Maneja el cierre con el botón 'X'."""
        if messagebox.askokcancel("Salir", "¿Seguro que quieres abandonar? El progreso no se guardará.", parent=self):
            if self.timer_id:
                self.after_cancel(self.timer_id)
            self.destroy()