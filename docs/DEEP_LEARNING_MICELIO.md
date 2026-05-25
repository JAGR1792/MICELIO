# Deep Learning en MICELIO

## Prefacio

Este documento describe la implementación de redes neuronales artificiales y deep learning en MICELIO. Está dirigido a personas que nunca han trabajado con frameworks como TensorFlow o PyTorch, y que quizá tampoco conocen los fundamentos teóricos del aprendizaje automático. Cada concepto se presenta desde su base, incluyendo el propósito de cada operación y el significado de los resultados.

La implementación completa está escrita en MICELIO puro, sin dependencias externas de machine learning. Las funciones matemáticas (exponencial, raíz cuadrada) se implementan mediante series de Taylor y Newton-Raphson, el generador de números aleatorios mediante un algoritmo congruencial lineal, y el ordenamiento mediante Quicksort.

---

## Indice

1. [Fundamentos: que es una red neuronal](#1-fundamentos-que-es-una-red-neuronal)
2. [Componentes de una red](#2-componentes-de-una-red)
3. [Forward propagation: como hace una prediccion la red](#3-forward-propagation-como-hace-una-prediccion-la-red)
4. [Backpropagation: como aprende la red de sus errores](#4-backpropagation-como-aprende-la-red-de-sus-errores)
5. [El ciclo de entrenamiento completo](#5-el-ciclo-de-entrenamiento-completo)
6. [API del modulo dl.mice](#6-api-del-modulo-dlmice)
7. [Ejemplo 1: XOR (clasificacion binaria)](#7-ejemplo-1-xor-clasificacion-binaria)
8. [Ejemplo 2: Caperucita Roja (multi-etiqueta)](#8-ejemplo-2-caperucita-roja-multi-etiqueta)
9. [Ejemplo 3: Autoencoder (compresion de datos)](#9-ejemplo-3-autoencoder-compresion-de-datos)
10. [Ejemplo 4: Clasificador Iris (softmax)](#10-ejemplo-4-clasificador-iris-softmax)
11. [Matematicas subyacentes](#11-matematicas-subyacentes)
12. [Arquitectura interna y conexion con Python](#12-arquitectura-interna-y-conexion-con-python)
13. [Limitaciones actuales](#13-limitaciones-actuales)

---

## 1. Fundamentos: que es una red neuronal

### 1.1 La idea central

Una red neuronal artificial es un programa que, en lugar de recibir instrucciones explicitas sobre como resolver un problema, **aprende a resolverlo a partir de ejemplos**.

El proceso es siempre el mismo:

```
1. Se le muestran ejemplos a la red (datos de entrada)
2. La red produce una respuesta (prediccion)
3. Se compara la respuesta con la respuesta correcta
4. Se calcula el error
5. La red ajusta sus parametros internos para reducir ese error
6. Se repite hasta que el error es aceptable
```

Esto se conoce como **aprendizaje supervisado**: la red aprende de ejemplos etiquetados.

### 1.2 La neurona artificial

Una neurona artificial es la unidad minima de procesamiento. Recibe varias señales de entrada, las combina, y decide si "se activa" o no.

**Analogia:** Una neurona biologica recibe señales de otras neuronas a traves de sus dendritas. Si la suma de esas señales supera un umbral, la neurona "dispara" una señal a traves de su axon. La neurona artificial hace lo mismo con numeros.

Estructuralmente, una neurona hace dos operaciones en secuencia:

```
Entrada 1 ──→ (peso 1)
Entrada 2 ──→ (peso 2) ──→ SUMA ──→ ACTIVACION ──→ Salida
Entrada 3 ──→ (peso 3)
```

**Primera operacion: suma ponderada.** Cada entrada se multiplica por un peso (que representa su importancia) y se suman todos los productos, mas un sesgo (bias):

```
z = (x1 * w1) + (x2 * w2) + (x3 * w3) + b
```

Donde:
- `x1, x2, x3` son las entradas
- `w1, w2, w3` son los pesos (parametros que la red aprende)
- `b` es el sesgo (otro parametro aprendido)
- `z` es el resultado de la suma ponderada

**Segunda operacion: funcion de activacion.** Se aplica una funcion no lineal a `z` para producir la salida de la neurona:

```
salida = activacion(z)
```

Esta funcion de activacion es crucial: sin ella, la red solo podria aprender relaciones lineales, y apilar varias capas no daria ninguna ventaja respecto a una sola.

### 1.3 Capas y redes profundas

Varias neuronas agrupadas forman una **capa** (layer). Varias capas apiladas forman una **red profunda** (deep neural network).

```
Entrada → [Capa oculta 1] → [Capa oculta 2] → [Capa de salida]
```

- **Capa de entrada:** recibe los datos sin procesar (por ejemplo, los pixeles de una imagen)
- **Capas ocultas:** procesan la informacion progresivamente, extrayendo patrones cada vez mas abstractos
- **Capa de salida:** produce la respuesta final de la red

Una red con multiples capas ocultas se denomina **Perceptron Multicapa (MLP)** y es la arquitectura fundamental del deep learning.

---

## 2. Componentes de una red

### 2.1 Pesos y sesgos

Los **pesos** (weights, simbolo `W`) son numeros que determinan la influencia de cada entrada sobre cada neurona. Si un peso es grande y positivo, la entrada correspondiente tiende a activar la neurona. Si es grande y negativo, tiende a inhibirla.

Los **sesgos** (biases, simbolo `b`) son numeros que determinan el umbral de activacion de la neurona. Un sesgo alto significa que la neurona se activa facilmente; uno bajo, que necesita mucha evidencia para activarse.

Durante el entrenamiento, la red ajusta estos valores para minimizar el error.

### 2.2 Funciones de activacion

Una funcion de activacion decide si una neurona debe "disparar" o no, y con que intensidad. Las tres funciones implementadas en MICELIO son:

#### Sigmoide

**Formula:** `sigma(x) = 1 / (1 + e^(-x))`

**Forma:** Curva en forma de S que transforma cualquier numero real en un valor entre 0 y 1.

```
    1 ───────────────
      │            ╱
      │          ╱
      │        ╱
      │      ╱
    0 ────╯
```

**Para que se usa:** Cuando la salida debe interpretarse como una **probabilidad**. En clasificacion binaria, la neurona de salida con sigmoide indica la probabilidad de pertenecer a la clase positiva. En problemas multi-etiqueta (donde varias opciones pueden ser ciertas a la vez), cada neurona de salida usa sigmoide independientemente.

**Ejemplo:** si la salida de una neurona con sigmoide es 0.87, se interpreta como "87% de probabilidad de que esto sea correcto".

#### ReLU (Rectified Linear Unit)

**Formula:** `ReLU(x) = max(0, x)`

**Forma:** Si la entrada es positiva, la deja pasar intacta. Si es negativa, la convierte en cero.

```
      │          ╱
      │        ╱
      │      ╱
      │    ╱
    0 ──╯
```

**Para que se usa:** En capas ocultas. Es la activacion mas utilizada en deep learning porque:
- Es computacionalmente simple (solo compara con cero)
- No satura para valores positivos grandes (a diferencia de sigmoide)
- Ayuda a mitigar el problema del desvanecimiento del gradiente

#### Softmax

**Formula:** `softmax(x_i) = e^(x_i) / sum(e^(x_j))` (con estabilizacion numerica restando el maximo)

**Forma:** Convierte un vector de numeros reales en una distribucion de probabilidad donde todos los valores suman 1.

**Para que se usa:** En la capa de salida de problemas de **clasificacion multiclase**, donde exactamente una clase debe ser seleccionada entre varias. Cada neurona de salida representa la probabilidad de una clase, y la clase con mayor probabilidad es la prediccion.

**Ejemplo:** si la salida softmax es `[0.70, 0.20, 0.10]`, la clase 0 tiene 70% de probabilidad, la clase 1 tiene 20%, y la clase 2 tiene 10%.

### 2.3 Inicializacion de pesos

Antes de entrenar, los pesos deben inicializarse con valores adecuados. Si todos los pesos comienzan en cero, todas las neuronas de una misma capa aprenderian exactamente lo mismo (simetria). Si son muy grandes, las activaciones se saturan. Si son muy pequenos, las senales se desvanecen.

MICELIO usa **inicializacion Xavier uniforme** (Glorot uniform):

```
W[i][j] = U(-1, 1) * sqrt(6 / (n_entrada + n_salida))
```

Donde `U(-1, 1)` es un numero aleatorio uniforme entre -1 y 1, y `n_entrada` y `n_salida` son las cantidades de neuronas de entrada y salida de la capa.

Esta inicializacion mantiene la varianza de las activaciones estable a traves de las capas, evitando que las senales crezcan o se reduzcan demasiado.

### 2.4 Funcion de perdida

La funcion de perdida (loss function) mide **que tan lejos** estan las predicciones de la red de los valores correctos. MICELIO implementa el **Error Cuadratico Medio (MSE)**:

```
MSE = (1 / (m * c)) * sum_i sum_j (y_real[i][j] - y_pred[i][j])^2
```

Donde `m` es el numero de muestras y `c` el numero de salidas por muestra.

- MSE = 0: prediccion perfecta
- MSE pequeno: la red se aproxima bien
- MSE grande: la red esta lejos de acertar

---

## 3. Forward propagation: como hace una prediccion la red

### 3.1 Definicion

Forward propagation (propagacion hacia adelante) es el proceso mediante el cual la red transforma una entrada en una prediccion. Los datos fluyen desde la capa de entrada, atraviesan las capas ocultas, y llegan a la capa de salida.

### 3.2 Algoritmo paso a paso

Para cada capa `l` de la red, desde la primera hasta la ultima:

**Paso 1: Transformacion lineal**

```
Z[l] = A[l-1] * W[l] + b[l]
```

Donde:
- `A[l-1]` es la activacion de la capa anterior (o la entrada `X` si es la primera capa)
- `W[l]` son los pesos de la capa actual
- `b[l]` es el sesgo de la capa actual
- `Z[l]` es el resultado de la combinacion lineal

**Para que sirve:** Esta operacion decide cuanto "escucha" la neurona a cada entrada, segun los pesos aprendidos.

**Paso 2: Aplicacion de la funcion de activacion**

```
A[l] = g[l](Z[l])
```

Donde `g[l]` es la funcion de activacion de la capa `l` (ReLU, sigmoide, softmax o lineal).

**Para que sirve:** Introduce no-linealidad. Sin este paso, apilar capas no tendria sentido porque toda la red seria equivalente a una sola capa lineal.

### 3.3 Implementacion en MICELIO

```mice
funcion forward(modelo, X) {
    var activaciones = [X]
    var actual = X

    para capa en modelo["capas"] {
        # Z = A_prev * W  (multiplicacion matricial)
        var Z = mat.multiplicar(actual, capa["W"])

        # Sumar el sesgo (bias) a cada fila (cada muestra)
        para fi en rango(mat.filas(Z)) {
            para ci en rango(mat.columnas(Z)) {
                Z[fi][ci] = Z[fi][ci] + capa["b"][0][ci]
            }
        }

        # Aplicar la funcion de activacion correspondiente
        si (capa["act"] == "relu") {
            actual = relu(Z)
        } sino_si (capa["act"] == "sigmoid") {
            actual = sigmoid(Z)
        } sino_si (capa["act"] == "softmax") {
            actual = softmax(Z)
        } sino {
            actual = Z   # activacion lineal (identidad)
        }

        # Guardar la activacion para usarla en backpropagation
        activaciones.agregar(actual)
    }

    # Retornar la prediccion y todas las activaciones intermedias
    regresa {"salida": actual, "activaciones": activaciones}
}
```

**Que retorna esta funcion:**
- `"salida"`: la prediccion de la red (matriz de tamano `m x c`, donde `m` es el numero de muestras y `c` el numero de neuronas de salida)
- `"activaciones"`: lista con la entrada y las activaciones de todas las capas, necesaria para el backpropagation

---

## 4. Backpropagation: como aprende la red de sus errores

### 4.1 Definicion

Backpropagation (retropropagacion del error) es el algoritmo que calcula como debe ajustarse cada peso para reducir el error de la red. El error "viaja hacia atras" desde la capa de salida hasta la primera capa oculta.

### 4.2 Intuicion

Cuando la red se equivoca, no toda la culpa es de la ultima capa. Cada capa contribuyo al error. Backpropagation reparte la culpa proporcionalmente:

1. Calcula el error en la salida
2. Determina cuanto contribuyo cada peso de la ultima capa a ese error
3. Propaga ese error hacia la capa anterior
4. Repite hasta llegar a la primera capa

### 4.3 Algoritmo paso a paso

**Paso 1: Error en la capa de salida**

```
delta = prediccion - Y
```

Donde `Y` son los valores correctos. Esta diferencia, elemento a elemento, es la direccion en que debe moverse la prediccion para acercarse a la realidad.

**Paso 2: Para cada capa, desde la ultima hasta la primera**

Para cada capa `i` (en orden inverso):

```
# Gradiente de los pesos: cuanto contribuyo cada peso al error
dW = (A_prev)^T * delta

# Gradiente del sesgo: suma del error por cada neurona
db = sum(delta, axis=0)

# Propagar el error a la capa anterior (si no es la primera)
error_oculto = delta * W^T

# Aplicar la derivada de la activacion de la capa anterior
si (activacion_anterior == "relu"):
    delta = error_oculto ⊙ ReLU'(A_prev)
sino si (activacion_anterior == "sigmoid"):
    delta = error_oculto ⊙ sigmoid'(A_prev)
sino:
    delta = error_oculto

# Actualizar pesos y sesgos
W = W - lr * dW
b = b - lr * db
```

**Paso 3: Repetir**

Se itera sobre todo el conjunto de datos tantas veces como epocas (epochs) se hayan configurado.

### 4.4 Las derivadas de activacion en MICELIO

Cada funcion de activacion tiene su correspondiente derivada, necesaria para backpropagation:

**Derivada de sigmoide:**
```
sigmoid'(x) = sigmoid(x) * (1 - sigmoid(x))
```
En MICELIO: `m[i][j] * (1 - m[i][j])` donde `m` es la salida de sigmoide.

**Derivada de ReLU:**
```
ReLU'(x) = 1  si x > 0
           0  si x <= 0
```
En MICELIO: `si (m[i][j] > 0) { 1 } sino { 0 }`.

### 4.5 Tasa de aprendizaje (learning rate)

La tasa de aprendizaje `lr` controla que tan grandes son los ajustes en cada paso:

```
nuevo_peso = viejo_peso - lr * gradiente
```

- Un valor alto (ej. 0.5) hace que la red aprenda rapido pero puede ser inestable
- Un valor bajo (ej. 0.01) hace que el aprendizaje sea lento pero estable
- Los valores tipicos estan entre 0.01 y 0.5

---

## 5. El ciclo de entrenamiento completo

El entrenamiento combina forward propagation y backpropagation en un ciclo:

```mice
funcion entrenar_red(modelo, X, Y, epochs, lr) {
    para e en rango(epochs) {
        # 1. Forward: obtener prediccion
        var fwd = forward(modelo, X)
        var pred = fwd["salida"]
        var activaciones = fwd["activaciones"]

        # 2. Error en la salida
        var delta = mat.resta_matrices(pred, Y)

        # 3. Backpropagation: desde la ultima capa hacia atras
        var i = modelo["capas"].longitud() - 1
        mientras (i >= 0) {
            var capa = modelo["capas"][i]
            var A_prev = activaciones[i]

            # Calcular gradientes
            var dW = mat.multiplicar(mat.transpuesta(A_prev), delta)
            var db = mat.ceros(1, mat.columnas(delta))
            para fila_d en delta {
                var c_idx = 0
                mientras (c_idx < fila_d.longitud()) {
                    db[0][c_idx] = db[0][c_idx] + fila_d[c_idx]
                    c_idx = c_idx + 1
                }
            }

            # Propagar error a la capa anterior
            si (i > 0) {
                var error_oculto = mat.multiplicar(delta, mat.transpuesta(capa["W"]))
                var act_prev = modelo["capas"][i-1]["act"]
                si (act_prev == "relu") {
                    delta = hadamard(error_oculto, relu_derivada(activaciones[i]))
                } sino_si (act_prev == "sigmoid") {
                    delta = hadamard(error_oculto, sigmoid_derivada(activaciones[i]))
                } sino {
                    delta = error_oculto
                }
            }

            # Actualizar parametros
            capa["W"] = mat.resta_matrices(capa["W"], mat.escalar(dW, lr))
            capa["b"] = mat.resta_matrices(capa["b"], mat.escalar(db, lr))

            i = i - 1
        }
    }
}


```

El parametro `modelo` se modifica **in-place**: los pesos se actualizan directamente sobre la estructura del modelo, no se retorna un nuevo modelo.

---

## 6. API del modulo dl.mice

Para usar el modulo de deep learning:

```mice
importar "dl.mice" como dl
```

Este modulo internamente importa dos bibliotecas:

- `matriz.mice` como `mat`: provee las operaciones de algebra lineal (multiplicacion de matrices, transpuesta, suma, resta). Todas estas operaciones estan implementadas en MICELIO puro mediante bucles anidados.
- `math.mice` como `math`: provee la funcion `raiz()` (raiz cuadrada mediante Newton-Raphson), usada en la inicializacion Xavier.

La funcion `exp()` que utiliza sigmoide y softmax no viene de `math.mice`, sino del ambito global, donde `builtins.mice` la define mediante una serie de Taylor de 10 terminos implementada en MICELIO puro.

### 6.1 `dl.aplicar(matriz, funcion)`

**Firma:** `aplicar(m, f)`

**Que hace:** Aplica una funcion `f` a cada elemento individual de la matriz `m`. Recorre cada fila y cada elemento, lo pasa por la funcion, y construye una nueva matriz con los resultados.

**Para que se usa:** Es la base de las funciones de activacion. `sigmoid(m)` se implementa como `aplicar(m, sigmoid_esc)`, donde `sigmoid_esc` opera sobre un solo numero.

**Ejemplo:**
```mice
var cuad = funcion (x) { regresa x * x }
dl.aplicar([[1, 2], [3, 4]], cuad)
# → [[1, 4], [9, 16]]
```

### 6.2 `dl.hadamard(m1, m2)`

**Firma:** `hadamard(m1, m2)`

**Que hace:** Multiplica dos matrices elemento por elemento (producto de Hadamard). No es la multiplicacion matricial usual, sino que cada posicion `[i][j]` del resultado es `m1[i][j] * m2[i][j]`. Ambas matrices deben tener las mismas dimensiones.

**Para que se usa:** Exclusivamente en backpropagation, para combinar el error propagado con la derivada de la funcion de activacion: `delta = error_oculto ⊙ derivada(activacion)`.

### 6.3 Funciones de activacion

#### `dl.sigmoid(matriz)`

**Firma:** `sigmoid(m)`

**Formula:** `sigmoid(x) = 1 / (1 + e^(-x))`

**Que hace:** Aplica la funcion sigmoide a cada elemento de la matriz. Cada elemento se transforma a un valor en el intervalo (0, 1).

**Para que se usa:** En capas de salida para problemas de clasificacion binaria o multi-etiqueta. La salida se interpreta como una probabilidad.

**Implementacion:**
```mice
funcion sigmoid_esc(x) { regresa 1 / (1 + exp(-x)) }
funcion sigmoid(m) { regresa aplicar(m, sigmoid_esc) }
```

La funcion `exp()` invocada es la serie de Taylor implementada en `builtins.mice`.

#### `dl.sigmoid_derivada(matriz)`

**Firma:** `sigmoid_derivada(m)`

**Formula:** `sigmoid_derivada(x) = x * (1 - x)`

**Que hace:** Calcula la derivada de la sigmoide. Recibe la **salida** de la sigmoide (no la entrada a la sigmoide). Esto es correcto porque si `a = sigmoid(z)`, entonces `sigmoid'(z) = a * (1 - a)`.

**Para que se usa:** En backpropagation, cuando la capa anterior usa activacion sigmoide.

#### `dl.relu(matriz)`

**Firma:** `relu(m)`

**Formula:** `ReLU(x) = max(0, x)`

**Que hace:** Para cada elemento, si es positivo lo deja igual, si es negativo lo convierte en cero.

**Para que se usa:** En capas ocultas. Es la activacion predeterminada en la mayoria de las redes profundas modernas.

#### `dl.relu_derivada(matriz)`

**Firma:** `relu_derivada(m)`

**Formula:** `ReLU'(x) = 1 si x > 0, 0 si x <= 0`

**Que hace:** Para cada elemento, retorna 1 si es positivo, 0 si es cero o negativo.

**Para que se usa:** En backpropagation, cuando la capa anterior usa activacion ReLU.

#### `dl.softmax(matriz)`

**Firma:** `softmax(m)`

**Formula:** `softmax(x_i) = e^(x_i - max) / sum_j e^(x_j - max)` (version numericamente estable)

**Que hace:** Convierte cada fila de la matriz en una distribucion de probabilidad donde todos los valores son positivos y suman 1.

**Para que se usa:** En la capa de salida para clasificacion multiclase (una opcion entre varias).

**Estabilidad numerica:** La implementacion resta el valor maximo de cada fila antes de calcular la exponencial. Esto evita el desbordamiento que ocurriria con valores grandes (ej. `exp(1000)`).

### 6.4 `dl.perceptron_multicapa(arquitectura)`

**Firma:** `perceptron_multicapa(arquitectura)`

**Que hace:** Crea un modelo de perceptron multicapa (MLP) con la arquitectura especificada. Inicializa los pesos con el metodo Xavier uniforme y los sesgos en cero.

**Parametro `arquitectura`:** Lista de diccionarios, cada uno representando una capa:

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `"in"` | numero | Cantidad de neuronas de entrada de esta capa |
| `"out"` | numero | Cantidad de neuronas de salida de esta capa |
| `"act"` | texto | Funcion de activacion: `"relu"`, `"sigmoid"`, `"softmax"`, `"lineal"` |

**Ejemplo de arquitectura:**
```mice
var arq = [
    {"in": 4, "out": 3, "act": "relu"},      # primera capa oculta
    {"in": 3, "out": 4, "act": "sigmoid"}     # capa de salida
]
```

**Retorno:** Diccionario con la estructura:
```
{
  "capas": [
    {
      "W": [[pesos...]],    # matriz de dimension (in x out)
      "b": [[sesgos...]],   # matriz de dimension (1 x out)
      "act": "relu"
    },
    ...
  ]
}
```

**Inicializacion de pesos (Xavier uniforme):**
```mice
W[i][j] = (aleatorio() * 2 - 1) * math.raiz(6 / (n_in + n_out))
```

Donde `aleatorio()` es el generador congruencial lineal implementado en `builtins.mice`, y `math.raiz()` es la raiz cuadrada mediante Newton-Raphson de `math.mice`.

### 6.5 `dl.forward(modelo, X)`

**Firma:** `forward(modelo, X)`

**Que hace:** Ejecuta una propagacion hacia adelante completa. Toma el modelo y una entrada, y retorna la prediccion.

**Parametros:**
- `modelo`: diccionario retornado por `perceptron_multicapa`
- `X`: matriz de entrada de dimension `(m x n)`, donde `m` es el numero de muestras y `n` el numero de caracteristicas

**Retorno:** Diccionario con dos campos:
- `"salida"`: matriz de prediccion de dimension `(m x c)`, donde `c` es el numero de neuronas de la ultima capa
- `"activaciones"`: lista con la entrada y las activaciones de todas las capas (necesaria para entrenamiento)

**Uso tipico:**
```mice
var resultado = dl.forward(modelo, [[1, 1, 0, 0]])
var prediccion = resultado["salida"]          # la respuesta
var activaciones = resultado["activaciones"]  # estados intermedios
```

### 6.6 `dl.entrenar_red(modelo, X, Y, epochs, lr)`

**Firma:** `entrenar_red(modelo, X, Y, epochs, lr)`

**Que hace:** Entrena la red neuronal usando el algoritmo de descenso de gradiente con backpropagation. El modelo se modifica in-place.

**Parametros:**
- `modelo`: modelo creado con `perceptron_multicapa` (se modifica directamente)
- `X`: datos de entrada, matriz de dimension `(m x n)`
- `Y`: valores objetivo (correctos), matriz de dimension `(m x c)`
- `epochs`: cantidad de iteraciones completas sobre todos los datos
- `lr`: tasa de aprendizaje (learning rate), tipicamente entre 0.01 y 0.5

**Algoritmo interno:**
1. Forward propagation: calcula prediccion y activaciones
2. Calcula el error: `delta = prediccion - Y`
3. Backpropagation: para cada capa en orden inverso, calcula gradientes y propaga el error
4. Actualizacion: `W = W - lr * dW`, `b = b - lr * db`

### 6.7 `dl.error_mse(y_real, y_pred)`

**Firma:** `error_mse(y_real, y_pred)`

**Que hace:** Calcula el Error Cuadratico Medio entre los valores reales y las predicciones.

**Formula:** `MSE = (1 / (f * c)) * sum_i sum_j (real[i][j] - pred[i][j])^2`

**Interpretacion:**
- MSE = 0: la prediccion es exactamente igual al valor real
- MSE bajo: la red se aproxima bien
- MSE alto: la red se equivoca mucho

---

## 7. Ejemplo 1: XOR (clasificacion binaria)

### 7.1 El problema

La compuerta XOR (o exclusivo) es un problema clasico para probar redes neuronales porque **no es linealmente separable**: una sola neurona no puede resolverlo.

```
Entrada:  (x1, x2)
Salida:   0 si x1 = x2, 1 si x1 != x2

Ejemplos:
  (0, 0) → 0
  (0, 1) → 1
  (1, 0) → 1
  (1, 1) → 0
```

Si se grafican estos puntos, los ceros estan en las esquinas opuestas del cuadrado, y los unos en las otras dos. No es posible trazar una linea recta que separe ambas clases. Se necesita al menos una capa oculta que doble el espacio de decision.

### 7.2 Codigo completo

```mice
importar "dl.mice" como dl
```

Esta linea importa el modulo de deep learning. Internamente, `dl.mice` importa `matriz.mice` (para operaciones algebraicas) y `math.mice` (para raiz cuadrada). Las funciones `exp()` y `aleatorio()` se resuelven desde el ambito global, donde `builtins.mice` las define en MICELIO puro.

```mice
var X = [[0,0], [0,1], [1,0], [1,1]]
```

Matriz de entrada: 4 muestras, cada una con 2 caracteristicas (coordenadas x1, x2).

```mice
var Y = [[1,0], [0,1], [0,1], [1,0]]
```

Matriz de salida en codificacion **one-hot**: cada fila tiene un 1 en la posicion de la clase correcta y 0 en las demas.
- `[1,0]` = clase 0 (XOR = 0)
- `[0,1]` = clase 1 (XOR = 1)

```mice
var arq = [
    {"in": 2, "out": 4, "act": "relu"},
    {"in": 4, "out": 2, "act": "softmax"}
]
```

Arquitectura de la red:
- **Capa 1:** 2 neuronas de entrada, 4 neuronas ocultas, activacion ReLU. Esta capa aprende a transformar el espacio de entrada para hacerlo separable.
- **Capa 2:** 4 neuronas de entrada (la salida de la capa anterior), 2 neuronas de salida, activacion softmax. Produce la probabilidad de pertenencia a cada clase.

Se usa softmax porque es un problema de clasificacion donde exactamente una clase debe ser seleccionada.

```mice
var modelo = dl.perceptron_multicapa(arq)
```

Crea la red con pesos inicializados aleatoriamente (metodo Xavier) y sesgos en cero.

```mice
dl.entrenar_red(modelo, X, Y, 2000, 0.1)
```

Entrena la red durante 2000 epocas con tasa de aprendizaje 0.1. En cada epoca se ejecuta forward propagation, se calcula el error, se hace backpropagation, y se actualizan los pesos.

```mice
var res = dl.forward(modelo, X)
imp res["salida"]
```

Evalua la red con los mismos datos de entrenamiento e imprime las predicciones.

### 7.3 Resultado esperado

Despues de 2000 epocas, la salida deberia aproximarse a:

```
[0.99, 0.01]  → clase 0 (para entrada 0,0)
[0.01, 0.99]  → clase 1 (para entrada 0,1)
[0.01, 0.99]  → clase 1 (para entrada 1,0)
[0.99, 0.01]  → clase 0 (para entrada 1,1)
```

Cada fila suma aproximadamente 1 (por softmax). El valor mas alto en cada fila indica la clase predicha. Un valor de 0.99 indica 99% de confianza en la prediccion.

---

## 8. Ejemplo 2: Caperucita Roja (multi-etiqueta)

### 8.1 El problema

Este ejemplo modela las reacciones de Caperucita Roja ante distintos personajes del cuento. Es un problema de clasificacion **multi-etiqueta**: un personaje puede activar varias reacciones simultaneamente.

**Datos de entrenamiento (4 rasgos de entrada):**

| Personaje | Orejas grandes | Dientes grandes | Apuesto | Arrugado |
|-----------|:---:|:---:|:---:|:---:|
| Lobo | 1 | 1 | 0 | 0 |
| Principe | 0 | 1 | 1 | 0 |
| Abuelita | 0 | 0 | 0 | 1 |

**Reacciones esperadas (4 salidas):**

| Personaje | Gritar | Abrazar | Dar comida | Besar |
|-----------|:------:|:-------:|:----------:|:-----:|
| Lobo | 1 | 0 | 0 | 0 |
| Principe | 0 | 0 | 1 | 1 |
| Abuelita | 0 | 1 | 1 | 0 |

Observe que el Principe activa dos salidas (comida y besar) simultaneamente. Esto es multi-etiqueta y requiere sigmoide en la salida (no softmax), porque cada neurona debe decidir independientemente si su etiqueta esta presente.

### 8.2 Codigo completo

```mice
importar "dl.mice" como dl
```

Importa el modulo de deep learning. Este modulo a su vez importa `matriz.mice` (operaciones matriciales) y `math.mice` (raiz cuadrada). La funcion `exp()` que usara sigmoide proviene de `builtins.mice` (serie de Taylor). No es necesario importar nada adicional.

```mice
var X = [
    [1, 1, 0, 0],   # Lobo: orejas grandes, dientes grandes
    [0, 1, 1, 0],   # Principe: dientes grandes, apuesto
    [0, 0, 0, 1]    # Abuelita: arrugada
]
```

Matriz de 3 muestras y 4 caracteristicas. Cada fila representa un personaje. Cada columna representa un rasgo binario (1 = presente, 0 = ausente).

```mice
var Y = [
    [1, 0, 0, 0],   # Lobo → solo gritar
    [0, 0, 1, 1],   # Principe → dar comida y besar
    [0, 1, 1, 0]    # Abuelita → abrazar y dar comida
]
```

Matriz de 3 muestras y 4 etiquetas. Cada fila representa las reacciones correctas para ese personaje. Multiple 1s por fila indican multiples reacciones simultaneas.

```mice
var arq = [
    {"in": 4, "out": 3, "act": "relu"},
    {"in": 3, "out": 4, "act": "sigmoid"}
]
```

Arquitectura:
- **Capa 1 (oculta):** 4 entradas, 3 neuronas, activacion ReLU. Reduce la dimensionalidad y aprende combinaciones relevantes de los rasgos.
- **Capa 2 (salida):** 3 entradas, 4 salidas, activacion sigmoide. Produce 4 probabilidades independientes entre 0 y 1, una por cada posible reaccion.

Se usa sigmoide en lugar de softmax porque las salidas no son mutuamente excluyentes. Con sigmoide, cada neurona de salida da una probabilidad independiente. Con softmax, las probabilidades sumarian 1, lo que obligaria a elegir una sola reaccion.

```mice
var modelo = dl.perceptron_multicapa(arq)
```

Crea la red. Los pesos se inicializan con Xavier uniforme y los sesgos en cero.

```mice
dl.entrenar_red(modelo, X, Y, 5000, 0.2)
```

Entrena por 5000 epocas con tasa de aprendizaje 0.2. Durante el entrenamiento, el modulo imprime el error MSE cada 200 epocas. Este error deberia disminuir progresivamente, indicando que la red esta aprendiendo.

```mice
var casos = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]]
var nombres = ["Lobo", "Principe", "Abuelita"]
var etiquetas = ["Gritar", "Abrazar", "Comida", "Besar"]

para i en rango(3) {
    var res = dl.forward(modelo, [casos[i]])
    var probs = res["salida"][0]
    imp nombres[i] + ":"
    para j en rango(4) {
        imp "  " + etiquetas[j] + ": " + aTexto(probs[j])
    }
}
```

Evalua la red con cada personaje. Para cada uno, imprime las 4 probabilidades. Una probabilidad cercana a 1 significa que la red predice que esa reaccion ocurrira. Cercana a 0 significa que no.

```mice
var res = dl.forward(modelo, [[1, 1, 0, 1]])
imp res["salida"][0]
```

Evalua un caso mixto: un personaje con orejas grandes, dientes grandes y arrugado (un "Lobo disfrazado de abuelita"). Esto permite ver como la red generaliza a combinaciones no vistas durante el entrenamiento.

### 8.3 Interpretacion de resultados

Un resultado tipico despues de 5000 epocas:

```
Lobo:          Gritar: 0.9999, Abrazar: 0.0001, Comida: 0.0001, Besar: 0.0001
Principe:      Gritar: 0.0001, Abrazar: 0.0001, Comida: 0.9999, Besar: 0.9999
Abuelita:      Gritar: 0.0001, Abrazar: 0.9999, Comida: 0.9999, Besar: 0.0001
Lobo disfraz:  Gritar: 0.9500, Abrazar: 0.1000, Comida: 0.0500, Besar: 0.0200
```

- La red aprendio que el Lobo solo provoca gritos (primer vector de probabilidad)
- El Principe provoca comida y beso (segundo vector, dos valores altos)
- La Abuelita provoca abrazo y comida (tercer vector, dos valores altos)
- El Lobo disfrazado activa principalmente "Gritar" (el rasgo mas distintivo del Lobo) pero con menor confianza que el Lobo puro, porque la presencia de arrugas (rasgo de abuelita) introduce ambiguedad

---

## 9. Ejemplo 3: Autoencoder (compresion de datos)

### 9.1 El problema

Un autoencoder es una red que aprende a **reconstruir su propia entrada**. Tiene una capa oculta con menos neuronas que la entrada (cuello de botella), que fuerza a la red a aprender una representacion comprimida de los datos.

```
Entrada (4) → Comprime → Cuello de botella (2) → Expande → Salida (4)
```

La utilidad del autoencoder es que el cuello de botella aprende a capturar la informacion esencial de los datos, descartando el ruido. Esto sirve para:
- Reduccion de dimensionalidad
- Deteccion de anomalias (lo que no se reconstruye bien es anomalo)
- Aprendizaje de representaciones latentes

### 9.2 Codigo completo

```mice
importar "dl.mice" como dl
```

```mice
var X = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]
```

Cuatro patrones de 4 bits, cada uno con un solo bit activo. La red debe aprender a comprimir cada patron a 2 numeros y luego reconstruirlo.

```mice
var arq = [
    {"in": 4, "out": 2, "act": "relu"},
    {"in": 2, "out": 4, "act": "sigmoid"}
]
```

Arquitectura con cuello de botella de 2 neuronas:
- **Capa 1:** codifica de 4 a 2 dimensiones con ReLU
- **Capa 2:** decodifica de 2 a 4 dimensiones con sigmoide

```mice
var modelo = dl.perceptron_multicapa(arq)
dl.entrenar_red(modelo, X, X, 3000, 0.1)
```

Note que `Y = X`: el objetivo de entrenamiento es la misma entrada. Esto es lo que define a un autoencoder.

```mice
var test = dl.forward(modelo, [[1, 0, 0, 1]])
imp "Entrada: [1, 0, 0, 1]"
imp "Reconstruccion:"
imp test["salida"][0]
```

Prueba con un patron que no estaba en los datos de entrenamiento. Si el patron se reconstruye bien, significa que es similar a los datos de entrenamiento. Si se reconstruye mal, es potencialmente anomalo.

```mice
imp "Codigo latente (2 neuronas):"
imp test["activaciones"][1]
```

Muestra la representacion interna del patron en el cuello de botella (activacion de la capa 1, que es el indice 1 en la lista de activaciones porque el indice 0 es la entrada).

---

## 10. Ejemplo 4: Clasificador Iris (softmax)

### 10.1 El problema

Clasificar flores Iris en 3 especies segun 2 caracteristicas. Es clasificacion **multiclase**: exactamente una especie debe ser seleccionada.

```mice
importar "dl.mice" como dl

var X = [
    [1.0, 2.0], [2.0, 1.0],   # clase 0
    [3.0, 3.0], [4.0, 2.0],   # clase 1
    [5.0, 5.0], [6.0, 4.0]    # clase 2
]

var Y = [
    [1, 0, 0], [1, 0, 0],
    [0, 1, 0], [0, 1, 0],
    [0, 0, 1], [0, 0, 1]
]
```

Codificacion one-hot: 3 clases, cada una representada por un vector con un 1 en su posicion.

```mice
var arq = [
    {"in": 2, "out": 5, "act": "relu"},
    {"in": 5, "out": 3, "act": "softmax"}
]
```

Arquitectura: 2 caracteristicas de entrada, 5 neuronas ocultas con ReLU, 3 salidas con softmax.

Se usa softmax porque las clases son mutuamente excluyentes. La salida es una distribucion de probabilidad sobre las 3 clases.

```mice
var modelo = dl.perceptron_multicapa(arq)
dl.entrenar_red(modelo, X, Y, 2000, 0.05)

var prueba = dl.forward(modelo, [[2.5, 1.5]])
imp prueba["salida"][0]

var clase = 0
si (prueba["salida"][0][1] > prueba["salida"][0][clase]) { clase = 1 }
si (prueba["salida"][0][2] > prueba["salida"][0][clase]) { clase = 2 }
imp "Clase predicha: " + aTexto(clase)
```

La clase predicha es la neurona de salida con el valor mas alto.

---

## 11. Matematicas subyacentes

### 11.1 Forward propagation

Para una red con L capas, la capa l calcula:

```
Z[l] = A[l-1] * W[l] + b[l]
A[l] = g[l](Z[l])
```

Donde:
- `A[0] = X` (la entrada)
- `W[l]` es la matriz de pesos de la capa l
- `b[l]` es el vector de sesgos de la capa l
- `g[l]` es la funcion de activacion de la capa l
- `A[L]` es la salida final (prediccion)

### 11.2 Backpropagation

Para MSE loss, el error en la capa de salida es:

```
delta[L] = A[L] - Y
```

Para cada capa l desde L-1 hasta 1:

```
delta[l] = (delta[l+1] * W[l+1]^T) ⊙ g[l]'(Z[l])
```

Los gradientes son:

```
dW[l] = A[l-1]^T * delta[l]
db[l] = sum(delta[l], axis=0)
```

La actualizacion:

```
W[l] = W[l] - lr * dW[l]
b[l] = b[l] - lr * db[l]
```

### 11.3 Derivadas de activacion

| Activacion | g(x) | g'(x) |
|-----------|------|-------|
| Sigmoide | 1/(1+e^(-x)) | g(x) * (1-g(x)) |
| ReLU | max(0, x) | 1 si x > 0, 0 si x <= 0 |

### 11.4 Inicializacion Xavier

```
W ~ U(-sqrt(6/(n_in + n_out)), +sqrt(6/(n_in + n_out)))
```

### 11.5 Exponencial (serie de Taylor)

```
e^x = sum_{n=0}^{10} x^n / n!
```

Error relativo para x en [-2, 2]: < 1e-8. Para valores fuera de este rango, la precision disminuye pero es suficiente para entrenamiento de redes.

### 11.6 Raiz cuadrada (Newton-Raphson)

```
x_{n+1} = 0.5 * (x_n + S / x_n)
```

Convergencia cuadratica en ~30 iteraciones.

### 11.7 Generador aleatorio (LCG)

```
semilla = (semilla * 1103515245 + 12345) % 2^31
aleatorio = semilla / 2^31
```

Algoritmo congruencial lineal (estandar POSIX).

---

## 12. Arquitectura interna y conexion con Python

### 12.1 Cadena de ejecucion

Cuando se ejecuta `dl.forward(modelo, X)` en MICELIO:

```
1. dl.mice llama a mat.multiplicar(A_prev, W)
2. matriz.mice ejecuta triple bucle anidado en MICELIO puro
3. Cada multiplicacion escalar a*b es interpretada por el Visitor
4. Si ambos operandos son listas anidadas, el Visitor llama a matrix_mul() en Python
5. matrix_mul ejecuta el algoritmo O(n^3) en Python puro
```

Cuando se ejecuta `sigmoid(Z)`:

```
1. dl.mice llama a aplicar(m, sigmoid_esc)
2. aplicar itera sobre cada elemento y llama sigmoid_esc(x)
3. sigmoid_esc(x) = 1 / (1 + exp(-x))
4. exp() resuelve a builtins.mice → serie de Taylor (10 terminos)
5. Cada termino de Taylor: multiplicacion y division en MICELIO puro
```

### 12.2 Funciones implementadas en MICELIO puro

| Funcion | Implementacion |
|---------|---------------|
| `exp(x)` | Serie de Taylor, 10 terminos |
| `aleatorio()` | LCG, modulo 2^31 |
| `ordenar(lista)` | Quicksort |
| `raiz(x)` | Newton-Raphson (math.mice) |
| `mat.multiplicar(A, B)` | Triple bucle O(n^3) |
| `sigmoid`, `relu`, `softmax` | Operaciones elemento a elemento |

### 12.3 Funciones que permanecen en Python

Las siguientes operaciones requieren acceso al sistema operativo y no pueden implementarse en MICELIO puro:

- Archivos: `__archivo_leer`, `__archivo_escribir`, etc.
- Graficos: `__grafico_set_pixel`, `__grafico_guardar`
- GUI: `__gui_alert`, `__gui_confirm`, etc.
- Web: `__hifa_*` (servidor HTTP)
- Type introspection: `__tipo_nativo`, `__a_numero`, `__a_texto`

---

## 13. Limitaciones actuales

### 13.1 Algoritmicas

- **Full-batch:** El entrenamiento procesa todos los datos en cada epoca. No hay soporte nativo para mini-batches, aunque pueden implementarse manualmente llamando a `entrenar_red` con `epochs=1` por cada lote.
- **SGD sin momentum:** Solo se usa el gradiente inmediato. No hay termino de momentum ni optimizadores como Adam o RMSProp.
- **Sin regularizacion:** No hay dropout, weight decay ni batch normalization. Redes grandes pueden sobreajustarse.
- **MSE como unica funcion de perdida:** No hay cross-entropy implementada en el ciclo de entrenamiento.
- **Learning rate fijo:** No hay schedulers ni adaptacion automatica.

### 13.2 De rendimiento

- **Multiplicacion matricial O(n^3):** Sin optimizaciones como Strassen o BLAS. Adecuado para redes pequenas (menos de 100 neuronas por capa).
- **Taylor series en exp():** 10 terminos por llamada. Para entrenamientos largos (5000+ epocas) el tiempo de ejecucion es significativamente mayor que con la implementacion nativa de Python.

### 13.3 Mitigaciones

- Para conjuntos de datos grandes, puede particionarse el entrenamiento en lotes manualmente
- Para problemas simples, 200-1000 epocas suelen ser suficientes
- Las redes pequenas (2-3 capas, <10 neuronas por capa) entrenan en tiempos aceptables
