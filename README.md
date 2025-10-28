# 🧩 Proyecto Parcial 2 y Ordinario – “Simulador de Examen de Inglés”

## 🎯 1. Estrategia General del Proyecto

**Nombre del sistema:**  
**Test of English Basic & Intermediate**

**Descripción:**  
El proyecto consiste en el desarrollo de una aplicación informática que permite evaluar el nivel de inglés de los alumnos mediante un simulador de examen.  
El sistema contará con **dos tipos de exámenes**:

- **Simulador de práctica:** 20 preguntas aleatorias (hasta 5 intentos por usuario).  
- **Examen final:** 40 preguntas aleatorias (hasta 2 intentos por usuario).  

El sistema determinará el **nivel del alumno (Básico, Intermedio o Avanzado)** en función de su desempeño, mostrando resultados porcentuales, errores por categoría y tiempo total.

**Objetivo principal:**  
Evaluar y reforzar el aprendizaje del idioma inglés a través de una plataforma de práctica con retroalimentación y estadísticas de rendimiento.

**Tecnologías utilizadas:**
- **Lenguaje:** Python  
- **Base de datos:** MySQL (implementada mediante XAMPP)  
- **Interfaz y dashboard:** Por definir (se añadirá más adelante)

---

## 👥 2. Control de Usuarios

Cada usuario podrá acceder al sistema mediante:
- **Usuario**
- **Matrícula**

Ambos datos se almacenan en la base de datos.  
Cada intento (ya sea práctica o examen) se vincula con la matrícula para mantener un historial individual de resultados.

**Tipos de usuario:**
- `1` → Alumno  
- `2` → Administrador  

---

## 🧠 3. Modelo de Base de Datos (Relacional)

### 💾 Diagrama ER (Mermaid)

```mermaid
erDiagram
    USERS {
        INT id_user PK
        VARCHAR matricula UK
        INT tipo_usuario
        VARCHAR nombre
        VARCHAR usuario
    }

    EXAMENES {
        INT id_examen PK
        VARCHAR matricula FK
        DECIMAL calificacion
        INT aciertos
        INT errores_beginner
        INT errores_elementary
        INT errores_preintermediate
        INT errores_intermediate
        INT errores_upperintermediate
        INT errores_advanced
        INT tiempo_total
        VARCHAR categoria
        DATETIME fecha_realizacion
    }

    PRUEBAS {
        INT id_prueba PK
        VARCHAR matricula FK
        DECIMAL calificacion
        INT aciertos
        INT errores_beginner
        INT errores_elementary
        INT errores_preintermediate
        INT errores_intermediate
        INT errores_upperintermediate
        INT errores_advanced
        INT tiempo_total
        VARCHAR categoria
        DATETIME fecha_realizacion
    }

    USERS ||--o{ EXAMENES : "realiza"
    USERS ||--o{ PRUEBAS : "realiza"
```
**Descripción del modelo:**  
- Cada usuario puede realizar **múltiples exámenes** y **múltiples pruebas de práctica**.  
- Las tablas `EXAMENES` y `PRUEBAS` almacenan calificación, tiempo y errores clasificados por nivel.  
- La columna `categoria` indica el nivel obtenido (Beginner, Elementary, etc.).  
- El campo `tipo_usuario` permite diferenciar administradores de alumnos.

---

## 🔄 4. Diagramas de Flujo

### 🧩 a) Flujo del Usuario

```mermaid
flowchart TD
    A[Inicio] --> B[Ingresar Usuario y Matrícula]
    B --> C[Seleccionar tipo de simulador: Prueba o Examen]
    C --> D[Cargar preguntas aleatorias]
    D --> E[Contestar pregunta]
    E --> F{¿Tiempo menor a 1 min?}
    F -- No --> G[Contar como error y avanzar]
    F -- Sí --> H[Guardar respuesta]
    H --> I{¿Hay más preguntas?}
    I -- Sí --> E
    I -- No --> J[Calcular aciertos y errores]
    J --> K[Determinar categoría final]
    K --> L[Mostrar resultado y calificación]
    L --> M[Fin]
```
### 🧩 b) Flujo del Administrador

```mermaid
flowchart TD
    A[Inicio] --> B[Iniciar sesión como administrador]
    B --> C[Consultar resultados de usuarios]
    C --> D[Filtrar por tipo de examen o fecha]
    D --> E[Visualizar estadísticas globales]
```
## 📘 Notas finales

- Cada pregunta tiene un tiempo límite de **1 minuto**; si no se responde, se marca como errónea.  
- Las preguntas se cargan **de forma aleatoria** para evitar repeticiones dentro del mismo intento.  
- Los resultados se almacenan automáticamente en la base de datos para generar reportes y dashboards más adelante.  
- Los intentos de práctica están limitados a **5 por usuario**, mientras que los exámenes finales solo se pueden realizar **2 veces**.  
- El sistema determinará el nivel del estudiante según su puntaje final (**Básico**, **Intermedio** o **Avanzado**).  
- La base de datos servirá para registrar intentos, calcular promedios y mostrar estadísticas comparativas entre pruebas y exámenes finales.
