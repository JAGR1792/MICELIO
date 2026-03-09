# GTK En Micelio (GUI Embebida)

## Que es GTK

GTK (GIMP Toolkit) es una libreria de interfaz grafica para aplicaciones de escritorio.
En Linux es una opcion muy comun para construir ventanas, botones, dialogos, barras y widgets.

En Micelio se usa via PyGObject (`gi.repository`) como backend de la capa GUI del runtime.

## Por que usamos GTK aqui

- `tkinter` no siempre esta instalado en todos los entornos Python.
- Se necesita una ventana tipo app para el graficador, no solo abrir archivos sueltos.
- GTK permite embebido real de imagen y controles en la misma ventana.

## Mini framework GUI en Micelio

Ademas de `plot`, el modulo `modulos_std/gui.mice` ahora funciona como una capa reusable,
tipo mini toolkit, construida por nosotros en Micelio y montada sobre primitivas del runtime.

Componentes base disponibles:

- `accion(id, etiqueta, descripcion)`
- `crear_menu(titulo, descripcion)`
- `menu_agregar(menu, item)`
- `menu_seleccionar(menu, valor_defecto)`
- `pedir_numero(prompt, valor_defecto)`

Con esto puedes crear interfaces por dialogos para cualquier modulo (`math`, `matriz`, `ml`, etc.),
manteniendo el frontend desacoplado de la logica de negocio.

## Arquitectura (Micelio + runtime)

La API publica la consume el usuario desde modulos `.mice`:

- `modulos_std/grafico.mice`
- `modulos_std/gui.mice`

El runtime en Python expone primitivas internas (`__gui_*`, `__grafico_*`) y ejecuta la parte nativa de ventana.

Flujo simplificado:

1. El programa Micelio llama `plot.mostrar()`.
2. `grafico.mice` delega a `__grafico_mostrar(...)`.
3. El runtime abre una ventana GTK embebida con la imagen del grafico.
4. El usuario puede hacer zoom, ajustar, guardar y cerrar desde esa misma ventana.

## Funcionamiento de la ventana GTK del graficador

Implementado en:

- `MICELIO/runtime.py` (funcion `_gtk_show_image_window`)

Controles incluidos:

- `+`: zoom in
- `-`: zoom out
- `Ajustar`: encaja la imagen al viewport
- `1:1`: escala real
- `Guardar como...`: exporta en ruta elegida por el usuario
- `Cerrar`

Barra de estado:

- Resolucion de la imagen
- Porcentaje de zoom
- Eventos simples como guardado

## Exportacion de imagen

Formato base:

- PPM (`P3`) generado desde cero por el modulo grafico.

Exportacion PNG:

- Si el usuario guarda como `.png`, se usa ImageMagick (`convert` o `magick`) cuando esta disponible.

## Dependencias reales

Minimas para GUI embebida:

- Python con `gi` (PyGObject)
- GTK 3 (`Gtk`, `GdkPixbuf`)

Opcionales:

- `zenity` (dialogs fallback)
- `xdg-open` (fallback de apertura)
- `convert`/`magick` (PNG)

## Codigo de referencia (lineas clave)

- `MICELIO/runtime.py`: `_gtk_show_image_window`
- `MICELIO/runtime.py`: `_plot_mostrar`
- `MICELIO/runtime.py`: `_gui_alert`, `_gui_confirm`, `_gui_input`, `_gui_open_file`, `_gui_save_file`, `_gui_show_image`
- `MICELIO/modulos_std/grafico.mice`: API de graficado y llamadas a runtime
- `MICELIO/modulos_std/gui.mice`: API GUI de alto nivel

## Ejemplo rapido

```micelio
importar "gui.mice" como gui
importar "grafico.mice" como plot

plot.estilo("ocean")
plot.titulo("Demo GTK")
plot.etiquetas("x", "y")
plot.lineas([1,2,3,4], [1,4,9,16])

# Abre ventana embebida con controles y guardado
plot.mostrar()
```

## Ejemplo GUI para modulo math

```micelio
importar "gui.mice" como gui
importar "math.mice" como mth

# Abre explorador de operaciones matematicas en GUI
gui.math(mth)
```

El explorador incluye operaciones unarias (seno, coseno, log, raiz, etc.), potencia y constantes.
La UI pide argumentos y el backend del modulo `math` ejecuta el calculo.

## Notas de compatibilidad

- Si GTK no esta disponible, el runtime usa fallback (`zenity`, luego visor del sistema).
- La API del lenguaje no cambia: siempre llamas funciones Micelio desde los modulos.
