# JORGESCRIPT

# 📘 Proyecto DSL para Deep Learning

> **📌 CONCEPTO CLAVE:** Vas a crear un lenguaje de programación completo desde cero usando ANTLR. No es solo hacer Deep Learning, es **inventar un lenguaje que permita hacer Deep Learning**
> 

<aside>
💪

**RETO EXTREMO:** Todo el proyecto se implementa SIN librerías externas. Tú implementas las matemáticas, las matrices, los algoritmos de ML y las redes neuronales desde cero. Solo Python básico y ANTLR. 

7 PALABRAS 

E S E N C I A

</aside>

Finalmente tenemos un Repo para el proyectito.

---

## 🎯 Requisitos Oficiales del Proyecto

El lenguaje debe ser capaz de:
### Operaciones Básicas

✅ Operaciones aritméticas completas (suma, resta, multiplicación, división, módulo, potencias x^y, trigonometría)

✅ Operaciones de matrices (suma, resta, multiplicación, inversa, transpuesta)

✅ Condicionales y ciclos (for y while)

✅ Gráficas de datos

✅ Manejo de archivos (lectura y escritura de texto)

### Funcionalidades de Deep Learning

✅ Regresión lineal y regresión logística

✅ Clasificador usando perceptrón multicapa

✅ Algoritmos con redes neuronales artificiales para agrupamiento, clasificación y predicción

### Requisitos Técnicos

✅ Enfoque funcional

✅ Implementación en Python usando patrón Visitor de ANTLR

✅ Ejecución por consola, interfaz de texto o plugin

✅ **Todo implementado desde cero (sin librerías externas)**

---

## 🔍 AUDITORÍA TÉCNICA REAL

**Ver documento completo:** [docs/AUDITORIA_TECNICA.md](docs/AUDITORIA_TECNICA.md)

Este es el estado exacto del proyecto: qué está HECHO, PARCIAL y FALTA en cada fase, con nombres técnicos de algoritmos para no buscar.

**Resumen ejecutivo:** Falta completar matrices (Gauss-Jordan, determinante) y ML (regresión logística, gradient descent, deep learning completo).

---

## Prioridad técnica real

Esta sección ordena la implementación por dependencia técnica, no por entusiasmo. La idea es cerrar primero lo que hace posible lo demás.

### 1. Algebra lineal base

Falta completar esto primero porque casi todo ML/DL depende de ello.

- [ ]  Implementar una clase `Matrix` en Python puro.
- [ ]  Definir constructor claro desde listas y validación de dimensiones.
- [ ]  Soportar acceso y actualización con `matrix[i][j]`.
- [ ]  Agregar suma, resta, multiplicación y transpuesta como operaciones formales.
- [ ]  Implementar inversa con Gauss-Jordan.
- [ ]  Implementar determinante.
- [ ]  Definir errores de dimensiones incompatibles con mensajes pedagógicos.

Porque importa:

- La regresión lineal matricial usa `X^T X` e inversa.
- La regresión logistica usa gradientes sobre vectores y matrices.
- Las redes neuronales usan multiplicaciones matriciales en forward y backpropagation.

### 2. Orden minimo para Machine Learning

Antes de meter algoritmos más grandes, hace falta una base de trabajo consistente.

- [ ]  Normalización de datos.
- [ ]  Train-test split reproducible.
- [ ]  Manejo de vectores y matrices de entrada.
- [ ]  Métricas comunes: MSE, accuracy, precision, recall, R2.
- [ ]  Función de pérdida para regresión y clasificación.

Porque importa:

- Sin normalización, muchos algoritmos convergen mal o lento.
- Sin partición train-test, no hay forma seria de medir si un modelo generaliza.
- Sin métricas, no se puede comparar modelos ni saber si una mejora es real.

### 3. Algoritmos de ML que sí son necesarios

- [ ]  Regresión lineal en forma matricial.
- [ ]  Regresión lineal por descenso de gradiente.
- [ ]  Regresión logística binaria.
- [ ]  Función sigmoide y log loss.
- [ ]  Descenso de gradiente con tasa de aprendizaje.
- [ ]  Clasificación básica con umbral y probabilidad.
- [ ]  K-means como opción de agrupamiento.

