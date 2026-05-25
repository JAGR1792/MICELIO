# Documentación Completa de MICELIO

**MICELIO** es un lenguaje de programación interpretado en español, con paradigma funcional, diseñado para enseñar fundamentos de programación y evolucionar hacia ciencia de datos, machine learning y deep learning. Construido desde cero usando ANTLR4 y Python (patrón Visitor), sin librerías externas de ML/DL.

---

## Índice

1. [Instalación](#1-instalación)
2. [Uso básico](#2-uso-básico)
3. [Sintaxis del lenguaje](#3-sintaxis-del-lenguaje)
4. [Tipos de datos](#4-tipos-de-datos)
5. [Biblioteca estándar](#5-biblioteca-estándar)
6. [Ejemplos por módulo](#6-ejemplos-por-módulo)
7. [Arquitectura](#7-arquitectura)
8. [Extensiones y herramientas](#8-extensiones-y-herramientas)
9. [Desarrollo](#9-desarrollo)

---

## 1. Instalación

### Requisitos

- Python 3.10+
- `antlr4-python3-runtime` (única dependencia obligatoria)

### Instalación rápida

```bash
git clone <repo-url>
cd MICELIO

# Linux/macOS
bash instalación/setup.sh

# Windows
instalación/setup.bat
```

### Instalación manual

```bash
cd MICELIO
pip install antlr4-python3-runtime
python3 main.py          # REPL
python3 main.py archivo.mice  # ejecutar archivo
```

### Dependencias opcionales (se usan si están instaladas)

| Dependencia    | Función                          |
|----------------|----------------------------------|
| Pillow (PIL)   | Convertir PPM a PNG              |
| PyGObject (GTK)| Ventanas GUI nativas             |
| Flask          | Servidor web demo (Hifa)         |
| ImageMagick    | Fallback de conversión de imagen |
| zenity         | Diálogos GUI en Linux            |
| notify-send    | Notificaciones de sistema        |

---

## 2. Uso básico

### Ejecutar un archivo `.mice`

```bash
python3 main.py ejemplos/01_basico.mice
```

### REPL interactivo

```bash
python3 main.py
```

### Usando el wrapper

```bash
./micelio archivo.mice
./micelio  # REPL
```

---

## 3. Sintaxis del lenguaje

### Variables y constantes

```mice
var x = 10
const PI = 3.1416
var nombre = "Micelio"
var lista = [1, 2, 3]
var dicc = {"clave": "valor"}
```

### Operaciones aritméticas

```mice
var suma = 5 + 3
var resta = 10 - 4
var mult = 6 * 7
var div = 20 / 4
var modulo = 10 % 3
var potencia = 2 ^ 10
```

### Control de flujo

```mice
# if / else
si (x > 0) {
    imp "positivo"
} sino {
    imp "negativo"
}

# while
var i = 0
mientras (i < 5) {
    imp i
    i = i + 1
}

# for
para elemento en [1, 2, 3] {
    imp elemento
}

# switch
segun (x) {
    caso 1 { imp "uno" }
    caso 2 { imp "dos" }
    defecto { imp "otro" }
}
```

### Funciones

```mice
funcion suma(a, b) {
    regresa a + b
}

# Función anónima
var cuad = funcion (x) { regresa x * x }

# Args variables
funcion sumar_todos(*args) {
    var total = 0
    para n en args {
        total = total + n
    }
    regresa total
}
```

### Programación funcional

```mice
# map, filter, reduce
var datos = [1, 2, 3, 4, 5]

var duplicados = map(funcion (x) { regresa x * 2 }, datos)
var pares = filter(funcion (x) { regresa x % 2 == 0 }, datos)
var suma = reduce(funcion (acc, x) { regresa acc + x }, datos, 0)

# Pipe operator
var resultado = datos
    |> map(funcion (x) { regresa x * 2 })
    |> filter(funcion (x) { regresa x > 5 })
    |> reduce(funcion (acc, x) { regresa acc + x }, 0)

imp resultado
```

### Entrada/Salida

```mice
imp "Hola mundo"
imp 42
imp [1, 2, 3]

leer variable
leer a, b, c  # múltiple en una línea
```

### Importar módulos

```mice
importar "math.mice" como math
imp math.seno(math.PI / 2)
```

### Desempaquetado

```mice
var a, b = [10, 20]
var x, y
leer x, y
a, b = [x, y]
```

### Operadores de incremento/decremento

```mice
x++   # x = x + 1
x--   # x = x - 1
x += 5
x -= 3
```

### Asignación múltiple con lectura

```mice
leer a, b
# preprocesado a: __leer_multi("a,b")
```

---

## 4. Tipos de datos

| Tipo      | Ejemplo                    | Descripción                  |
|-----------|----------------------------|------------------------------|
| Numero    | `42`, `3.14`, `-7`         | Enteros y flotantes          |
| Texto     | `"hola"`, `'mundo'`        | Cadenas de caracteres        |
| Booleano  | `verdadero`, `falso`       | Valores lógicos              |
| Lista     | `[1, 2, 3]`                | Colección ordenada mutable   |
| Set       | `#{1, 2, 3}`               | Conjunto sin duplicados      |
| Dict      | `{"a": 1, "b": 2}`         | Mapa clave-valor             |
| Nulo      | `nulo`                     | Ausencia de valor            |
| Funcion   | `funcion (x) { regresa x }`| Función de primera clase     |

### Métodos incorporados

Todas las colecciones tienen métodos nativos:

```mice
# Listas
[1, 2, 3].longitud()     # 3
[1, 2, 3].agregar(4)     # [1, 2, 3, 4]
[3, 1, 2].ordenar()      # [1, 2, 3]

# Texto
"hola".longitud()         # 4
"a,b,c".separar(",")      # ["a", "b", "c"]

# Dict
{"a": 1}.claves()         # ["a"]
{"a": 1}.valores()        # [1]
{"a": 1}.items()          # [["a", 1]]

# Set
#{1, 2, 3}.longitud()     # 3
```

---

## 5. Biblioteca estándar

### 5.1 builtins.mice (auto-cargado)

Cargado automáticamente al iniciar. Provee las funciones globales del lenguaje.

| Función                | Descripción                                   |
|------------------------|-----------------------------------------------|
| `tipo(valor)`          | Devuelve el tipo como texto                   |
| `longitud(coleccion)`  | Longitud de lista, texto, dict, set           |
| `map(func, lista)`     | Aplica función a cada elemento                |
| `filter(pred, lista)`  | Filtra elementos según predicado              |
| `reduce(func, lista, init)` | Reduce lista a un valor                  |
| `todos(pred, lista)`   | ¿Todos cumplen el predicado?                  |
| `alguno(pred, lista)`  | ¿Alguno cumple el predicado?                  |
| `ordenar(lista)`       | Ordena lista (Timsort nativo)                 |
| `aNumero(valor)`       | Convierte a número (soporta 0b, 0o, 0x)       |
| `aTexto(valor)`        | Convierte cualquier valor a texto             |
| `error(mensaje)`       | Lanza error con mensaje                       |
| `rango(fin)` / `rango(ini, fin)` | Genera lista numérica              |
| `primero(lista)`       | Primer elemento                               |
| `ultimo(lista)`        | Último elemento                               |
| `invertir(lista)`      | Lista invertida                               |
| `concatenar(l1, l2)`   | Concatena dos listas                          |
| `aleatorio()`          | Número aleatorio entre 0 y 1                  |
| `abs(x)`               | Valor absoluto                                |
| `maximo(a, b)`         | Máximo de dos números                         |
| `minimo(a, b)`         | Mínimo de dos números                         |
| `exp(x)`               | Exponencial (e^x) nativo                      |
| `max_lista(lista)`     | Máximo valor en lista                         |
| `min_lista(lista)`     | Mínimo valor en lista                         |
| `suma(lista)`          | Suma de elementos                             |
| `producto(lista)`      | Producto de elementos                         |
| `promedio(lista)`      | Promedio aritmético                           |
| `contar(pred, lista)`  | Cuenta cuántos cumplen predicado              |
| `claves(dicc)`         | Claves de diccionario                         |
| `valores(dicc)`        | Valores de diccionario                        |
| `items(dicc)`          | Pares [clave, valor]                          |

### 5.2 math.mice

Funciones matemáticas implementadas desde cero. Trigonometría vía series de Taylor, raíces con Newton-Raphson.

```mice
importar "math.mice" como math
```

| Función                            | Descripción                |
|------------------------------------|----------------------------|
| `math.PI`                          | Constante π                |
| `math.E`                           | Constante e                |
| `math.abs(x)`                      | Valor absoluto             |
| `math.piso(x)`                     | Piso (floor)               |
| `math.techo(x)`                    | Techo (ceil)               |
| `math.redondear(x)`                | Redondeo                   |
| `math.entero(x)`                   | Parte entera               |
| `math.flotante(x)`                 | Conversión a flotante      |
| `math.factorial(n)`                | Factorial (n!)             |
| `math.potencia_entera(base, exp)`  | Potencia entera            |
| `math.seno(x)`                     | Seno (serie de Taylor)     |
| `math.coseno(x)`                   | Coseno (serie de Taylor)   |
| `math.tangente(x)`                 | Tangente (sin/cos)         |
| `math.arcotangente(x)`             | Arco tangente (Taylor)     |
| `math.arcoseno(x)`                 | Arco seno (Newton-Raphson) |
| `math.arcocoseno(x)`               | Arco coseno                |
| `math.raiz(x)`                     | Raíz cuadrada (Newton-Raphson) |
| `math.log(x)`                      | Logaritmo natural (atanh)  |
| `math.log10(x)`                    | Logaritmo base 10          |
| `math.exp(x)`                      | Exponencial (serie Taylor) |
| `math.potencia(base, exp)`         | Potencia general           |

### 5.3 matriz.mice

Álgebra lineal: ceros, unos, identidad, transpuesta, multiplicación, determinante (LU), inversa (Gauss-Jordan).

```mice
importar "matriz.mice" como mat
```

| Función                                    | Descripción                      |
|--------------------------------------------|----------------------------------|
| `mat.ceros(filas, columnas)`               | Matriz de ceros                  |
| `mat.unos(filas, columnas)`                | Matriz de unos                   |
| `mat.identidad(n)`                         | Matriz identidad n×n             |
| `mat.filas(m)`                             | Número de filas                  |
| `mat.columnas(m)`                          | Número de columnas               |
| `mat.dimensiones(m)`                       | [filas, columnas]                |
| `mat.transpuesta(m)`                       | Matriz transpuesta               |
| `mat.suma_matrices(a, b)`                  | Suma de matrices                 |
| `mat.resta_matrices(a, b)`                 | Resta de matrices                |
| `mat.multiplicar(a, b)`                    | Multiplicación matricial         |
| `mat.escalar(m, k)`                        | Multiplicación por escalar       |
| `mat.fila(m, i)`                           | Obtener fila i                   |
| `mat.columna(m, j)`                        | Obtener columna j                |
| `mat.traza(m)`                             | Traza de matriz cuadrada         |
| `mat.determinante(m)`                       | Determinante (Sarrus ≤3×3, LU)   |
| `mat.inversa(m)`                            | Matriz inversa (Gauss-Jordan)    |
| `mat.norma_frobenius(m)`                   | Norma de Frobenius               |
| `mat.aplanar(m)`                           | Aplana a lista                   |

### 5.4 ml.mice

Algoritmos de machine learning: regresión lineal, regresión logística, K-Means, métricas.

```mice
importar "ml.mice" como ml
```

| Función                                            | Descripción                          |
|----------------------------------------------------|--------------------------------------|
| `ml.dividir_datos(X, Y, proporcion)`               | Train/test split                     |
| `ml.media(valores)`                                | Media aritmética                     |
| `ml.varianza(valores)`                             | Varianza                             |
| `ml.desviacion_estandar(valores)`                   | Desviación estándar                  |
| `ml.normalizar(valores)`                           | Normalización z-score                |
| `ml.regresion_lineal(X, y)`                        | Regresión lineal (mínimos cuadrados) |
| `ml.predecir_lineal(modelo, X)`                    | Predicción lineal                    |
| `ml.r_cuadrado(y_real, y_pred)`                    | Coeficiente R²                       |
| `ml.mse(y_real, y_pred)`                           | Error cuadrático medio               |
| `ml.regresion_lineal_descenso(X, y, lr, epochs)`   | Regresión con descenso de gradiente  |
| `ml.regresion_lineal_matricial(X, y)`              | Regresión matricial                  |
| `ml.sigmoid(z)`                                    | Función sigmoide                     |
| `ml.sigmoid_derivada(z)`                           | Derivada de sigmoide                 |
| `ml.regresion_logistica(X, y, lr, epochs)`         | Regresión logística                  |
| `ml.predecir_logistica(modelo, X, umbral)`         | Predicción logística                 |
| `ml.k_means(X, k, iteraciones)`                    | Algoritmo K-Means                    |
| `ml.distancia_euclidiana(a, b)`                    | Distancia euclidiana                 |
| `ml.matriz_confusion(y_real, y_pred)`              | Matriz de confusión                  |
| `ml.exactitud(y_real, y_pred)`                     | Accuracy                             |
| `ml.precision(y_real, y_pred)`                     | Precision                            |
| `ml.recall(y_real, y_pred)`                        | Recall                               |
| `ml.f1_score(y_real, y_pred)`                      | F1-Score                             |

### 5.5 dl.mice

Deep Learning: perceptrón multicapa, forward/backpropagation, funciones de activación, entrenamiento.

```mice
importar "dl.mice" como dl
```

| Función                                                    | Descripción                          |
|------------------------------------------------------------|--------------------------------------|
| `dl.aplicar(matriz, funcion)`                              | Aplica función a cada elemento       |
| `dl.hadamard(m1, m2)`                                      | Producto Hadamard (elemento a elemento) |
| `dl.sigmoid(m)`                                            | Sigmoide sobre matriz                |
| `dl.sigmoid_derivada(m)`                                   | Derivada de sigmoide                 |
| `dl.relu(m)`                                               | ReLU sobre matriz                    |
| `dl.relu_derivada(m)`                                      | Derivada de ReLU                     |
| `dl.softmax(m)`                                            | Softmax                              |
| `dl.perceptron_multicapa(arquitectura)`                    | Crear MLP con inicialización Xavier  |
| `dl.forward(modelo, X)`                                    | Propagación hacia adelante           |
| `dl.entrenar_red(modelo, X, Y, lr, epochs, verbose)`       | Entrenamiento completo con backprop  |
| `dl.error_mse(y_real, y_pred)`                             | Error MSE                            |

### 5.6 grafico.mice

Motor gráfico que genera imágenes PPM (convertidas a PNG si Pillow está disponible).

```mice
importar "grafico.mice" como grafico
```

| Función                                          | Descripción                        |
|--------------------------------------------------|------------------------------------|
| `grafico.iniciar_grafico(ancho, alto)`           | Inicializa un gráfico              |
| `grafico.titulo(texto)`                          | Define título                      |
| `grafico.etiquetas(xlabel, ylabel)`              | Etiquetas de ejes                  |
| `grafico.lineas(xs, ys, color)`                  | Dibuja líneas                      |
| `grafico.dispersion(xs, ys)`                     | Gráfico de dispersión              |
| `grafico.histograma(datos, bins)`                | Histograma                         |
| `grafico.guardar(archivo)`                       | Guarda como PNG/PPM                |
| `grafico.mostrar()`                              | Muestra la imagen                  |
| `grafico.pintar_mapa(titulo)`                    | Prepara el lienzo                  |
| `grafico.pintar_puntos(puntos)`                  | Dibuja puntos                      |
| `grafico.color_linea(r, g, b)`                   | Define color de línea              |
| `grafico.dibujar_grafo(nodos, aristas)`          | Dibuja un grafo (layout circular)  |
| `grafico.linea_sobre_grafico(x1, y1, x2, y2)`    | Línea directa sobre gráfico        |
| `grafico.texto(texto, x, y)`                     | Texto en coordenadas               |
| `grafico.estilo(tema)`                           | Tema: claro, oscuro, ocean, retro  |

### 5.7 gui.mice

Interfaz gráfica de usuario usando zenity (Linux) y/o GTK.

```mice
importar "gui.mice" como gui
```

| Función                                              | Descripción                      |
|------------------------------------------------------|----------------------------------|
| `gui.alerta(mensaje)`                                | Mensaje de alerta                |
| `gui.confirmar(mensaje)`                             | Diálogo de confirmación          |
| `gui.pedir_texto(mensaje)`                           | Entrada de texto                 |
| `gui.abrir_archivo()`                                | Selector de archivos             |
| `gui.guardar_archivo_como()`                         | Guardar archivo                  |
| `gui.mostrar_imagen(archivo)`                        | Mostrar imagen                   |
| `gui.calculadora_ux(titulo)`                         | Calculadora interactiva (GTK)    |
| `gui.crear_menu(opciones)`                           | Menú de opciones                 |
| `gui.explorar_math()`                                | Explorador matemático interactivo|

### 5.8 hifa.mice

Microframework web estilo Flask, implementado en el runtime con `http.server`. Sin dependencias externas.

```mice
importar "hifa.mice" como hifa
```

| Función                                                    | Descripción                          |
|------------------------------------------------------------|--------------------------------------|
| `hifa.crear(nombre)`                                       | Crear aplicación web                 |
| `hifa.estaticos(app, carpeta)`                             | Servir archivos estáticos            |
| `hifa.plantillas(app, carpeta)`                            | Carpeta de plantillas                |
| `hifa.get_texto(app, ruta, contenido)`                     | Ruta GET (texto/html)                |
| `hifa.post_texto(app, ruta, contenido)`                    | Ruta POST (texto/html)               |
| `hifa.get_json(app, ruta, datos)`                          | Ruta GET (JSON)                      |
| `hifa.get_template(app, ruta, archivo, contexto)`          | Ruta GET con plantilla               |
| `hifa.redireccion(app, metodo, ruta, destino)`             | Redirección HTTP                     |
| `hifa.rutas(app)`                                          | Listar todas las rutas               |
| `hifa.iniciar(app, host, puerto)`                          | Iniciar servidor                     |
| `hifa.iniciar_con_navegador(app, host, puerto)`            | Iniciar y abrir navegador            |
| `hifa.generar_demo(ruta)`                                  | Generar proyecto demo                |

### 5.9 archivo.mice

Operaciones de archivos y parseo CSV.

```mice
importar "archivo.mice" como archivo
```

| Función                                    | Descripción                       |
|--------------------------------------------|-----------------------------------|
| `archivo.leer(ruta)`                       | Leer archivo completo             |
| `archivo.escribir(ruta, contenido)`        | Escribir archivo                  |
| `archivo.leer_lineas(ruta)`                | Leer líneas a lista               |
| `archivo.escribir_lineas(ruta, lineas)`    | Escribir lista de líneas          |
| `archivo.anexar(ruta, contenido)`          | Añadir al final del archivo       |
| `archivo.existe(ruta)`                     | Verificar si existe                |
| `archivo.eliminar(ruta)`                   | Eliminar archivo                   |
| `archivo.tamano(ruta)`                     | Tamaño del archivo                |
| `archivo.leer_csv(ruta)`                   | Parsear CSV a lista de diccionarios|
| `archivo.escribir_csv(ruta, datos)`        | Escribir datos a CSV               |

### 5.10 lista.mice

Utilidades para listas.

```mice
importar "lista.mice" como lista
```

| Función                                    | Descripción                      |
|--------------------------------------------|----------------------------------|
| `lista.contiene(elemento, lista)`          | ¿Lista contiene elemento?        |
| `lista.contar_ocurrencias(elemento, lista)`| Contar apariciones               |
| `lista.indice_de(elemento, lista)`         | Índice del elemento              |
| `lista.sin_duplicados(lista)`              | Elimina duplicados               |
| `lista.porcion(lista, inicio, fin)`        | Sublista (slice)                 |
| `lista.ordenar_asc(lista)`                 | Orden ascendente                 |
| `lista.ordenar_desc(lista)`                | Orden descendente                |
| `lista.pares(lista)`                       | Elementos en índices pares       |
| `lista.impares(lista)`                     | Elementos en índices impares     |

### 5.11 dict.mice

Utilidades para diccionarios.

```mice
importar "dict.mice" como dict
```

| Función                                        | Descripción                    |
|------------------------------------------------|--------------------------------|
| `dict.tiene_clave(dicc, clave)`                | ¿Existe clave?                 |
| `dict.obtener(dicc, clave, defecto)`           | Obtener valor con default      |
| `dict.combinar(dicc1, dicc2)`                  | Combinar diccionarios          |
| `dict.invertir(dicc)`                          | Intercambiar clave↔valor       |
| `dict.filtrar_claves(dicc, predicado)`         | Filtrar por clave              |
| `dict.mapear_valores(dicc, func)`              | Transformar valores            |
| `dict.de_listas(claves, valores)`              | Crear desde dos listas         |
| `dict.copia_profunda(dicc)`                    | Copia profunda                 |

### 5.12 set.mice

Operaciones de conjuntos.

```mice
importar "set.mice" como set
```

| Función                                            | Descripción                   |
|----------------------------------------------------|-------------------------------|
| `set.crear_conjunto(elementos)`                    | Crear conjunto                |
| `set.union(a, b)`                                  | Unión                         |
| `set.interseccion(a, b)`                           | Intersección                  |
| `set.diferencia(a, b)`                             | Diferencia                    |
| `set.diferencia_simetrica(a, b)`                   | Diferencia simétrica          |
| `set.es_subconjunto(a, b)`                         | ¿A ⊆ B?                      |
| `set.producto_cartesiano(a, b)`                    | Producto cartesiano           |
| `set.complemento(universo, conjunto)`              | Complemento                   |

---

## 6. Ejemplos por módulo

Todos los ejemplos están en `MICELIO/ejemplos/`. Se ejecutan con:

```bash
python3 main.py ejemplos/01_basico.mice
```

| Archivo                               | Descripción                                    |
|---------------------------------------|------------------------------------------------|
| `01_basico.mice`                      | Variables, aritmética, listas, I/O             |
| `02_fibonacci.mice`                   | Fibonacci recursivo                            |
| `03_matrices.mice`                    | Operaciones con matrices                       |
| `04_errores.mice`                     | Demostración de errores pedagógicos            |
| `05_funcional.mice`                   | map/filter/reduce, pipe, closures              |
| `06_caperucita.mice`                  | Procesamiento de texto                         |
| `07_perceptron_simple.mice`           | Neurona simple (compuerta AND)                 |
| `08_regresion.mice`                   | Regresión lineal                               |
| `09_k_means_visual.mice`              | K-Means con visualización                       |
| `10_autoencoder_simple.mice`          | Autoencoder simple                             |
| `11_currificacion_avanzada.mice`      | Currying                                       |
| `12_clasificador_iris_simplificado.mice` | Clasificador multiclase softmax            |
| `13_series_taylor_custom.mice`        | Series de Taylor                               |
| `14_analisis_archivos_csv.mice`       | Análisis de archivos CSV                       |
| `15_big_data_regression.mice`         | Regresión a gran escala                        |
| `16_stress_test_nn.mice`              | Prueba de estrés de red neuronal               |
| `17_debug_xor.mice`                   | Depuración de red XOR                          |
| `18_mini_batch_visual.mice`           | Entrenamiento mini-batch con visualización     |
| `19_grafico_simple.mice`              | Grafo simple                                   |
| `20_grafico_seno_coseno.mice`         | Seno y coseno superpuestos                     |
| `21_grafico_histograma.mice`          | Histograma                                     |
| `22_math_didactico.mice`              | Módulo math didáctico                          |
| `23_lista_didactica.mice`             | Utilidades de listas                           |
| `24_dict_didactico.mice`              | Diccionarios                                   |
| `25_set_didactico.mice`               | Conjuntos                                      |
| `26_matriz_didactica.mice`            | Matrices                                       |
| `27_archivo_didactico.mice`           | Archivos                                       |
| `28_ml_didactico.mice`                | Machine learning                               |
| `29_dl_didactico.mice`                | Deep learning                                  |
| `30_gui_didactico.mice`               | GUI                                            |
| `31_hifa_didactico.mice`              | Hifa web framework                             |

### Ejemplo completo: Regresión Lineal

```mice
importar "ml.mice" como ml

var X = [[1], [2], [3], [4], [5]]
var y = [2, 4, 6, 8, 10]

var modelo = ml.regresion_lineal(X, y)
imp "Modelo entrenado"

var pred = ml.predecir_lineal(modelo, [[6]])
imp "Prediccion para 6: " + aTexto(pred[0])

var mse_val = ml.mse(y, ml.predecir_lineal(modelo, X))
imp "MSE: " + aTexto(mse_val)
```

### Ejemplo completo: Perceptrón Multicapa (XOR)

```mice
importar "dl.mice" como dl

var X = [[0,0], [0,1], [1,0], [1,1]]
var Y = [[0], [1], [1], [0]]

var modelo = dl.perceptron_multicapa([2, 4, 1])
dl.entrenar_red(modelo, X, Y, 0.5, 2000, falso)

var pred = dl.forward(modelo, X)
imp "Predicciones XOR:"
imp pred
```

### Ejemplo completo: Servidor Web con Hifa

```mice
importar "hifa.mice" como hifa

var app = hifa.crear("MiApp")
hifa.get_texto(app, "/", "<h1>Hola Micelio</h1>")
hifa.get_json(app, "/api", {"mensaje": "Hola desde Hifa"})
hifa.iniciar(app, "localhost", 8080)
```

---

## 7. Arquitectura

### Pipeline de ejecución

```
archivo.mice
     │
     ▼
main.py (preprocesador)
  ├── azúcar sintáctico: leer a,b → __leer_multi("a,b")
  ├── a,b = expr → __asignar_multi("a,b", expr)
  └── x += 1 → x = x + (1)
     │
     ▼
ANTLR4 Lexer (MicelioLexer) → tokens
     │
     ▼
ANTLR4 Parser (MicelioParser) → árbol de parseo
     │
     ▼
EvalVisitor (eval_visitor.py)
  ├── recorre el árbol ANTLR
  ├── evalúa expresiones/sentencias
  ├── resuelve variables (Environment chain)
  └── delega a runtime functions
     │
     ▼
Runtime (runtime.py)
  ├── Environment (tabla de símbolos con alcance léxico)
  ├── FunctionValue (funciones Micelio con clausuras)
  ├── BoundMethod (métodos nativos en colecciones)
  ├── make_primitives() → wrappers Python de bajo nivel
  └── make_builtins() → funciones incorporadas de alto nivel
     │
     ▼
Salida (consola, archivos, imágenes PPM, ventanas GTK, HTTP)
```

### Estructura del repositorio

```
MICELIO/
├── main.py                    # Entrada CLI/REPL, preprocesador
├── micelio                    # Wrapper bash
│
├── nucleo/
│   ├── eval_visitor.py        # Visitor de evaluación semántica
│   └── runtime.py             # Entorno, builtins, gráficos, GUI, Hifa
│
├── errores/
│   └── pedagogicos.py         # Errores pedagógicos con formato glassmorphic
│
├── gramatica/
│   └── Micelio.g4             # Gramática ANTLR4 (163 reglas)
│
├── generado/
│   └── gramatica/             # Lexer/Parser/Visitor generados por ANTLR
│
├── modulos_std/               # Biblioteca estándar en Micelio puro
│   ├── builtins.mice          #   Auto-cargado al inicio
│   ├── math.mice              #   Matemáticas (Taylor, Newton-Raphson)
│   ├── matriz.mice            #   Álgebra lineal
│   ├── ml.mice                #   Machine learning
│   ├── dl.mice                #   Deep learning
│   ├── grafico.mice           #   Motor gráfico PPM
│   ├── gui.mice               #   GUI (zenity/GTK)
│   ├── hifa.mice              #   Web framework
│   ├── archivo.mice           #   Archivos y CSV
│   ├── lista.mice             #   Utilidades de listas
│   ├── dict.mice              #   Utilidades de diccionarios
│   └── set.mice               #   Operaciones de conjuntos
│
├── ejemplos/                  # 31+ ejemplos ejecutables
│   ├── 01_basico.mice
│   ├── ...
│   └── 31_hifa_didactico.mice
│
┤
├── instalación/               # Scripts de instalación
│   ├── setup.sh               #   Linux/macOS
│   ├── setup.bat              #   Windows
│   └── install-micelio.sh     #   Instalación CLI
│
├── micelio-vscode/            # Extensión VS Code
│   └── extension_unpacked/
│       └── extension/
│           ├── package.json
│           ├── extension.js
│           ├── language-configuration.json
│           ├── syntaxes/micelio.tmLanguage.json
│           └── snippets/micelio.code-snippets
│
└── docs/                      # Documentación
    ├── DOCUMENTACION.md       #   Este documento
    ├── lenguaje.md            #   Sintaxis del lenguaje
    ├── runtime.md             #   Arquitectura del runtime
    ├── estructura-proyecto.md #   Estructura del proyecto
    └── ...
```

### Componentes clave

| Archivo           | Líneas | Propósito                                    |
|-------------------|--------|----------------------------------------------|
| `main.py`         | ~200   | Entrada CLI, REPL, preprocesador             |
| `eval_visitor.py` | ~1024  | Evaluación semántica del árbol ANTLR         |
| `runtime.py`      | ~2035  | Entorno, tipos, builtins, gráficos, GUI, web |
| `pedagogicos.py`  | ~197   | Errores pedagógicos con formato ANSI         |
| `Micelio.g4`      | ~163   | Gramática completa del lenguaje              |

---

## 8. Extensiones y herramientas

### Extensión VS Code

La extensión `micelio-vscode` provee resaltado de sintaxis, snippets y autocompletado para archivos `.mice` y `.micelio`.

**Instalación:**

```bash
cd micelio-vscode
./install-local.sh
```

O desde VS Code: Extensiones → Install from VSIX → seleccionar `micelio-vscode/extension_unpacked/`.

Incluye:
- Resaltado de sintaxis (TextMate grammar)
- Snippets: `fun`, `si`, `para`, `mientras`, `imp`, `leer`, `pipe`
- Continuación automática con Enter después de `|>`
- Configuración de comentarios, brackets y auto-cierre

---

## 9. Desarrollo

### Regenerar lexer/parser desde la gramática

```bash
cd MICELIO
antlr4 -Dlanguage=Python3 gramatica/Micelio.g4 -o generado/gramatica -no-listener -visitor
```

### Dependencia única

```
antlr4-python3-runtime==4.13.1
```

### Pruebas

Los ejemplos en `MICELIO/ejemplos/` funcionan como pruebas informales:

```bash
python3 main.py ejemplos/01_basico.mice
python3 main.py ejemplos/07_perceptron_simple.mice
python3 main.py ejemplos/08_regresion.mice
```

### Errores pedagógicos

El sistema de errores muestra:

```
¿Qué pasó?      → descripción del error
¿Dónde?         → línea, columna y marca visual
¿Por qué pasa?  → causa técnica
¿Cómo arreglarlo? → sugerencia con ejemplo
```
