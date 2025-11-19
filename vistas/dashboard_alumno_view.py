import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardAlumnoView(tk.Toplevel):
    def __init__(self, parent, controller, stats_data):
        super().__init__(parent)
        self.controller = controller
        self.stats_data = stats_data

        self.title("Dashboard de Rendimiento Personal")
        self.geometry("1000x700") # Ventana más ancha para dos columnas
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.transient(parent)
        self.grab_set()

        if not self.stats_data:
            messagebox.showerror("Error", "No se pudieron cargar los datos de rendimiento.", parent=self)
            self.destroy()
            return

        self.create_widgets()

    def _create_stat_box(self, parent, title, value):
        """Función auxiliar para crear un cuadro de estadística (KPI)."""
        frame = ttk.Frame(parent, padding=(5, 5), relief="groove", borderwidth=2)
        
        label_title = ttk.Label(frame, text=title, font=("Arial", 10, "bold"))
        label_title.pack()
        
        label_value = ttk.Label(frame, text=str(value), font=("Arial", 16))
        label_value.pack()
        return frame

    def _create_error_graph(self, parent, error_data, title):
        """Función auxiliar para crear una gráfica de barras de errores."""
        graph_frame = ttk.LabelFrame(parent, text=title, padding="10")
        
        # Preparar la figura de Matplotlib
        fig = plt.Figure(figsize=(5, 3.5), dpi=100)
        ax = fig.add_subplot(111)

        # Filtrar categorías con 0 errores para una gráfica más limpia
        errores_filtrados = {cat.replace('-', '-\n'): val for cat, val in error_data.items() if val > 0}

        if errores_filtrados:
            categorias = list(errores_filtrados.keys())
            valores = list(errores_filtrados.values())
            
            # Crear la gráfica
            ax.bar(categorias, valores, color='#66b3ff')
            ax.set_ylabel("Número de Errores")
            plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=8)
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)) # Asegurar que el eje Y sea de enteros
            ax.set_ylim(bottom=0)
        else:
            ax.text(0.5, 0.5, "¡Felicidades!\nSin errores registrados.", horizontalalignment='center', verticalalignment='center')

        fig.tight_layout() # Ajustar para que las etiquetas no se corten
        
        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return graph_frame

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")
        # Configurar las columnas para que se expandan por igual
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # --- COLUMNA DE PRUEBAS (IZQUIERDA) ---
        pruebas_col_frame = ttk.Frame(main_frame)
        pruebas_col_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        pruebas_col_frame.grid_rowconfigure(1, weight=1) # La gráfica se expandirá

        if self.stats_data.get('total_pruebas', 0) > 0:
            kpi_pruebas_frame = ttk.LabelFrame(pruebas_col_frame, text="Resumen de Prácticas", padding="10")
            kpi_pruebas_frame.grid(row=0, column=0, sticky="ew")
            
            self._create_stat_box(kpi_pruebas_frame, "Intentos Realizados", self.stats_data['total_pruebas']).pack(fill="x", pady=3)
            self._create_stat_box(kpi_pruebas_frame, "Mejor Calificación", f"{self.stats_data['mejor_nota_prueba']:.2f}%").pack(fill="x", pady=3)
            self._create_stat_box(kpi_pruebas_frame, "Nivel Más Común", self.stats_data['nivel_comun_prueba']).pack(fill="x", pady=3)
            
            graph_p = self._create_error_graph(pruebas_col_frame, self.stats_data['errores_por_categoria_pruebas'], "Análisis de Errores en Prácticas")
            graph_p.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        else:
            label_sin_datos_p = ttk.Label(pruebas_col_frame, text="Aún no has realizado pruebas de práctica.", font=("Arial", 12), justify="center", wraplength=400)
            label_sin_datos_p.grid(row=0, column=0, sticky="nsew", pady=20)

        # --- COLUMNA DE EXÁMENES (DERECHA) ---
        examenes_col_frame = ttk.Frame(main_frame)
        examenes_col_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        examenes_col_frame.grid_rowconfigure(1, weight=1) # La gráfica se expandirá

        # Usamos mejor_nota_examen como indicador de si se ha hecho algún examen
        if self.stats_data.get('mejor_nota_examen', 0) > 0 or self.stats_data.get('nivel_comun_examen') != 'N/A':
            kpi_examenes_frame = ttk.LabelFrame(examenes_col_frame, text="Resumen de Exámenes Finales", padding="10")
            kpi_examenes_frame.grid(row=0, column=0, sticky="ew")

            # Nota: Necesitas añadir COUNT(*) a la consulta de exámenes en DashboardManager para 'total_examenes'
            total_examenes = self.stats_data.get('total_examenes', 'N/A') 
            self._create_stat_box(kpi_examenes_frame, "Intentos Realizados", total_examenes).pack(fill="x", pady=3)
            self._create_stat_box(kpi_examenes_frame, "Mejor Calificación", f"{self.stats_data['mejor_nota_examen']:.2f}%").pack(fill="x", pady=3)
            self._create_stat_box(kpi_examenes_frame, "Nivel Más Común", self.stats_data['nivel_comun_examen']).pack(fill="x", pady=3)

            graph_e = self._create_error_graph(examenes_col_frame, self.stats_data['errores_por_categoria_examenes'], "Análisis de Errores en Exámenes")
            graph_e.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        else:
            label_sin_datos_e = ttk.Label(examenes_col_frame, text="Aún no has realizado exámenes finales.", font=("Arial", 12), justify="center", wraplength=400)
            label_sin_datos_e.grid(row=0, column=0, sticky="nsew", pady=20)

        # --- Botón para cerrar ---
        ttk.Button(main_frame, text="Cerrar Ventana", command=self.destroy).grid(row=1, column=0, columnspan=2, pady=10)