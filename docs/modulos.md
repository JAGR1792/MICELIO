# Modulos de la biblioteca estandar

MICELIO incluye una biblioteca estandar implementada en MICELIO puro.
Los modulos se cargan con `importar "ruta" como alias`.

---

## builtins.mice (auto-cargado)

Se carga automaticamente al iniciar el interprete. No necesita `importar`.

### Funciones de orden superior

```mice
map(funcion, lista)      # Aplica funcion a cada elemento
filter(predicado, lista)  # Filtra segun predicado
reduce(funcion, lista, inicio)  # Reduce a un valor
todos(predicado, lista)  # True si todos cumplen
alguno(predicado, lista)  # True si alguno cumple
contar(predicado, lista)  # Cuantos cumplen
```

### Transformacion de datos

```mice
ordenar(lista)           # Quicksort, devuelve copia ordenada
invertir(lista)          # Invierte orden
concatenar(lista1, lista2)
aNumero(valor)           # Texto a numero (0b, 0o, 0x)
aTexto(valor)            # Cualquier valor a texto
rango(*args)             # rango(fin) o rango(inicio, fin)
primero(lista)           # Primer elemento
ultimo(lista)            # Ultimo elemento
```

### Matematicas basicas

```mice
abs(x)                   # Valor absoluto
maximo(a, b), minimo(a, b)
exp(x)                   # e^x por Taylor (6 terminos)
aleatorio()              # Pseudoaleatorio [0, 1) via LCG
suma(lista), producto(lista), promedio(lista)
max_lista(lista), min_lista(lista)
```

### Introspection

```mice
tipo(valor)              # Tipo del valor
longitud(coleccion)      # Largo de lista/texto/dict
```

---

## math.mice

Trigonometria, logaritmos, redondeo y constantes.

```
importar "math.mice" como math
```

### Constantes

```
PI = 3.141592653589793
E  = 2.718281828459045
```

### Redondeo y conversion

| Funcion | Descripcion |
|---------|-------------|
| `entero(x)` | Trunca a entero (hacia cero) |
| `flotante(x)` | Convierte a flotante |
| `piso(x)` | Parte entera inferior (floor) |
| `techo(x)` | Parte entera superior (ceil) |
| `redondear(x)` | Redondeo clasico |

### Potencias y factorial

| Funcion | Descripcion |
|---------|-------------|
| `potencia_entera(base, exp)` | `base^exp` con exp entero (soporta negativos) |
| `potencia(x, exponente)` | `x^y` con exponente real |
| `factorial(n)` | `n!` recursivo |
| `raiz(x)` | Raiz cuadrada (Newton-Raphson) |
| `exp(x)` | `e^x` por Taylor (30 terminos) |

### Logaritmos

| Funcion | Descripcion |
|---------|-------------|
| `log(x)` | Logaritmo natural |
| `log10(x)` | Logaritmo base 10 |

### Trigonometria

| Funcion | Descripcion |
|---------|-------------|
| `seno(x)` | Seno en radianes |
| `coseno(x)` | Coseno en radianes |
| `tangente(x)` | Tangente en radianes |
| `arcotangente(x)` | Arco tangente (atan) |
| `arcoseno(x)` | Arco seno (asin) |
| `arcocoseno(x)` | Arco coseno (acos) |

### Utilerias

| Funcion | Descripcion |
|---------|-------------|
| `normalizar_angulo(x)` | Normaliza angulo a `[-PI, PI]` |
| `abs(x)` | Valor absoluto |

---

## matriz.mice

Algebra lineal: matrices, determinante, inversa, multiplicacion.

```
importar "matriz.mice" como mat
```

### Creacion

| Funcion | Descripcion |
|---------|-------------|
| `ceros(filas, columnas)` | Matriz de ceros |
| `unos(filas, columnas)` | Matriz de unos |
| `identidad(n)` | Matriz identidad `n x n` |

### Propiedades

| Funcion | Descripcion |
|---------|-------------|
| `filas(m)` | Numero de filas |
| `columnas(m)` | Numero de columnas |
| `dimensiones(m)` | `[filas, columnas]` |
| `traza(m)` | Suma diagonal (cuadrada) |
| `norma_frobenius(m)` | Norma de Frobenius |
| `es_matriz_valida(m)` | Valida estructura |
| `copia(m)` | Copia superficial |

### Acceso

| Funcion | Descripcion |
|---------|-------------|
| `fila(m, n)` | Fila n-esima |
| `columna(m, n)` | Columna n-esima |
| `aplanar(m)` | Convierte a vector |

### Operaciones

