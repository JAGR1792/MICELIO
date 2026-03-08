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

- `map`, `filter`, `reduce`
- Conversiones: `aNumero`, `aTexto`, `aBooleano`
- Bases numericas: `aBinario`, `aOctal`, `aHexadecimal`, `aBase`, `desdeBase`, etc.

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
