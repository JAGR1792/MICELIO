# Errores Pedagogicos

## Objetivo

En vez de mostrar errores crudos, Micelio muestra mensajes guiados para aprendizaje.

Formato:

- `Que paso`
- `Donde`
- `Por que pasa`
- `Como arreglarlo`

## Donde se implementa

- `MICELIO/main.py`
  - Listener de errores de ANTLR
  - Formateadores de errores de sintaxis y ejecucion
  - Hints por patron conocido

## Errores de sintaxis (ejemplo)

Caso invalido:

```mice
a = map(aTexto, leer.separar())
```

Explicacion pedagogica esperada:

- `leer` es sentencia, no metodo.
- Alternativa sugerida:

```mice
var linea
leer linea
var partes = linea.separar()
```

## Errores de ejecucion (ejemplo)

Caso invalido:

```mice
imp z
```

Respuesta pedagogica:

- variable no definida
- sugerencia de declaracion previa con `var`

## Casos cubiertos actualmente

- Variable no definida
- Redeclaracion en mismo ambito
- Intento de invocar no-callable
- Desempaquetado invalido
- `leer` multiple con cantidad incorrecta
- Asignacion multiple con cantidad incorrecta

## Como ampliar el catalogo

1. Detectar nuevo patron frecuente.
2. Agregar regla en `_syntax_hint` o `_runtime_hint`.
3. Agregar ejemplo minimo reproducible.
4. Verificar salida en CLI (`python main.py archivo.mice`).

## Recomendacion

Mantener mensajes cortos y accionables. Priorizar sugerencias que el usuario pueda copiar y adaptar rapido.