### Algoritmos que faltan y son más graves

Estos son los huecos que más frenan el proyecto si queremos que ML/DL tenga sentido técnico.

1. **Matrix completa en Python puro**
    - Falta porque casi todo ML/DL depende de multiplicación, transpuesta e inversa.
    - Más tarde sirve para regresión lineal matricial, gradientes y backpropagation.

2. **Gauss-Jordan para inversa**
    - Falta porque la regresión lineal por mínimos cuadrados la necesita.
    - Más tarde sirve para resolver sistemas lineales y verificar estabilidad numérica.

3. **Determinante**
    - Falta porque ayuda a validar invertibilidad y a entender el comportamiento de matrices cuadradas.
    - Más tarde sirve para filtros matemáticos y control de singularidad.

4. **Normalización y train-test split**
    - Falta porque sin eso los modelos se entrenan y evalúan mal.
    - Más tarde sirve para comparar modelos de forma seria y reproducible.

5. **Regresión lineal matricial**
    - Falta porque es la primera puerta real al ML con álgebra lineal.
    - Más tarde sirve como base conceptual para descenso de gradiente y modelos más complejos.

6. **Regresión logística binaria**
    - Falta porque introduce clasificación probabilística y función sigmoide.
    - Más tarde sirve para clasificar, medir accuracy y preparar softmax.

7. **Funciones de activación y sus derivadas**
    - Falta porque sin ellas no existe red neuronal entrenable.
    - Más tarde sirven para capas densas, clasificación y control de gradientes.

8. **Backpropagation**
    - Falta porque es el núcleo del aprendizaje en redes neuronales.
    - Más tarde sirve para MLP, autoencoders y cualquier red entrenable.

9. **Softmax + one-hot + categorical cross-entropy**
    - Falta porque sin esto no hay clasificación multiclase seria.
    - Más tarde sirve para salida de redes de clasificación y evaluación multi-clase.

10. **Inicialización de pesos**
    - Falta porque afecta estabilidad y velocidad de aprendizaje.
    - Más tarde sirve para evitar redes estancadas o gradientes pobres.

11. **K-means**
    - Falta menos grave que lo anterior, pero es útil como primer clustering.
    - Más tarde sirve para agrupamiento y como comparación con autoencoders.

Porque importa:

- Regresión lineal y logística son la base del ML clásico.
- K-means sirve como primer algoritmo de clustering antes de redes más complejas.
- El descenso de gradiente es la columna vertebral del aprendizaje automático moderno.

### 4. Deep Learning realista

No conviene empezar por la red completa; primero faltan los bloques que la hacen posible.

- [ ]  Activaciones: sigmoid, tanh, ReLU, softmax.
- [ ]  Derivadas de activación.
- [ ]  Funciones de pérdida: MSE, binary cross-entropy, categorical cross-entropy.
- [ ]  Inicialización de pesos: aleatoria, Xavier/Glorot, He.
- [ ]  Clase `Layer`.
- [ ]  Clase `NeuralNetwork`.
- [ ]  Forward propagation.
- [ ]  Backpropagation.
- [ ]  Mini-batch gradient descent.
- [ ]  Guardado y carga de modelos.

Porque importa:

- Sin activaciones y sus derivadas no hay retropropagación correcta.
- Sin inicialización decente la red aprende mal o se estanca.
- Sin layers y una red formal solo hay funciones sueltas, no un framework real.

### 5. Empaquetado y entrega

- [ ]  Binario standalone por plataforma.
- [ ]  Distribución Linux, Windows y macOS.
- [ ]  Flujo de release consistente con versionado.
- [ ]  Documentación de instalación final.

Porque importa:

- Sin esto el proyecto funciona solo para quien lo ejecuta en el repo.
- El valor real sube cuando otro puede instalarlo y probarlo sin fricción.

---

## 🗺️ Roadmap Completo (Desde Cero)

<aside>
🎓

