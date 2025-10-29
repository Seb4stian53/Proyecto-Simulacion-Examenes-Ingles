import random
import pandas as pd
import tkinter as tk

df = pd.read_csv("formularios/preguntas_ingles.csv")
df = df.fillna("")

#num_pregunta = pregunta['numero']

def obtener_categoria(num_pregunta):
    if 0 < num_pregunta <= 10:
        categoria = 0
    elif num_pregunta <= 25:
        categoria = 1
    elif num_pregunta <= 40:
        categoria = 2
    elif num_pregunta <= 60:
        categoria = 3
    elif num_pregunta <= 70:
        categoria = 4
    elif num_pregunta <= 75:
        categoria = 5
    return categoria

#print(obtener_categoria(num_pregunta))

errores = [0,0,0,0,0,0]

def validar_respuesta(n_preg, respuesta):
    if df['respuestas'].iloc[n_preg-1] == respuesta:
        print("Respuesta correcta")
    else:
        categoria = obtener_categoria(n_preg)
        errores[categoria] += 1
        print("Respuesta incorrecta")

def obtener_clasificacion():
    categorias = [
        ("Begginer", 0, 2),
        ("Elementary", 1, 3),
        ("Pre-intermediate", 2, 3),
        ("Intermediate", 3, 4),
        ("Upper-intermediate", 4, 2),
        ("Upper-intermediate", 5, 2),
    ]

    for nombre, indice, limite in categorias:
        if errores[indice] >= limite:
            return nombre

    return "Advanced"

def generar_lista_preguntas_20():
    num_preguntas = []
    
    num_preguntas.extend(random.sample(range(1, 10), 3))
    num_preguntas.extend(random.sample(range(11, 25), 3))
    num_preguntas.extend(random.sample(range(26, 40), 4))
    num_preguntas.extend(random.sample(range(41, 60), 5))
    num_preguntas.extend(random.sample(range(61, 70), 3))
    num_preguntas.extend(random.sample(range(71, 75), 2))    

    random.shuffle(num_preguntas)
    return num_preguntas

def generar_lista_preguntas_40():
    num_preguntas = []
    
    num_preguntas.extend(random.sample(range(1, 10), 6))
    num_preguntas.extend(random.sample(range(11, 25), 6))
    num_preguntas.extend(random.sample(range(26, 40), 8))
    num_preguntas.extend(random.sample(range(41, 60), 10))
    num_preguntas.extend(random.sample(range(61, 70), 6))
    num_preguntas.extend(random.sample(range(71, 75), 4))      

    random.shuffle(num_preguntas)
    return num_preguntas

errores = [0,0,0,0,0,0]

def generar_cuestionario_tkinter(num_preguntas):
    n_preg = 0
    root = tk.Tk()
    root.title("Cuestionario de inglés")
    root.geometry("600x400")

    pregunta = df.iloc[num_preguntas[n_preg]]
    texto_pregunta = pregunta['pregunta'].replace("\\n", "\n")
    pregunta_texto = f"{n_preg + 1}. {texto_pregunta}"

    label_pregunta = tk.Label(root, text=(pregunta_texto))
    label_pregunta.pack()

    selected_option = tk.IntVar()
    selected_option.set(0) 

    radioa = tk.Radiobutton(root, variable=selected_option, text=pregunta['a'], value=1)
    radiob = tk.Radiobutton(root, variable=selected_option, text=pregunta['b'], value=2)
    radioc = tk.Radiobutton(root, variable=selected_option, text=pregunta['c'], value=3)
    radiod = tk.Radiobutton(root, variable=selected_option, text=pregunta['d'], value=4)

    radioa.pack()
    radiob.pack()
    radioc.pack()
    radiod.pack()

    def on_button_click():
        nonlocal n_preg

        if selected_option.get() == 0:
            return
        
        opciones_map = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

        opcion_seleccionada = selected_option.get()

        if opcion_seleccionada in opciones_map:
            validar_respuesta(num_preguntas[n_preg] + 1, opciones_map[opcion_seleccionada])
        
        selected_option.set(0) 

        n_preg += 1
        if n_preg < len(num_preguntas):
            pregunta = df.iloc[num_preguntas[n_preg]]
            texto_pregunta = pregunta['pregunta'].replace("\\n", "\n")
            pregunta_texto = f"{num_preguntas[n_preg] + 1}. {texto_pregunta}"
            label_pregunta.config(text=pregunta_texto)
            radioa.config(text=pregunta['a'])
            radiob.config(text=pregunta['b'])
            radioc.config(text=pregunta['c'])
            radiod.config(text=pregunta['d'])
        else:
            cant_errores = 0
            for i in range (len(errores)):
                cant_errores += errores[i] 

            promedio = (len(num_preguntas)-cant_errores)/len(num_preguntas)

            print(f"Tu promedio es: {promedio*100}%")
            print(f"Tu categoria es: {obtener_clasificacion()}")

            print("Fin del cuestionario")
            root.quit()

    button = tk.Button(root, text="Siguiente", command=on_button_click)
    button.pack()
    root.mainloop()
    return 

generar_cuestionario_tkinter(generar_lista_preguntas_20())