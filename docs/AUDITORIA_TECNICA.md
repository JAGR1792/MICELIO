# 🔍 AUDITORÍA TÉCNICA: MICELIO

**Estado: 11 Mayo 2026 | 5 ✅ | 2 ⚠️ | 1 ❌**

Qué está HECHO, PARCIAL y FALTA con nombres exactos de algoritmos.

---

## 📊 RESUMEN EJECUTIVO

| Fase | Estado | Bloqueador |
|:---|:---:|---:|
| **0-1** Fundamentos | ✅ | — |
| **2** Matemáticas | ✅ | — |
| **3** Matrices | ⚠️ | Gauss-Jordan, Determinante |
| **4** Control Flujo | ✅ | — |
| **5** Gráficas/I/O | ✅ | — |
| **6** ML Básico | ⚠️ | Sigmoid, Logística, GD |
| **7** Deep Learning | ❌ | TODO |

---

## ✅ FASE 0-1: FUNDAMENTOS Y CALCULADORA

**Implementado:**
- ✔️ Lexer/Parser ANTLR con Micelio.g4
- ✔️ Visitor pattern (eval_visitor.py)
- ✔️ Operaciones aritméticas: +, -, *, /, %, ^
- ✔️ Precedencia de operadores y paréntesis
- ✔️ Variables y tabla de símbolos (Environment)
- ✔️ Control de flujo: si/sino, mientras, para
- ✔️ Funciones de usuario, recursión, scopes
- ✔️ REPL interactivo con variable `_`

---

## FASE 2: MATEMÁTICAS CIENTÍFICAS

### ✅ HECHO
**Trigonométricas (Serie de Taylor):**
- sin(x), cos(x), tan(x)
- arcsin(x), arccos(x), arctan(x)

**Exponenciales y logarítmicas:**
- exp(x) (serie de Taylor)
- log(x) (serie de atanh)
- log10(x)

**Raíces y potencias:**
- sqrt(x) (Newton-Raphson)
- pow(x, y), potencia_entera()

**Utilidades:**
- abs(x), factorial(n)
- piso(), techo(), redondear()
- Constantes: PI, E

### ⚠️ PARCIAL
- Series de Taylor limitadas a 30 iteraciones (pueden mejorar precisión)

### ❌ FALTA
- Nada crítico

---

## FASE 3: MATRICES Y ÁLGEBRA LINEAL

### ✅ HECHO
**Constructores:**
- ceros(filas, columnas)
- unos(filas, columnas)
- identidad(n)

**Operaciones:**
- suma_matrices(a, b)
- resta_matrices(a, b)
- multiplicar(a, b) - producto de matrices
- escalar(matriz, valor) - multiplicación por escalar

**Transformaciones:**
- transpuesta(matriz)
- aplanar(matriz)

**Utilidades:**
- filas(matriz), columnas(matriz), dimensiones(matriz)
- traza(matriz)
- norma_frobenius(matriz)
- fila(matriz, i), columna(matriz, j)
- copia(matriz) - copia profunda
- es_matriz_valida(m)

### ⚠️ PARCIAL
- Multiplicación matricial existe pero validación de dimensiones es básica
- No hay integración completa con sintaxis del lenguaje

### ❌ FALTA ⚠️⚠️⚠️ CRÍTICO PARA ML
1. **Gauss-Jordan** - elimación de Gauss-Jordan para inversa
2. **Determinante** - expansión de cofactores o triangulación
3. **Inversa de matriz** - matrix.inverse() o inversa()

**Por qué importa:** La regresión lineal por mínimos cuadrados necesita β = (X^T X)^(-1) X^T y

---

## FASE 4: CONTROL DE FLUJO

### ✅ HECHO
- Condicionales: si, sino, sino_si
- Comparación: >, <, >=, <=, ==, !=
- Lógica: y, o, no
- Ciclos: mientras, para, para...en
- Control: romper, continuar

### ⚠️ PARCIAL
- Nada crítico

### ❌ FALTA
- Nada urgente

---

## FASE 5: GRÁFICAS Y ARCHIVOS

### ✅ HECHO
**Módulo archivo.mice:**
- leer(ruta)
- escribir(ruta, contenido)
- leer_lineas(ruta), escribir_lineas(ruta, lineas)
- anexar(ruta, contenido)
- existe(ruta), eliminar(ruta), tamaño(ruta)
- leer_csv(ruta, delim), escribir_csv(ruta, datos, delim)

