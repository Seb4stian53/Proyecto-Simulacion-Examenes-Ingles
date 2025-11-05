import tkinter as tk
import time

class PruebaViewOriginal(tk.Toplevel):
    def __init__(self, parent, controller, dataframe_preguntas, lista_numeros_preguntas, on_complete_callback):
        super().__init__(parent)
        self.controller = controller
        self.df = dataframe_preguntas
        self.num_preguntas = lista_numeros_preguntas
        self.on_complete_callback = on_complete_callback

        # Adaptación de tus variables globales
        self.n_preg = 0
        self.errores = [0, 0, 0, 0, 0, 0]
        self.tiempo_inicio = time.time()

        # Configuración de la ventana (reemplaza a root = tk.Tk())
        self.title("Cuestionario de inglés")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.transient(parent)
        self.grab_set()

        # --- El cuerpo de tu función 'generar_cuestionario_tkinter' va aquí ---
        
        pregunta = self.df.iloc[self.num_preguntas[self.n_preg]]
        texto_pregunta = str(pregunta['pregunta']).replace("\\n", "\n")
        pregunta_texto = f"{self.n_preg + 1}. {texto_pregunta}"

        self.label_pregunta = tk.Label(self, text=pregunta_texto)
        self.label_pregunta.pack()

        self.selected_option = tk.StringVar(value=None)

        self.radioa = tk.Radiobutton(self, variable=self.selected_option, text=pregunta['a'], value='a')
        self.radiob = tk.Radiobutton(self, variable=self.selected_option, text=pregunta['b'], value='b')
        self.radioc = tk.Radiobutton(self, variable=self.selected_option, text=pregunta['c'], value='c')
        self.radiod = tk.Radiobutton(self, variable=self.selected_option, text=pregunta['d'], value='d')

        self.radioa.pack()
        self.radiob.pack()
        self.radioc.pack()
        self.radiod.pack()
        
        button = tk.Button(self, text="Siguiente", command=self.on_button_click)
        button.pack()

    # --- Tus funciones de lógica ahora son métodos de la clase ---

    def obtener_categoria(self, num_pregunta):
        # ... (esta función se mantiene exactamente igual) ...
        if 0 < num_pregunta <= 10: return 0
        elif num_pregunta <= 25: return 1
        elif num_pregunta <= 40: return 2
        elif num_pregunta <= 60: return 3
        elif num_pregunta <= 70: return 4
        elif num_pregunta <= 75: return 5

    def validar_respuesta(self, n_preg, respuesta):
        if self.df['respuestas'].iloc[n_preg-1] == respuesta:
            print("Respuesta correcta")
            return True
        else:
            categoria = self.obtener_categoria(n_preg)
            self.errores[categoria] += 1
            print("Respuesta incorrecta")
            return False

    def obtener_clasificacion(self):
        # ... (esta función se mantiene exactamente igual, pero usa self.errores) ...
        categorias = [("Beginner", 0, 2),("Elementary", 1, 3),("Pre-intermediate", 2, 3),("Intermediate", 3, 4),("Upper-intermediate", 4, 2),("Advanced", 5, 2)]
        for nombre, indice, limite in categorias:
            if self.errores[indice] >= limite:
                return nombre
        return "Advanced"

    def on_button_click(self):
        respuesta_seleccionada = self.selected_option.get()
        if not respuesta_seleccionada:
            tk.messagebox.showwarning("Atención", "Debes seleccionar una respuesta.", parent=self)
            return

        self.validar_respuesta(self.num_preguntas[self.n_preg] + 1 , respuesta_seleccionada)
        self.selected_option.set(None)
        self.n_preg += 1

        if self.n_preg < len(self.num_preguntas):
            pregunta = self.df.iloc[self.num_preguntas[self.n_preg]]
            texto_pregunta = str(pregunta['pregunta']).replace("\\n", "\n")
            pregunta_texto = f"{self.n_preg + 1}. {texto_pregunta}"
            self.label_pregunta.config(text=pregunta_texto)
            self.radioa.config(text=pregunta['a'])
            self.radiob.config(text=pregunta['b'])
            self.radioc.config(text=pregunta['c'])
            self.radiod.config(text=pregunta['d'])
        else:
            # --- Fin del cuestionario: Calculamos y devolvemos resultados ---
            cant_errores = sum(self.errores)
            total_preguntas = len(self.num_preguntas)
            aciertos = total_preguntas - cant_errores
            promedio = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0
            categoria = self.obtener_clasificacion()
            tiempo_total = int(time.time() - self.tiempo_inicio)
            
            # Mapeamos los errores de tu lista a un diccionario como lo espera FormularioManager
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
            
            # Llamamos al callback para que AlumnoView guarde los datos
            self.on_complete_callback(resultados)
            
            tk.messagebox.showinfo("Fin del Cuestionario", f"Tu promedio es: {promedio:.2f}%\nTu categoria es: {categoria}", parent=self)
            self.destroy() # Cerramos la ventana