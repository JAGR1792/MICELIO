# 🍄 LIBRO BLANCO DE MICELIO (MICELIO WHITE PAPER)
**Versión: 2.0 | El Lenguaje de la Esencia Artificial**

Micelio es un lenguaje de programación de dominio específico (DSL) diseñado para la implementación de algoritmos de Inteligencia Artificial desde su base matemática, siguiendo un paradigma de programación funcional y estructural.

---

## 📑 CONTENIDO
1. [Introducción y Filosofía](#1-introducción-y-filosofía)
2. [Guía de Sintaxis Completa](#2-guía-de-sintaxis-completa)
3. [El Paradigma Funcional](#3-el-paradigma-funcional)
4. [Álgebra Lineal desde Cero](#4-álgebra-lineal-desde-cero)
5. [Machine Learning Clásico](#5-machine-learning-clásico)
6. [Deep Learning: El Motor de Redes Neuronales](#6-deep-learning-el-motor-de-redes-neuronales)
7. [Visualización y I/O](#7-visualización-y-io)
8. [Guía para el Estudiante (Sklearn to Micelio)](#8-guía-para-el-estudiante)

---

## 1. Introducción y Filosofía
Micelio nace bajo la premisa "Para entender, hay que construir". A diferencia de otros lenguajes que dependen de librerías como NumPy o Scikit-Learn, Micelio obliga a que cada operación matricial, cada derivada y cada ajuste de pesos sea explícito y comprensible.

---

## 2. Guía de Sintaxis Completa

### Variables y Ámbito (Scope)
```micelio
var x = 10         # Variable global o local al bloque
const E = 2.718    # Constante inmutable
```

### Estructuras de Datos
- **Listas:** Dinámicas y heterogéneas. `var l = [1, "dos", [3]]`. Soportan `.agregar(v)` y `.longitud()`.
- **Diccionarios:** Pares clave-valor. `var d = {"in": 4, "out": 2}`.
- **Sets:** Colecciones de elementos únicos. `var s = set(1, 2, 2)`.

### Control de Flujo Avanzado
```micelio
# Condicionales
si (condicion) { ... } sino_si (otra) { ... } sino { ... }

# Ciclos
mientras (x < 10) { x++ }
para i en rango(0, 10, 1) { imp i } # inicio, fin, paso
para elemento en mi_lista { imp elemento }
```

---

## 3. El Paradigma Funcional
Micelio trata a las funciones como **ciudadanos de primera clase**.

### Funciones de Orden Superior
```micelio
funcion ejecutar(f, x) { regresa f(x) }
var res = ejecutar(funcion(n){ regresa n * n }, 5)
```

### El Operador Pipe (`|>`)
Permite encadenar transformaciones de datos de forma elegante:
```micelio
var resultado = datos |> filter(es_par) |> map(cuadrado) |> reduce(sumar, 0)
```

### Closures y Currificación
```micelio
funcion potencia(n) {
    regresa funcion(x) { regresa x ** n }
}
var al_cubo = potencia(3)
imp al_cubo(2) # 8
```

---

## 4. Álgebra Lineal desde Cero (`matriz.mice`)
El corazón matemático de Micelio.

- `mat.multiplicar(A, B)`: Producto matricial (O(n^3)).
- `mat.determinante(M)`: Implementación de LU para matrices grandes y Sarrus para 3x3.
- `mat.inversa(M)`: Eliminación de Gauss-Jordan con pivoteo parcial.
- `mat.transpuesta(M)`: Rotación de ejes.

---

## 5. Machine Learning Clásico (`ml.mice`)
Implementaciones estructurales de algoritmos base.

### Regresión Lineal Matricial
Resuelve `beta = (X'X)^-1 X'y` usando el motor de álgebra lineal de Micelio.

### K-Means Clustering
Algoritmo iterativo de asignación de centroides con soporte visual mediante `grafico.mice`.

---

## 6. Deep Learning: El Motor de Redes Neuronales (`dl.mice`)
Un framework completo de redes neuronales profundas.

### Arquitectura Modular
```micelio
var arq = [
    {"in": 2, "out": 4, "act": "relu"},
    {"in": 4, "out": 2, "act": "softmax"}
]
```

### Forward & Backpropagation
- **Forward:** Propaga la señal calculando `Z = WX + b`.
- **Backward:** Calcula gradientes usando la regla de la cadena y actualiza pesos mediante SGD (Stochastic Gradient Descent).

### Funciones de Activación
- **ReLU:** `max(0, x)` para capas ocultas.
- **Sigmoid:** Para clasificación binaria.
- **Softmax:** Para clasificación multiclase (probabilidades normalizadas).

---

## 7. Visualización y I/O

### Graficación (`grafico.mice`)
Micelio renderiza sus propios buffers de imagen.
```micelio
g.set_titulo("Curva de Aprendizaje")
g.plot(X_epochs, Y_loss)
g.mostrar() # Genera y abre un archivo PPM/BMP
```

---

## 8. Guía para el Estudiante

| Tarea | Scikit-Learn / Numpy | Micelio |
| :--- | :--- | :--- |
| Multiplicar Matrices | `A @ B` | `mat.multiplicar(A, B)` |
| Inversa | `np.linalg.inv(A)` | `mat.inversa(A)` |
| Entrenar Red | `MLP.fit(X, y)` | `dl.entrenar_red(m, X, Y, ep, lr)` |
| Predicción | `MLP.predict(X)` | `dl.forward(m, X)["salida"]` |
| Plotear | `plt.scatter(x, y)` | `g.scatter(X_puntos, clases)` |

---

Para más detalles, consulta la carpeta `/ejemplos` con sus 14 scripts demostrativos.