**Módulo grafico.mice:**
- lineas(x, ys) - gráfica de línea
- dispersion(x, ys) - scatter plot
- histograma(datos, bins)
- titulo(texto), etiquetas(xlabel, ylabel)
- guardar(path), mostrar()
- Rendering: PPM pixel-by-pixel
- Ejes, grid, etiquetas

### ⚠️ PARCIAL
- Formato limitado a PPM (por diseño, no es debilidad)
- Escalas y normalización son básicas

### ❌ FALTA
- Curvas suaves (splines, Bezier) - opcional
- Exportación a otros formatos - opcional

---

## FASE 6: MACHINE LEARNING BÁSICO

### ✅ HECHO
**Utilidades:**
- dividir_datos(X, Y, prop) - train-test split
- media(valores)
- varianza(valores)
- desviacion_estandar(valores)
- normalizar(valores) - z-score normalization

**Algoritmos:**
- regresion_lineal(X, Y) - **SÓ**LO PARA 1D (pendiente + intercepción)
- predecir_lineal(x, modelo)
- k_means(X, k, iteraciones) - clustering básico
- distancia_euclidiana(p1, p2) - scalar y vectorial

**Métricas:**
- exactitud(predichos, reales)
- precision(predichos, reales)
- recall(predichos, reales)
- f1_score(predichos, reales)
- matriz_confusion(predichos, reales)

### ⚠️ PARCIAL
- Regresión lineal es **SÓ**LO 1D, falta forma matricial: β = (X^T X)^(-1) X^T y
- k_means no recalcula centroides correctamente (solo itera)
- Métricas asumen binario (0 y 1), no multivaluado

### ❌ FALTA ⚠️⚠️⚠️ CRÍTICO PARA CERRAR ML

1. **Regresión lineal matricial** - necesita **Gauss-Jordan**
   - Formula: β = (X^T X)^(-1) X^T y
   - Necesita: inversa de matriz

2. **Regresión logística binaria** - tres piezas juntas:
   - **Sigmoid**: σ(z) = 1 / (1 + e^(-z))
   - **Log Loss (Binary Cross-Entropy)**: -[y·log(ŷ) + (1-y)·log(1-ŷ)]
   - **Gradient descent**: w_new = w - α·∇L

3. **Descenso de gradiente** - loop de optimización
   - Learning rate α
   - Actualización iterativa de parámetros
   - Criterio de parada (epochs, convergencia)

4. **Clasificación probabilística**
   - Predicción como probabilidad [0,1]
   - Umbral de decisión configurable (no solo 0.5)

5. **Normalización por característica** - feature normalization
   - Diferente de normalización global
   - Necesaria para convergencia de gradient descent

---

## FASE 7: DEEP LEARNING

### ✅ HECHO
- **Nada del core de redes neuronales existe aún**

### ⚠️ PARCIAL
- Nada

### ❌ FALTA ⚠️⚠️⚠️ CRÍTICO PARA REDES NEURONALES

**Activaciones (necesitan derivada también):**
1. **Sigmoid**: σ(z) = 1 / (1 + e^(-z)), σ'(z) = σ(z)·(1-σ(z))
2. **Tanh**: tanh(z), tanh'(z) = 1 - tanh²(z)
3. **ReLU**: max(0, z), derivada = 1 si z>0 else 0
4. **Softmax**: e^z / Σ(e^z) para multiclase, jacobiano

**Funciones de pérdida:**
1. **MSE (Mean Squared Error)**: Σ((y - ŷ)²) / n
2. **Binary Cross-Entropy**: -[y·log(ŷ) + (1-y)·log(1-ŷ)]
3. **Categorical Cross-Entropy**: -Σ(y·log(ŷ))

**Inicialización de pesos:**
1. **Aleatoria**: N(0, 1)
2. **Xavier/Glorot**: N(0, √(1/(n_in + n_out)))
3. **He Initialization**: N(0, √(2/n_in))

**Arquitectura de red:**
1. **Clase Layer** - capas densas
   - Atributos: pesos W, bias b, tamaños entrada/salida
   - forward(x): z = Wx + b; a = activation(z)
   - backward(δ): calcular gradientes

2. **Clase NeuralNetwork** - contenedor de capas
   - Lista de capas
   - forward(x): pasar por todas las capas
   - backward(loss_gradient): propagar error atrás

