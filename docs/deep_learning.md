# Deep Learning y Redes Neuronales Artificiales (RNA)

Este documento explica los conceptos y la implementación de Redes Neuronales Artificiales (RNA) en Micelio, la API disponible en `MICELIO/modulos_std/dl.mice`, ejemplos prácticos y buenas prácticas para entrenar modelos desde cero sin librerías externas.

**Resumen técnico**
- Micelio implementa redes feedforward (perceptrón multicapa) con representación basada en diccionarios: cada capa es `{"W": matriz, "b": bias, "act": "relu|sigmoid|softmax"}`.
- `perceptron_multicapa(arquitectura)` construye un `modelo` con `modelo["capas"]`.
- `forward(modelo, X)` devuelve `{"salida": Y_pred, "activaciones": [A0, A1, ...]}` donde `A0` es la entrada `X`.
- `entrenar_red(modelo, X, Y, epochs, lr)` ejecuta un ciclo de entrenamiento (forward, backprop, update) usando gradiente descendente.

## 1) ¿Qué es una RNA?

Una Red Neuronal Artificial (RNA) es un modelo computacional inspirado en el cerebro, compuesto por capas de unidades (neuronas) que transforman entradas en salidas mediante productos lineales y funciones de activación no lineales. El entrenamiento ajusta los pesos y sesgos para minimizar una función de pérdida (ej. MSE o cross-entropy) usando retropropagación (backpropagation).

Conceptos clave:
- Neurona: suma ponderada z = W·x + b, seguida de una activación.
- Capa: colección de neuronas con la misma salida vectorial.
- Forward: propagación de entradas hacia la salida.
- Backprop: cálculo de gradientes y actualización de pesos.

## 2) API de `MICELIO/modulos_std/dl.mice`

- `perceptron_multicapa(arquitectura)` — devuelve `modelo`.
  - `arquitectura` es una lista de diccionarios con `{"in": n_in, "out": n_out, "act": "relu|sigmoid|softmax|"}`.
- `forward(modelo, X)` — ejecuta la pasada hacia delante. `X` es una lista de filas (cada fila = vector de entrada).
- `entrenar_red(modelo, X, Y, epochs, lr)` — entrena el modelo con `epochs` épocas y tasa de aprendizaje `lr`.
- Funciones de activación: `relu`, `sigmoid`, `softmax` y sus derivadas internas.
- Utilidades: `mat.filas`, `mat.columnas`, `mat.multiplicar`, `mat.transpuesta`, `mat.resta_matrices`, `mat.escalar`.

### Formato de datos
- `X`: lista de ejemplos, cada ejemplo es una lista de números (forma `[n_samples, n_features]`).
- `Y`: lista de etiquetas; para clasificación multiclase usar one-hot vectors `[n_samples, n_classes]`.

## 3) Ejemplo mínimo (XOR)

Un ejemplo típico (archivo `ejemplos/xor_test.mice`) usa:

```
importar "modulos_std/dl.mice" como dl

var X = [[0,0],[0,1],[1,0],[1,1]]
var Y = [[1,0],[0,1],[0,1],[1,0]]
var arq = [{"in":2,"out":4,"act":"relu"},{"in":4,"out":2,"act":"softmax"}]
var modelo = dl.perceptron_multicapa(arq)
dl.entrenar_red(modelo, X, Y, 2000, 0.1)
var res = dl.forward(modelo, X)
imp res["salida"]
```

Nota: `Y` en este ejemplo está en formato one-hot invertido (clase 0 -> [1,0], clase 1 -> [0,1]).

## 4) Ejemplos incluidos en el repositorio

- `ejemplos/07_perceptron_simple.mice` — neurona única (AND), enfoque didáctico.
- `ejemplos/10_autoencoder_simple.mice` — autoencoder 4→2→4.
- `ejemplos/12_clasificador_iris_simplificado.mice` — clasificación multiclase con softmax.
- `ejemplos/16_stress_test_nn.mice` — prueba con 100 registros y arquitectura 2→8→2.

Estos ejemplos muestran patrones de uso y sirven como tests de regresión para `dl.mice`.

## 5) Buenas prácticas y consejos de depuración

