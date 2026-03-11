# Runtime de Micelio

## Vista general

La ejecucion de Micelio usa pipeline clasico:

1. Fuente `.mice`
2. Lexer/Parser ANTLR
3. Parse tree
4. Visitor evaluator
5. Runtime (entorno, builtins, representacion de valores)

## Archivos clave

- `MICELIO/main.py`: entrada CLI/REPL, parse y errores pedagogicos.
- `MICELIO/eval_visitor.py`: semantica del lenguaje por nodo.
- `MICELIO/runtime.py`: tipos runtime, entorno, builtins, helpers.

## Entorno y alcance

`Environment` implementa:

- `define(name, value, is_const=False)`
- `get(name)`
- `assign(name, value)`

Con soporte de scopes anidados (`parent`).

## Funciones y llamadas

- `FunctionValue`: representa funciones del lenguaje.
- `BoundMethod`: habilita metodos sobre tipos runtime (lista, texto, set, dict).
- `_call_callable`: unifica llamada de funciones declaradas y callables nativos.

## Builtins relevantes

- `map`, `filter`, `reduce`, `ordenar`
- Conversiones: `aNumero`, `aTexto`, `aBooleano`
- Bases numericas: `aBinario`, `aOctal`, `aHexadecimal`, `aBase`, `desdeBase`, etc.

## Modulo grafico (desde cero)

La logica publica de `grafico` ahora vive en `MICELIO/modulos_std/grafico.mice`.
El runtime solo aporta primitivas internas (prefijo `__grafico_`) para:

- crear/reiniciar lienzo
- dibujar pixeles/ejes
- guardar PPM

De esta forma, la API que importa el usuario es modulo estandar (`importar "grafico.mice"`) y no funciones globales del runtime.

- Implementa renderizado pixel a pixel en memoria.
- Exporta imagenes en formato `PPM` (`P3`) con `guardar(ruta)`.
- Si se pasa una ruta `.png`, se guarda como `.ppm` equivalente para mantener implementacion 100% propia.

Funciones disponibles:

- `lineas(x, y)`
- `dispersion(x, y)`
- `histograma(datos, bins)`
- `titulo(texto)`
- `etiquetas(xlabel, ylabel)`
- `guardar(ruta)`
- `mostrar()`

Archivo de referencia del modulo estandar:

- `MICELIO/modulos_std/grafico.mice`

## REPL interactivo

Arranca sin argumentos:

```
python main.py
# o
./micelio
```

### Variable `_`

El REPL guarda automaticamente el ultimo resultado en la variable `_`.

```
micelio> var a = [2, 21, 32, 2]
[2, 21, 32, 2]
micelio> _
[2, 21, 32, 2]
```

### Continuacion con `|>`

Una linea que empiece con `|>` se encadena automaticamente al resultado anterior (`_`):

```
micelio> var a = [0, 2, 1, 3]
[0, 2, 1, 3]
micelio> a = a
[0, 2, 1, 3]
micelio> |> map(funcion(x) { regresa x + 1 })
[1, 3, 2, 4]
micelio> |> filter(funcion(x) { regresa x > 2 })
[3, 4]
```

Internamente, `|> expr` se expande a `_ |> expr` antes de parsear.

> **Nota:** `_` se actualiza solo cuando la expresion devuelve un valor no nulo.
> Las sentencias (`var`, `imp`, etc.) no actualizan `_`.

## Azucar sintactico soportado

Desde `main.py` se preprocesan patrones antes de parsear:

- `leer a, b` -> llamada interna de lectura multiple.
- `a, b = expr` -> llamada interna de asignacion multiple.

Eso permite tener sintaxis amigable sin romper la gramatica base vigente.

## Desempaquetado

Soportado en:

- Declaracion: `var a, b = expr`
- Asignacion: `a, b = expr`

Reglas:

- `expr` debe evaluar a lista/tupla.
- Debe coincidir cantidad de elementos y variables.

## Formato de salida

`micelio_repr` se encarga de imprimir valores con estilo del lenguaje:

- `verdadero`, `falso`, `nulo`
- listas, sets y dicts
- texto con comillas y escapes visibles

## Consideraciones tecnicas

- El parser generado (`MicelioParser.py`) puede no reflejar cambios recientes en `.g4` si no se regenera.
- En caso de divergencia gramatica/parser, el comportamiento real lo dicta el parser generado en uso.