| Funcion | Descripcion |
|---------|-------------|
| `suma_matrices(m1, m2)` | Suma elemento a elemento |
| `resta_matrices(m1, m2)` | Resta elemento a elemento |
| `multiplicar(m1, m2)` | Multiplicacion matricial |
| `escalar(m, valor)` | Multiplicacion por escalar |
| `transpuesta(m)` | Transposicion |
| `determinante(m)` | Determinante (Sarrus o LU) |
| `gauss_jordan(m)` | Eliminacion con pivoteo |
| `inversa(m)` | Matriz inversa |

---

## ml.mice

Machine learning clasico: regresion lineal/logistica, K-Means, metricas.

```
importar "ml.mice" como ml
```

### Regresion lineal

| Funcion | Descripcion |
|---------|-------------|
| `regresion_lineal(X, Y)` | Pendiente e intercepcion por minimos cuadrados |
| `predecir_lineal(x, modelo)` | Predice con modelo lineal |
| `regresion_lineal_descenso(X, Y, lr, iter)` | Regresion por descenso de gradiente |
| `regresion_lineal_matricial(X, Y)` | Minimos cuadrados via `(X^T X)^-1 X^T Y` |

### Regresion logistica

| Funcion | Descripcion |
|---------|-------------|
| `sigmoid(z)` | Funcion sigmoide |
| `sigmoid_derivada(z)` | Derivada de sigmoide |
| `regresion_logistica(X, Y, lr, iter)` | Clasificacion binaria por gradiente |
| `predecir_logistica(x, modelo)` | Predice clase (0/1) con umbral 0.5 |

### Clustering

| Funcion | Descripcion |
|---------|-------------|
| `k_means(X, k, iteraciones)` | K-Means: agrupa en k clusters |
| `distancia_euclidiana(p1, p2)` | Distancia entre dos puntos |

### Metricas

| Funcion | Descripcion |
|---------|-------------|
| `mse(y_real, y_pred)` | Error cuadratico medio |
| `r_cuadrado(y_real, y_pred)` | Coeficiente de determinacion |
| `matriz_confusion(pred, reales)` | `{tp, tn, fp, fn}` |
| `exactitud(pred, reales)` | Accuracy |
| `precision(pred, reales)` | Precision |
| `recall(pred, reales)` | Sensibilidad |
| `f1_score(pred, reales)` | F1-score |

### Preprocesamiento

| Funcion | Descripcion |
|---------|-------------|
| `dividir_datos(X, Y, proporcion_train)` | Divide en train/test |
| `media(valores)` | Media aritmetica |
| `varianza(valores)` | Varianza |
| `desviacion_estandar(valores)` | Desviacion estandar |
| `normalizar(valores)` | Z-score |

---

## dl.mice

Deep learning: perceptron multicapa con retropropagacion.

```
importar "../stdlib/dl.mice" como dl
```

### Activaciones

| Funcion | Descripcion |
|---------|-------------|
| `sigmoid(m)` | Sigmoide sobre matriz |
| `sigmoid_derivada(m)` | Derivada de sigmoide |
| `relu(m)` | ReLU sobre matriz |
| `relu_derivada(m)` | Derivada de ReLU |
| `softmax(m)` | Softmax por filas (con estabilidad numerica) |

### Red neuronal

| Funcion | Descripcion |
|---------|-------------|
| `perceptron_multicapa(arquitectura)` | Inicializa pesos/sesgos con Xavier |
| `forward(modelo, X)` | Propagacion hacia adelante |
| `entrenar_red(modelo, X, Y, epochs, lr)` | Entrena con backpropagation |
| `error_mse(y_true, y_pred)` | Error cuadratico medio |
| `hadamard(m1, m2)` | Producto elemento a elemento |

### Ejemplo minimo

```mice
var red = dl.perceptron_multicapa([2, 4, 1])   # 2 entradas, 4 ocultas, 1 salida
dl.entrenar_red(red, X, Y, 1000, 0.1)
var pred = dl.forward(red, X)
```

---

## grafico.mice

Graficacion 2D: lineas, dispersion, histograma, exportar PNG.

```
importar "grafico.mice" como plt
```

### Configuracion

| Funcion | Descripcion |
|---------|-------------|
| `estilo(nombre)` | "claro", "oscuro", "ocean", "retro" |
| `marcadores(activo, tamano)` | Activa puntos y su tamano |
| `color_linea(r, g, b)` | Color RGB para lineas |
| `iniciar_grafico(xmin, xmax, ymin, ymax)` | Crea grafico con rejilla y ejes |
| `titulo(texto)` | Titulo del grafico |
| `etiquetas(xtext, ytext)` | Etiquetas de ejes |

### Graficado

