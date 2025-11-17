import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardAdminView(tk.Toplevel):
    def __init__(self, parent, controller, stats_data):
        super().__init__(parent)
        self.controller = controller
        self.stats_data = stats_data

        self.title("Dashboard de Administrador - Estadísticas Globales")
        self.geometry("1100x800")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.transient(parent)
        self.grab_set()

        if not self.stats_data:
            messagebox.showerror("Error", "No se pudieron cargar los datos.", parent=self)
            self.destroy()
            return

        self.create_widgets()

    def _create_stat_box(self, parent, title, value, color="black"):
        """Función auxiliar para crear un cuadro de KPI."""
        frame = ttk.Frame(parent, padding=(10, 5), relief="solid", borderwidth=1)
        label_title = ttk.Label(frame, text=title, font=("Arial", 11))
        label_title.pack()
        label_value = ttk.Label(frame, text=str(value), font=("Arial", 20, "bold"), foreground=color)
        label_value.pack()
        return frame

    def _create_bar_chart(self, parent, data, title, x_label, y_label):
        """Función auxiliar para crear una gráfica de barras."""
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        fig = plt.Figure(figsize=(5, 3.5), dpi=100)
        ax = fig.add_subplot(111)

        if data:
            labels = [item['categoria'] for item in data]
            values = [item['cuenta'] for item in data]
            ax.bar(labels, values, color='#66b3ff')
            ax.set_ylabel(y_label)
            ax.set_xlabel(x_label)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=9)
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.set_ylim(bottom=0)
        else:
            ax.text(0.5, 0.5, "No hay datos disponibles.", ha='center', va='center')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return frame

    def _create_pie_chart(self, parent, data, title):
        """Función auxiliar para crear una gráfica de pastel."""
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        fig = plt.Figure(figsize=(5, 3.5), dpi=100)
        ax = fig.add_subplot(111)

        filtered_data = {k: v for k, v in data.items() if v > 0}
        
        if filtered_data:
            labels = filtered_data.keys()
            sizes = filtered_data.values()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
            ax.axis('equal') # Asegura que el pastel sea un círculo.
        else:
            ax.text(0.5, 0.5, "No hay datos disponibles.", ha='center', va='center')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return frame

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")
        
        # --- FILA DE KPIs ---
        kpi_frame = ttk.Frame(main_frame)
        kpi_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        for i in range(4): kpi_frame.grid_columnconfigure(i, weight=1)

        self._create_stat_box(kpi_frame, "Total Prácticas Realizadas", self.stats_data['total_pruebas_global']).grid(row=0, column=0, padx=5, sticky="ew")
        self._create_stat_box(kpi_frame, "Promedio Gral. Prácticas", f"{self.stats_data['promedio_pruebas_global']:.2f}%").grid(row=0, column=1, padx=5, sticky="ew")
        self._create_stat_box(kpi_frame, "Tasa Aprobación Exámenes", f"{self.stats_data['tasa_aprobacion_global']:.2f}%", color="green").grid(row=0, column=2, padx=5, sticky="ew")
        
        # KPI del Indicador de Beneficio
        avg_p = self.stats_data['promedio_pruebas_global']
        avg_e = self.stats_data['promedio_examenes_global']
        indicador_texto = "Mejora" if avg_e > avg_p else "Sin Mejora"
        indicador_color = "green" if avg_e > avg_p else "orange"
        self._create_stat_box(kpi_frame, "Práctica -> Examen", indicador_texto, color=indicador_color).grid(row=0, column=3, padx=5, sticky="ew")
        
        # --- FILA DE GRÁFICAS DE BARRAS ---
        bar_charts_frame = ttk.Frame(main_frame)
        bar_charts_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        bar_charts_frame.grid_columnconfigure(0, weight=1)
        bar_charts_frame.grid_columnconfigure(1, weight=1)

        self._create_bar_chart(bar_charts_frame, self.stats_data['distribucion_niveles_pruebas'], "Distribución de Niveles (Prácticas)", "Nivel Obtenido", "Cantidad de Pruebas").grid(row=0, column=0, padx=5, sticky="nsew")
        self._create_bar_chart(bar_charts_frame, self.stats_data['distribucion_niveles_examenes'], "Distribución de Niveles (Exámenes)", "Nivel Obtenido", "Cantidad de Exámenes").grid(row=0, column=1, padx=5, sticky="nsew")

        # --- FILA DE GRÁFICAS DE PASTEL ---
        pie_charts_frame = ttk.Frame(main_frame)
        pie_charts_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        pie_charts_frame.grid_columnconfigure(0, weight=1)
        pie_charts_frame.grid_columnconfigure(1, weight=1)

        self._create_pie_chart(pie_charts_frame, self.stats_data['total_errores_categoria_pruebas'], "Distribución de Errores (Prácticas)").grid(row=0, column=0, padx=5, sticky="nsew")
        self._create_pie_chart(pie_charts_frame, self.stats_data['total_errores_categoria_examenes'], "Distribución de Errores (Exámenes)").grid(row=0, column=1, padx=5, sticky="nsew")
        
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)