**IMPORTANTE:** Este plan asume que NUNCA has usado ANTLR. Cada fase está diseñada para aprender haciendo. Y además, vas a implementar TODO desde cero.

</aside>

---

## 📚 FASE 0: Fundamentos (Semana 1)

### Conceptos Básicos

- [x]  ¿Qué es un analizador sintáctico? (lee texto y verifica si sigue reglas)
- [x]  ¿Qué es ANTLR? (genera analizadores sintácticos automáticamente)
- [x]  ¿Qué es una gramática? (archivo .g4 con reglas de tu lenguaje)
- [x]  ¿Qué es el patrón Visitor? (recorre el árbol de análisis)
- [x]  ¿Qué es un DSL? (lenguaje para un dominio específico)

### Instalación Mínima

- [x]  Instalar ANTLR4
- [x]  Instalar Java (ANTLR lo necesita)
- [x]  Instalar runtime de ANTLR para Python: `pip install antlr4-python3-runtime`
- [x]  Probar que ANTLR funciona con ejemplo Hello World

<aside>
⚠️

**IMPORTANTE:** Solo instalas ANTLR. Todo lo demás (matemáticas, matrices, ML, gráficas) lo implementas TÚ desde cero.

</aside>

---

## 🧪 FASE 1: Tu Primera Gramática (Semana 1-2)

### Proyecto Mini 1: Calculadora Básica

**Objetivo:** Crear un lenguaje que solo sume y reste números

- [x]  Escribir ejemplos: `3 + 5`, `10 - 2`, `7 + 3 - 1`
- [x]  Crear archivo `MiniCalc.g4`
- [x]  Definir qué es un número en la gramática
- [x]  Definir qué es una suma y una resta
- [x]  Generar analizador: `antlr4 -Dlanguage=Python3 MiniCalc.g4`
- [x]  Probar con `grun` que reconoce expresiones
- [x]  Ver el árbol de análisis visual

**Entregable:** Programa que reconoce sumas y restas

### Proyecto Mini 2: Calculadora que Ejecuta

- [x]  Generar el Visitor desde la gramática
- [x]  Crear tu clase Visitor en Python
- [x]  Implementar método que visita números
- [x]  Implementar método que visita sumas
- [x]  Implementar método que visita restas
- [x]  Crear script que lee una expresión y muestra resultado

**Entregable:** Programa que calcula `3 + 5` y da `8`

<aside>
🎉

**MILESTONE 1:** ¡Ya tienes un lenguaje de programación funcional!

</aside>

---

## 🔧 FASE 2: Matemáticas (Semana 2-3)

### Operaciones Aritméticas

- [x]  Agregar multiplicación, división, módulo a la gramática
- [x]  Agregar potencias (x^y)
- [x]  Implementar precedencia de operadores
- [x]  Agregar paréntesis
- [x]  Actualizar Visitor para cada operación
- [x]  Probar: `(3 + 5) * 2^3`

### Implementar Funciones Matemáticas Desde Cero

- [x]  **Trigonometría (serie de Taylor):**
    - [x]  `sin(x)` - implementar serie de Taylor
    - [x]  `cos(x)` - implementar serie de Taylor
    - [x]  `tan(x)` - calcular como sin/cos
- [x]  **Raíces y potencias:**
    - [x]  `sqrt(x)` - método de Newton-Raphson
    - [x]  `pow(x, y)` - exponenciación rápida
- [x]  **Otras funciones:**
    - [x]  `abs(x)`, `log(x)`, `exp(x)` - implementar con series
- [x]  Definir en gramática e implementar en Visitor

### Variables

- [x]  Permitir declarar: `x = 5`
- [x]  Permitir usar: `x + 3`
- [x]  Crear tabla de símbolos
- [x]  Implementar en Visitor

**Entregable:** Calculadora científica completa (todo desde cero)

---

## 🔲 FASE 3: Matrices (Semana 3-4)

### Prioridad técnica de esta fase

Esta fase no es solo "hacer matrices". Es cerrar el bloque matemático que más tarde va a sostener regresión, optimización y redes neuronales.