| Funcion | Descripcion |
|---------|-------------|
| `lineas(x, ys)` | Grafica linea conectando puntos |
| `dispersion(x, ys)` | Grafico de dispersion |
| `histograma(datos, bins)` | Histograma |
| `pintar_puntos(xs, ys, r, g, b, tam)` | Dibuja puntos con color |
| `pintar_mapa(xs, ys, clases, c0, c1)` | Mapa de puntos por clase |
| `linea_sobre_grafico(xs, ys)` | Linea sobre grafico existente |
| `texto(x, y, str, r, g, b)` | Texto en posicion |

### Salida

| Funcion | Descripcion |
|---------|-------------|
| `guardar(path)` | Exporta a PNG |
| `mostrar()` | Guarda y abre ventana |

---

## gui.mice

Ventanas y dialogos GTK. Calculadora interactiva y explorador de funciones.

```
importar "gui.mice" como gui
```

### Dialogos

| Funcion | Descripcion |
|---------|-------------|
| `alerta(mensaje)` | Dialogo de alerta |
| `confirmar(mensaje)` | Dialogo Si/No |
| `pedir_texto(prompt, defecto)` | Entrada de texto |
| `pedir_numero(prompt, defecto)` | Entrada numerica validada |
| `abrir_archivo()` | Selector de archivo |
| `guardar_archivo_como(sugerido)` | Guardar como |

### Mensajes

| Funcion | Descripcion |
|---------|-------------|
| `mensaje_exito(titulo, msg)` | Dialogo de exito |
| `mensaje_error(titulo, msg)` | Dialogo de error |
| `mensaje_info(titulo, msg)` | Dialogo informativo |

### Aplicaciones

| Funcion | Descripcion |
|---------|-------------|
| `calculadora_ux()` | Calculadora interactiva |
| `calculadora_ux_tamano(w, h)` | Calculadora con tamano personalizado |
| `calculadora_ux_estilo(estilo)` | Calculadora con tema |
| `mostrar_imagen(ruta, titulo)` | Visor de imagenes |
| `explorar_math(mod_math)` | Explorador de funciones matematicas |

### Temas

| Funcion | Descripcion |
|---------|-------------|
| `estilo(nombre)` | Cambia tema visual |
| `estilo_actual()` | Tema actual |
| `estilos_disponibles()` | Lista de temas |

---

## archivo.mice

Lectura y escritura de archivos, soporte CSV.

```
importar "archivo.mice" como archivo
```

| Funcion | Descripcion |
|---------|-------------|
 | `leer_archivo(ruta)` | Lee archivo completo |
 | `escribir(ruta, contenido)` | Escribe contenido |
 | `leer_lineas(ruta)` | Lee lineas como lista |
 | `escribir_lineas(ruta, lineas)` | Escribe lista de lineas |
 | `anexar(ruta, contenido)` | Anade al final |
 | `existe(ruta)` | Verifica existencia |
 | `eliminar(ruta)` | Elimina archivo |
 | `tamano(ruta)` | Tamano en bytes |
 | `leer_csv(ruta, delim)` | Lee CSV |
 | `escribir_csv(ruta, datos, delim)` | Escribe CSV |
 | `leer_json(ruta)` | Lee archivo JSON a estructura |
 | `escribir_json(ruta, datos)` | Escribe estructura como JSON |
 | `cargar_numeros(ruta, delim, saltar_cabecera)` | CSV a lista de numeros (ML) |
 | `cargar_dataset(ruta, col_target, delim, saltar_cabecera)` | CSV a {X, Y} (ML) |
 | `cargar_matriz(ruta, delim, saltar_cabecera)` | CSV a matriz (DL) |
 | `guardar_datos(ruta, datos, cabeceras, delim)` | Guarda datos numericos como CSV |

---

## lista.mice

Funciones auxiliares para listas.

```
importar "lista.mice" como lista
```

| Funcion | Descripcion |
|---------|-------------|
| `contiene(lista, elem)` | Busqueda |
| `contar_ocurrencias(lista, elem)` | Frecuencia |
| `indice_de(lista, elem)` | Posicion (-1 si no existe) |
| `sin_duplicados(lista)` | Unicos, preserva orden |
| `porcion(lista, inicio, fin)` | Sublista |
| `repetir(lista, n)` | Repite cada elemento n veces |
| `intercalar(lista1, lista2)` | Alterna elementos |
| `rellenar(lista, n, valor)` | Extiende hasta longitud n |
| `agrupar(lista, tamano)` | Particiona en grupos |
| `ordenar_asc(lista)` | Orden ascendente (burbuja) |
| `ordenar_desc(lista)` | Orden descendente (burbuja) |
| `pares(lista)` | Elementos en indices pares |
| `impares(lista)` | Elementos en indices impares |
