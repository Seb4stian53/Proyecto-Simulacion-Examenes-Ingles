import random
import pandas as pd
import time

df = pd.read_csv("preguntas_ingles.csv")
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

def validar_respuesta(n_preg):
    start_time = time.time()
    respuesta = input("Ingresa tu respuesta: ")
    elapsed_time = time.time() - start_time

    if elapsed_time > 60:
        print("Tiempo agotado. Respuesta inválida.")
        return

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

errores = [0,0,0,0,0,0]

def generar_cuestionario_20():
    num_preguntas = []
    
    num_preguntas.extend(random.sample(range(1, 10), 3))
    num_preguntas.extend(random.sample(range(11, 25), 3))
    num_preguntas.extend(random.sample(range(26, 40), 4))
    num_preguntas.extend(random.sample(range(41, 60), 5))
    num_preguntas.extend(random.sample(range(61, 70), 3))
    num_preguntas.extend(random.sample(range(71, 75), 2))    

    random.shuffle(num_preguntas)

    for i in range (len(num_preguntas)): 
        pregunta = df.iloc[num_preguntas[i]]

        print(f"{num_preguntas[i]}. Selecciona la respueta correcta")
        #print(f"{i+1}. Selecciona la respueta correcta")
        print(pregunta['pregunta'].replace("\\n", "\n"))
        print(f"A. {pregunta['a']}\nB. {pregunta['b']}\nC. {pregunta['c']}\nD. {pregunta['d']}\n")
        validar_respuesta(num_preguntas[i])

    cant_errores = 0

    for i in range (len(errores)):
        cant_errores += errores[i] 

    promedio = (20-cant_errores)/20

    print(f"Tu promedio es: {promedio*100}%")
    print(f"Tu categoria es: {obtener_clasificacion()}")
    return 