### Implementar Clase Matrix Desde Cero

- [ ]  Crear clase `Matrix` en Python puro
- [ ]  Constructor desde listas
- [ ]  Acceso a elementos `matrix[i][j]`
- [ ]  Métodos para obtener dimensiones

### Sintaxis en el Lenguaje

- [ ]  Decidir sintaxis: `A = [[1, 2], [3, 4]]`
- [ ]  Agregar a la gramática

### Operaciones Matriciales Desde Cero

- [ ]  Suma (elemento por elemento)
- [ ]  Resta (elemento por elemento)
- [ ]  Multiplicación (algoritmo matricial)
- [ ]  Transpuesta (intercambio filas/columnas)
- [ ]  Inversa (Gauss-Jordan)
- [ ]  Determinante (expansión de cofactores o eliminacion triangular)
- [ ]  Validación de dimensiones y manejo de errores

### Orden sugerido de implementación

1. `Matrix` y validaciones.
2. Suma, resta y transpuesta.
3. Multiplicación matricial.
4. Determinante.
5. Inversa.
6. Pruebas con ejemplos pequeños y verificables.

### Por qué esta fase es clave

- La regresión lineal matricial usa multiplicación, transpuesta e inversa.
- La regresión logística necesita una base de matrices estable para el descenso de gradiente.
- Las redes neuronales requieren multiplicaciones repetidas de matrices en forward y backpropagation.

**Entregable:** Sistema de álgebra lineal desde cero

---

## 🔀 FASE 4: Control de Flujo (Semana 4-5)

### Condicionales

- [ ]  Definir sintaxis if/else
- [ ]  Operadores de comparación: `>`, `<`, `>=`, `<=`, `==`, `!=`
- [ ]  Operadores lógicos: `and`, `or`, `not`
- [ ]  Implementar en Visitor

### Ciclos

- [ ]  Definir sintaxis `for`
- [ ]  Definir sintaxis `while`
- [ ]  Implementar en Visitor

**Entregable:** Lenguaje con estructuras de control

---

## 📊 FASE 5: Gráficas y Archivos (Semana 5-6)

### Sistema de Gráficas Desde Cero

<aside>
🎨

**OPCIONES:** Generar archivos SVG (XML), HTML con Canvas, o gráficas ASCII en consola (más simple).

</aside>

- [ ]  Decidir formato (SVG/HTML/ASCII)
- [ ]  Implementar gráfica de línea: `plot(x, y)`
- [ ]  Implementar dispersión: `scatter(x, y)`
- [ ]  Implementar histograma: `histogram(datos)`
- [ ]  Funciones: calcular escalas, normalizar, dibujar ejes

### Archivos

- [ ]  Sintaxis lectura: `datos = read_file("data.txt")`
- [ ]  Sintaxis escritura: `write_file("output.txt", contenido)`
- [ ]  Parseo de CSV/TXT
- [ ]  Implementar en Visitor

**Entregable:** Visualización e I/O desde cero

---

## FASE 6: Machine Learning Básico (Semana 6-7)

### Lo que realmente falta antes de llamar esto "ML listo"

- [ ]  Normalización de datos.
- [ ]  Separación train-test.
- [ ]  Representación consistente de vectores y matrices.
- [ ]  Métricas comparables entre modelos.

### Algoritmos prioritarios

### Regresión Lineal Desde Cero

- [ ]  Implementar mínimos cuadrados: β = (X^T X)^(-1) X^T y
- [ ]  Implementar regresión lineal por descenso de gradiente
- [ ]  Función de predicción
- [ ]  Definir sintaxis: `modelo = linear_regression(X, y)`
- [ ]  Métricas: MSE, R²

### Regresión Logística Desde Cero

- [ ]  Función sigmoide: σ(z) = 1 / (1 + e^(-z))
- [ ]  Función de costo (log loss)
- [ ]  Gradient descent
- [ ]  Función de predicción
- [ ]  Métricas: accuracy, precision, recall
- [ ]  Umbral de clasificación configurable

### Algoritmos que conviene priorizar aquí