- Dimensiones: siempre comprobar `mat.filas(X)` y `mat.columnas(X)` antes del `forward`. Errores en dimensiones generan comportamientos extraños.
- One-hot: para softmax usar vectores one-hot en `Y` y medir pérdida categorical.
- Epochs/learning rate: empezar con pocos epochs (100–500) y lr pequeño (0.01–0.1) en datasets toy.
- Imprimir checkpoints: si la ejecución “cuelga”, insertar `imp` en el script de test (antes/después de `entrenar_red`, dentro del loop de entrenamiento) para localizar dónde queda atascado.
- Bucles `mientras`: verificar incrementos (`i = i + 1`) — causa común de bucles infinitos.

Depuración rápida (si el entrenamiento cuelga):
1. Ejecutar `dl.entrenar_red(modelo, X, Y, 10, 0.1)` con `epochs=10`.
2. Añadir `imp "entrando epoch" + aTexto(e)` dentro de `entrenar_red` (temporalmente) para identificar si el bucle de épocas avanza.
3. Reducir tamaño de datos y comprobar `forward(modelo, [[1,0]])` antes y después de `entrenar_red`.

## 6) Extensiones recomendadas (ideas de ejemplos nuevos)

- Mini-batch gradient descent (batch_size configurable).
- Algoritmos de optimización: momentum, RMSProp, Adam.
- Early stopping y guardado de pesos.
- Visualización de pérdida por época (histograma o gráfico ASCII).
- Ejemplos: regresión de series temporales, detección de anomalías con autoencoders, red convolucional simple (simulada).

## 7) Cómo contribuir con ejemplos y docs

- Añadir ejemplos en `MICELIO/ejemplos/` con nombres descriptivos `NN_*.mice`.
- Actualizar `docs/deep_learning.md` con resultados y observaciones empíricas (ej.: tiempo por epoch, convergencia).
- Incluir casos de test que se ejecuten rápido (≤ 5s) para CI local.

---

## 8) Visualizaciones y explicaciones didácticas

Hemos añadido ejemplos que integran `modulos_std/dl.mice` con `modulos_std/grafico.mice` para observar cómo cambia la frontera de decisión y cómo evolucionan las predicciones durante el entrenamiento.

- `ejemplos/17_debug_xor.mice`: Entrena la red por épocas de a una iteración (llamando repetidamente a `entrenar_red(...,1,lr)`) y guarda checkpoints visuales (`xor_init.ppm`, `xor_epoch_*.ppm`). Esto permite localizar fácilmente si el bucle de entrenamiento avanza y cómo cambia la clasificación en la rejilla de entrada. Técnica didáctica: entrenar en pasos pequeños y salvar imágenes ayuda a entender la dinámica del gradiente.

- `ejemplos/18_mini_batch_visual.mice`: Genera un dataset no lineal (círculo) y entrena la red por mini-batches; cada cierto número de épocas calcula una rejilla de puntos, evalúa la red y guarda una imagen con la clasificación de la rejilla y los puntos de entrenamiento superpuestos. Técnica didáctica: visualizar la rejilla muestra claramente la generalización de la red y los falsos positivos/negativos.

Cómo funcionan las visualizaciones (resumen técnico):

- `grafico.iniciar_grafico(xmin,xmax,ymin,ymax)` configura el lienzo y escala la coordenada de datos al espacio de píxeles.
- `grafico.pintar_puntos(xs, ys, r,g,b, tam)` dibuja marcadores sin resetear el lienzo, permitiendo componer capas (rejilla de decisión + puntos de entrenamiento).
- `grafico.guardar(path)` escribe el archivo `.ppm` que se puede abrir con cualquier visor de imágenes.

Sugerencia didáctica: ejecutar `ejemplos/17_debug_xor.mice` con `epochs` bajos y revisar los archivos `xor_epoch_*.ppm` en orden para construir una animación (por ejemplo con `convert -delay 20 -loop 0 xor_epoch_*.ppm xor.gif`).

---

Si querés, puedo:
- Añadir una tarea para generar una animación GIF automáticamente desde los checkpoints (requiere ImageMagick disponible en el sistema).
- Implementar `early stopping` y `guardar_mejor_modelo` en `dl.mice`.


Si querés, puedo:
- Generar un ejemplo nuevo `ejemplos/17_mini_batch_nn.mice` que muestre mini-batches y early stopping.
- Añadir instrucciones paso a paso para reproducir el experimento XOR y comprobar por qué se colgó la ejecución (prints de depuración).

Indícame qué prefieres que haga ahora.
