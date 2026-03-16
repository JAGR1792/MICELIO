# Lenguaje Micelio

## Objetivo

Micelio es un lenguaje interpretado en espanol con enfoque didactico, soporte funcional y crecimiento hacia ciencia de datos y ML.

## Elementos principales

- Declaracion: `var`, `const`
- Control de flujo: `si`, `sino`, `mientras`, `para`, `segun`
- Funciones: `funcion`, `regresa`
- IO: `leer`, `imp`
- Modulos: `importar "archivo.mice" como alias`
- Operadores funcionales: `map`, `filter`, `reduce`, `ordenar`, `|>`

## Tipos y colecciones

- Numero
- Booleano: `verdadero`, `falso`
- Texto
- Lista
- Set
- Dict
- Nulo: `nulo`

## Ejemplos

### Variables y salida

```mice
var x = 10
const base = 2
imp x + base
```

### Condicional

```mice
var x = 5
si (x > 0) {
  imp "positivo"
} sino {
  imp "no positivo"
}
```

### Pipeline funcional

```mice
var datos = [1, 2, 3, 4, 5]

var total = datos
  |> map(funcion (x) { regresa x * 2 })
  |> filter(funcion (x) { regresa x > 5 })
  |> reduce(funcion (acc, x) { regresa acc + x }, 0)

imp total
```

### Entrada multiple y desempaquetado

```mice
var a, b
leer a, b

var x, y = [10, 20]
a, b = [x, y]

imp a + b
```

## Reglas utiles

- `leer` simple: `leer variable`
- `leer` multiple: `leer a, b, c` (una linea de entrada con misma cantidad de valores)
- Desempaquetado:
  - `var a, b = expr`
  - `a, b = expr`
- Para desempaquetar, `expr` debe evaluar a lista/tupla con misma longitud.

## Palabras reservadas

No uses como identificadores: `si`, `sino`, `y`, `o`, `no`, `funcion`, `var`, `const`, etc.

## Estado actual vs especificacion

La referencia de vision amplia esta en `main.tex`. El comportamiento real se define por:

- `MICELIO/grammar/Micelio.g4`
- `MICELIO/core/eval_visitor.py`
- `MICELIO/core/runtime.py`

## Proxima ampliacion sugerida

1. Modulo `matriz.mice`
2. Modulo `estadistica.mice`
3. Modulo `aleatorio.mice`
4. Modulo `ml_basico.mice`