3. **Forward propagation** - paso adelante completo
   - Para cada capa: z = Wx + b; a = act(z)
   - Guardar activaciones para backprop

4. **Backpropagation** - retropropagación del error
   - δ_L = ∇_a L ⊙ a'(z_L)
   - δ_l = (W_l+1^T δ_l+1) ⊙ a'(z_l)
   - ∇_W = δ a^T, ∇_b = δ

5. **Mini-batch gradient descent**
   - Dividir datos en lotes
   - Actualizar W, b por lote
   - W ← W - α·∇_W, b ← b - α·∇_b

6. **One-hot encoding** para multiclase
   - Convertir clase a vector [0,0,1,0]

**Arquitecturas específicas:**
1. **Perceptrón multicapa (MLP)** configurable
   - Constructor: layers([input_size, hidden1, hidden2, output_size])
   - Entrenable con cualquier activación

2. **Autoencoder** para agrupamiento
   - Encoder + Decoder
   - Pérdida de reconstrucción

3. **Red para series temporales** (opcional)
   - Ventanas deslizantes
   - Predicción paso a paso

---

## RESUMEN EJECUTIVO: BLOQUEADORES

### INMEDIATOS (Para ML básico)
| Prioridad | Algoritmo | Por qué | Impacto |
|-----------|-----------|--------|--------|
| 🔴 CRÍTICA | Gauss-Jordan | Calcula inversa de matrices | Regresión lineal matricial |
| 🔴 CRÍTICA | Determinante | Valida invertibilidad | ML robusto |
| 🔴 CRÍTICA | Regresión lineal matricial | Forma correcta con X^T | ML base |
| 🔴 CRÍTICA | Regresión logística + sigmoide | Clasificación binaria | ML base |
| 🔴 CRÍTICA | Gradient descent | Loop de optimización | ML funcional |

### PARA DEEP LEARNING
| Prioridad | Componente | Necesidad | Orden |
|-----------|-----------|----------|-------|
| 1️⃣ | Sigmoid + derivada | Base de activación | Primero |
| 2️⃣ | MSE + Binary CE | Pérdidas | Segundo |
| 3️⃣ | ReLU + Tanh + derivadas | Activaciones | Tercero |
| 4️⃣ | Backpropagation | Aprendizaje | Cuarto |
| 5️⃣ | Clase Layer | Estructura | Quinto |
| 6️⃣ | Clase NeuralNetwork | Contenedor | Sexto |
| 7️⃣ | Inicialización (Xavier, He) | Convergencia | Séptimo |
| 8️⃣ | Softmax + Categorical CE | Multiclase | Octavo |

---

## ORDEN RECOMENDADO DE IMPLEMENTACIÓN

```
1. Gauss-Jordan (matriz.mice)
   └─ Permite: regresión lineal matricial

2. Determinante (matriz.mice)
   └─ Permite: validación de estabilidad

3. Regresión lineal matricial (ml.mice)
   └─ Requiere: Gauss-Jordan
   └─ Permite: ML base funcional

4. Regresión logística binaria (ml.mice)
   ├─ Sigmoid + log loss
   ├─ Gradient descent
   └─ Permite: clasificación probabilística

5. Activaciones + derivadas (ml.mice o nucleo/runtime.py)
   ├─ Sigmoid, Tanh, ReLU, Softmax
   └─ Permite: redes neuronales entrenable

6. Funciones de pérdida (ml.mice o runtime.py)
   ├─ MSE, Binary CE, Categorical CE
   └─ Permite: entrenamiento multiclase

7. Backpropagation (ml.mice o nueva clase)
   └─ Permite: aprendizaje real

8. Capas (Layer class - nueva)
   └─ Permite: arquitecturas flexibles

9. Red neuronal (NeuralNetwork class - nueva)
   ├─ Forward + Backward
   ├─ Mini-batch training
   └─ Permite: modelos funcionles

10. Inicialización + Optimización avanzada
    └─ Permite: convergencia eficiente
```

---

## NOTAS TÉCNICAS

- **En Python puro**: Sin NumPy, SciPy, TensorFlow
- **Precisión numérica**: Series de Taylor con 30 iteraciones es razonable
- **Performance**: El intérprete es lento por diseño; está optimizado en hot-paths (ver docs/auditoria-rendimiento.md)
- **Estabilidad**: Gauss-Jordan con pivoteo es recomendado
- **Convergencia**: Learning rate adaptativo ayuda pero no es obligatorio

