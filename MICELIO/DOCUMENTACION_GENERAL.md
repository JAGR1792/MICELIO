# 🍄 Manual Maestro de MICELIO: El Lenguaje de la Esencia Artificial

Bienvenido a la documentación oficial de **MICELIO**. Este manual está diseñado para llevarte desde el "Hola Mundo" hasta la implementación de redes neuronales profundas, todo bajo un enfoque de **programación funcional** y **DSL para Machine Learning**.

---

## 💎 1. Filosofía del Lenguaje
Micelio es un lenguaje de dominio específico (DSL) cuya meta es eliminar las "cajas negras" (librerías externas como Scikit-Learn o Numpy) para que el estudiante implemente los algoritmos desde su base matemática.

**Principales Pilares:**
1. **Todo es Micelio:** Las matemáticas, matrices y redes están escritas en el propio lenguaje.
2. **Funcionalismo:** Las funciones son ciudadanos de primera clase.
3. **Simplicidad Pedagógica:** Errores que te enseñan qué hiciste mal.

---

## 🛠️ 2. Guía Rápida de Sintaxis

### Variables y Constantes
```micelio
var nombre = "Micelio"  # Variable mutable
const PI = 3.1415       # Constante
```

### Tipos de Datos
- **Números:** `10`, `3.14`
- **Textos:** `"Hola"`
- **Listas:** `[1, 2, 3]`
- **Diccionarios:** `{"clave": "valor"}`
- **Booleanos:** `verdadero`, `falso`
- **Nulo:** `nulo`

### Control de Flujo
```micelio
# Condicionales
si (x > 0) { ... } sino_si (x < 0) { ... } sino { ... }

# Ciclos
mientras (condicion) { ... }
para i en rango(10) { ... }
para elemento en lista { ... }
```

---

## 🧩 3. Programación Funcional Avanzada

Micelio brilla en su capacidad funcional. Puedes encadenar operaciones usando el operador **Pipe** (`|>`).

### Map, Filter y Reduce
```micelio
var lista = [1, 2, 3, 4, 5]

# Obtener suma de cuadrados de los pares
var resultado = lista 
    |> filter(funcion(x) { regresa x % 2 == 0 }) 
    |> map(funcion(x) { regresa x * x }) 
    |> reduce(funcion(a, b) { regresa a + b }, 0)
```

### Closures
```micelio
funcion crear_sumador(n) {
    regresa funcion(x) { regresa x + n }
}
var suma5 = crear_sumador(5)
imp suma5(10) # Resultado: 15
```

---

## 🔲 4. Álgebra Lineal (matriz.mice)

Micelio incluye un motor matricial robusto escrito desde cero.

```micelio
importar "matriz.mice" como mat

var A = [[1, 2], [3, 4]]
var B = [[5, 6], [7, 8]]

var C = mat.multiplicar(A, B)  # Producto matricial
var det = mat.determinante(A)   # LU o Sarrus
var inv = mat.inversa(A)        # Gauss-Jordan
```

---

## 🧠 5. Machine Learning (ml.mice y dl.mice)

Aquí es donde Micelio cumple su propósito como DSL para IA.

### Neurona Artificial (Perceptrón)
Puedes programar una neurona manualmente definiendo sus pesos y función de activación:
```micelio
funcion neurona(X, W, b) {
    var z = (X[0]*W[0] + X[1]*W[1]) + b
    regresa 1 / (1 + exp(-z)) # Activación Sigmoide
}
```

### Regresión Lineal y Logística
```micelio
importar "ml.mice" como ml

var modelo = ml.regresion_lineal(X, Y)
var prediccion = ml.predecir_lineal(nuevo_x, modelo)
```

### Redes Neuronales Profundas (MLP)
Micelio soporta redes multicapa con Backpropagation:

```micelio
importar "dl.mice" como dl

# Definir arquitectura
var arq = [
    {"in": 4, "out": 10, "act": "relu"},
    {"in": 10, "out": 3, "act": "softmax"}
]

var red = dl.perceptron_multicapa(arq)
dl.entrenar_red(red, X_train, Y_train, epochs=1000, lr=0.1)
```

---

## 📈 6. Visualización y Datos

### Gráficas (grafico.mice)
Genera archivos PPM que pueden convertirse a imágenes:
```micelio
importar "grafico.mice" como g
g.plot(X, Y)
g.mostrar()
```

### Archivos (archivo.mice)
Maneja tus datasets CSV o TXT:
```micelio
importar "archivo.mice" como arc
var datos = arc.leer("dataset.csv")
```

---

## 🎓 7. Guía para el Estudiante (Requerimientos del Profesor)

Si estás replicando el cuaderno de **RNA Intro**, aquí tienes cómo mapear las funciones de Scikit-Learn a Micelio:

| Concepto Python (Sklearn) | Concepto Micelio |
| :--- | :--- |
| `Perceptron.fit()` | `ml.regresion_logistica()` o `dl.entrenar_red()` |
| `MLPClassifier()` | `dl.perceptron_multicapa()` |
| `np.dot(A, B)` | `mat.multiplicar(A, B)` |
| `plt.plot()` | `grafico.plot()` |
| `Sigmoid` / `ReLU` | `dl.sigmoid()` / `dl.relu()` |

Para ejemplos completos, revisa la carpeta `/ejemplos` en la raíz del proyecto.
