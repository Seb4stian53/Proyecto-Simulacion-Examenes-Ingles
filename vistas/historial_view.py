import tkinter as tk
from tkinter import ttk, messagebox
from vistas.revision_view import RevisionView

class HistorialView(tk.Toplevel):
    def __init__(self, parent, controller, historial_data, dashboard_manager):
        super().__init__(parent)
        self.controller = controller
        self.historial_data = historial_data
        self.dashboard_manager = dashboard_manager

        self.title("Historial de Evaluaciones")
        self.geometry("600x400")
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")

        # --- Crear la tabla (Treeview) ---
        self.tree = ttk.Treeview(main_frame, columns=("Tipo", "Calificacion", "Fecha"), show="headings")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Calificacion", text="Calificación")
        self.tree.heading("Fecha", text="Fecha de Realización")
        
        self.tree.column("Tipo", width=80)
        self.tree.column("Calificacion", width=100, anchor="center")
        self.tree.column("Fecha", width=150)

        # Poblar la tabla con los datos del historial
        for item in self.historial_data:
            calificacion_str = f"{item['calificacion']:.2f}%"
            # Guardamos el ID y el tipo en el 'item' para poder recuperarlos después
            self.tree.insert("", "end", iid=f"{item['tipo']}_{item['id']}", values=(item['tipo'], calificacion_str, item['fecha_realizacion']))
        
        self.tree.pack(expand=True, fill="both")

        # Botón para revisar la selección
        btn_revisar = ttk.Button(main_frame, text="Revisar Intento Seleccionado", command=self.revisar_intento)
        btn_revisar.pack(pady=10)

    def revisar_intento(self):
        seleccion = self.tree.focus() # Obtiene el ID del item seleccionado
        if not seleccion:
            messagebox.showwarning("Sin selección", "Por favor, selecciona un intento de la lista para revisar.", parent=self)
            return
        
        # Descomponemos el ID que guardamos, ej: "Prueba_15" -> ["Prueba", "15"]
        tipo, id_evaluacion = seleccion.split('_')
        id_evaluacion = int(id_evaluacion)

        # Pedimos al manager los detalles de esa evaluación
        detalle_data = self.dashboard_manager.obtener_detalle_evaluacion(tipo, id_evaluacion)

        if detalle_data:
            # Abrimos la ventana de revisión con los detalles
            RevisionView(parent=self, controller=self.controller, detalle_evaluacion=detalle_data, tipo_evaluacion=tipo)
        else:
            messagebox.showerror("Error", "No se pudieron cargar los detalles de esta evaluación.", parent=self)