1. Regresión lineal matricial.
2. Regresión lineal por descenso de gradiente.
3. Regresión logística binaria.
4. K-means como base de clustering.

### Por qué esto va antes que redes neuronales

- Obliga a tener matrices, funciones de pérdida y optimización bien resueltas.
- Da métricas para validar si el runtime matemático funciona de verdad.
- Sirve como puente didáctico hacia deep learning.

**Entregable:** Algoritmos de regresión desde cero

---

## 🧠 FASE 7: Deep Learning (Semana 7-9)

<aside>
🔥

**RETO MÁXIMO:** Redes neuronales desde cero. Solo MICELIO puro y matemáticas.

</aside>

### Componentes Base

- [ ]  **Funciones de activación y derivadas:**
    - [ ]  Sigmoid, Tanh, ReLU, Softmax
- [ ]  **Funciones de pérdida:**
    - [ ]  MSE, Binary Cross-Entropy, Categorical Cross-Entropy
- [ ]  **Inicialización de pesos:**
    - [ ]  Aleatoria, Xavier/Glorot, He

### Orden de trabajo recomendado

1. Activaciones y derivadas.
2. Funciones de pérdida.
3. Inicialización de pesos.
4. Clase `Layer`.
5. Clase `NeuralNetwork`.
6. Forward propagation.
7. Backpropagation.
8. Mini-batch y ajuste de pesos.

### Algoritmos que faltan y son realmente necesarios

- [ ]  Capa densa totalmente funcional.
- [ ]  Backpropagation con gradientes correctos.
- [ ]  Clasificación multiclase con softmax y one-hot.
- [ ]  Red para predicción de secuencias simples.
- [ ]  Autoencoder o equivalente para agrupamiento/representación.

### Orden técnico recomendado para deep learning

1. Activaciones y derivadas.
2. Funciones de pérdida.
3. Inicialización de pesos.
4. Capa densa.
5. Forward propagation.
6. Backpropagation.
7. Mini-batch gradient descent.
8. Clasificación multiclase con softmax.
9. Autoencoder o red simple de predicción.

### Por qué estos algoritmos importan

- Sin backpropagation no existe aprendizaje real.
- Sin softmax y one-hot no hay clasificación multiclase seria.
- Sin una capa densa estable no hay forma de escalar a arquitecturas mayores.

### Perceptrón Multicapa

- [ ]  Clase `Layer`
- [ ]  Clase `NeuralNetwork`
- [ ]  Forward propagation
- [ ]  Backpropagation (cálculo de gradientes)
- [ ]  Gradient descent y mini-batch
- [ ]  Actualización de pesos y biases
- [ ]  Sintaxis: `red = create_mlp([input, hidden, output])`

### Algoritmos de NN

- [ ]  **Agrupamiento:** Autoencoder o K-means
- [ ]  **Clasificación:** Red multiclase con one-hot
- [ ]  **Predicción:** Series temporales con ventanas

**Entregable:** Framework de Deep Learning desde cero

---

## 🎨 FASE 8: Funciones de Usuario (Semana 9-10)

- [ ]  Definir funciones: `function calcular(x, y) { return x^2 + y^2 }`
- [ ]  Llamadas a funciones
- [ ]  Recursión
- [ ]  Scope (variables locales vs globales)
- [ ]  Stack de llamadas

**Entregable:** Lenguaje funcionalmente completo

---

## 🖥️ FASE 9: Interfaz (Semana 10-11)

### Consola REPL

- [ ]  Read-Eval-Print Loop
- [ ]  Mantener estado entre comandos
- [ ]  Comandos especiales: `:help`, `:quit`, `:vars`

### Ejecución de Archivos

- [ ]  Ejecutar `.jgs`: `python [jorgescript.py](http://jorgescript.py) programa.jgs`
- [ ]  Manejo de errores con número de línea
- [ ]  Modo debug/verbose

### UX

- [ ]  Mensajes de error claros
- [ ]  Progress bar ASCII para entrenamientos
- [ ]  Formato bonito para matrices

**Entregable:** Interfaz completa

