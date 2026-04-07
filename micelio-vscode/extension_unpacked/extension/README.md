# Micelio Syntax v0.1.0

Extensión de VS Code para Micelio - lenguaje de programación educativo en español.

## 🎨 Características

- **Resaltado de sintaxis**: Palabras clave, funciones built-in, números, strings, comentarios
- **Autocompletado inteligente de módulos**: 
  - Escribe `importar "math.mice" como math`
  - Luego escribe `math.` y obtén sugerencias de todas las funciones (PI, E, abs, piso, etc.)
- **Fragmentos de código (snippets)**: Plantillas para importar, pipes, funciones
- **Configuración de lenguaje**: Cierre automático de paréntesis/corchetes, formateo

## 🔍 Funciones Resaltadas

### Core Built-ins
- `tipo`, `longitud`, `rango`, `error`
- `map`, `filter`, `reduce` - operaciones funcionales
- `aNumero`, `aTexto` - conversiones
- `primero`, `ultimo`, `invertir`, `concatenar`

### Matemáticas
- `abs`, `exp`, `maximo`, `minimo`
- `max_lista`, `min_lista`, `suma`, `producto`, `promedio`

### Predicados
- `todos`, `alguno`, `contar`

### Diccionarios
- `claves`, `valores`, `items`

## 🚀 Uso

### Importar módulos con alias

```micelio
importar "math.mice" como math

# Ahora escribe math. y obtén sugerencias
im math.PI
im math.abs(-5)
im math.seno(1)
```

### Usar pipes con composición

```micelio
[1, 2, 3, 4, 5]
  |> map(funcion (x) { x * 2 })
  |> filter(funcion (x) { x > 4 })
  |> ordenar()
```

## 🔄 Versiones

- **0.1.0**: Autocompletado de módulos, resaltado mejorado, snippets

## 📝 Módulos Disponibles

- `builtins.mice` - Funciones globales (cargado automáticamente)
- `math.mice` - Trigonometría, potencias, logaritmos
- `lista.mice` - Operaciones con listas
- `matriz.mice` - Álgebra lineal
- `set.mice` - Operaciones de conjuntos
- `dict.mice` - Utilidades de diccionarios
- `archivo.mice` - I/O de archivos
- `ml.mice` - Algoritmos de machine learning