---

## 📝 FASE 10: Documentación (Semana 11-12)

- [ ]  Manual de usuario
- [ ]  Documentar sintaxis con ejemplos
- [ ]  Guía de instalación
- [ ]  Documentar matemáticas implementadas
- [ ]  Suite de tests
- [ ]  Demos de cada funcionalidad
- [ ]  Ejemplo completo: entrenar red neuronal

**Entregable:** Proyecto completo

---

## Algoritmos a Implementar Desde Cero

### Matemáticas

- Serie de Taylor (sin, cos, exp)
- Newton-Raphson (raíces)
- Exponenciación rápida

### Álgebra Lineal

- Multiplicación de matrices
- Gauss-Jordan (inversa)
- Determinante
- Transpuesta

### Machine Learning

- Regresión lineal (mínimos cuadrados)
- Regresión logística con gradient descent
- K-means (opcional)

### Deep Learning

- Forward propagation
- Backpropagation
- Gradient descent
- Funciones de activación y derivadas
- Funciones de pérdida
- Inicialización de pesos

### Utilidades

- Normalización de datos
- One-hot encoding
- Train-test split

---

## ⏱️ Cronograma (12 Semanas)

| Semanas | Fase | Hito |
| --- | --- | --- |
| 1-2 | Fundamentos + Calculadora | Primera gramática |
| 2-3 | Matemáticas | Calculadora científica |
| 3-4 | Matrices | Álgebra lineal |
| 4-5 | Control de Flujo | If, for, while |
| 5-6 | Gráficas y Archivos | Visualización |
| 6-7 | ML Básico | Regresiones |
| 7-9 | Deep Learning | Redes neuronales |
| 9-10 | Funciones | Lenguaje completo |
| 10-11 | Interfaz | Consola |
| 11-12 | Documentación | Finalizado |

---

## 📚 Recursos

### ANTLR

- **GitHub:** [https://github.com/antlr/antlr4](https://github.com/antlr/antlr4)
- **Libro:** The Definitive ANTLR 4 Reference [https://drive.google.com/file/d/1QqbeXpcvJIF2qk_4P2M_sdQRI7B6Lr-v/view?usp=sharing](https://drive.google.com/file/d/1QqbeXpcvJIF2qk_4P2M_sdQRI7B6Lr-v/view?usp=sharing)

### Buscar

- "ANTLR4 Python Visitor tutorial"
- "ANTLR4 calculator example"
- "Taylor series implementation"
- "Backpropagation algorithm step by step"
- "Neural network from scratch Python"

---

## Próximos Pasos

### Esta Semana

1. Leer Capítulo 1 del libro de ANTLR
2. Instalar entorno (Java, ANTLR, Python)
3. Hacer tutorial Hello de ANTLR
4. Crear primer `.g4` (calculadora suma/resta)

### Siguiente Semana

1. Implementar primer Visitor
2. Lograr calculadora funcional
3. Entender flujo: gramática → ANTLR → Visitor → ejecución

<aside>
🚀

**OBJETIVO REALISTA:** primero dejar estable el núcleo matemático. Si matrices, pérdidas y gradientes quedan bien, lo demás escala con menos riesgo.

**RECUERDA:** Implementar todo desde cero te hará entender profundamente ML/DL. Es difícil, pero tendrás conocimiento real.

</aside>

[INSTALACIÓN ANTLR](https://www.notion.so/INSTALACI-N-ANTLR-2fc807d50a948019a5a3d3d056559741?pvs=21)
[Ejecutando Código](https://www.notion.so/Ejecutando-C-digo-304807d50a94809b9cbdd209c30045f1?pvs=21)

[Análisis Sintáctico Descendente (ASD) — Guía Completa de Parcial](https://www.notion.so/An-lisis-Sint-ctico-Descendente-ASD-Gu-a-Completa-de-Parcial-341807d50a9481b98f58c6d0d442f6b6?pvs=21)

[Documentacion MICELIO](https://www.notion.so/Documentacion-MICELIO-351807d50a94810facd2ffe4bfb0079a?pvs=21)