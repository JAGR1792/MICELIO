# Estructura del proyecto MICELIO

## Vision general

```
MICELIO/
├── MICELIO/                  # implementacion del interprete
│   ├── main.py               # punto de entrada CLI/REPL
│   ├── gramatica/            # gramatica ANTLR (.g4)
│   ├── generado/             # codigo generado por ANTLR
│   ├── nucleo/               # logica de ejecucion
│   │   ├── eval_visitor.py   # semantica de sentencias/expresiones
│   │   └── runtime.py        # entorno, tipos, builtins
│   ├── errores/              # errores pedagogicos
│   ├── stdlib/          # biblioteca estandar en .mice
│   └── hifa_demo_test/       # demo web Hifa
├── docs/                     # documentacion
├── micelio-vscode/           # extension VS Code
├── instalacion/              # scripts de instalacion
└── Pruebas/                  # prototipos historicos
```

## MICELIO/main.py — Punto de entrada

`main.py` es el punto de entrada del interprete. Sus responsabilidades:

1. **Preprocesamiento**: transforma azucar sintactico antes del parseo:
   - `leer a, b` → llamada interna de lectura multiple
   - `a, b = expr` → asignacion multiple
   - `|> expr` en REPL → se encadena al resultado anterior (`_`)

2. **Compilacion**: instancia lexer/parser ANTLR, genera el arbol de parseo.

3. **Ejecucion**: delega al visitor (`eval_visitor.py`) que recorre el AST.

4. **Errores**: captura excepciones y las pasa al sistema de errores pedagogicos.

Modo de uso:
```bash
python3 main.py              # REPL interactivo
python3 main.py archivo.mice # ejecutar archivo
python3 main.py -e "imp 2+2" # ejecutar expresion inline
```

## MICELIO/gramatica/ — Fuente de verdad sintactica

`Micelio.g4` es la gramatica ANTLR que define toda la sintaxis del lenguaje.

Para regenerar el parser tras editar la gramatica:
```bash
cd MICELIO
bash regenerar_parser.sh
```

Esto produce los archivos en `MICELIO/generado/`:
- `MicelioLexer.py`, `MicelioParser.py`
- `MicelioListener.py`, `MicelioVisitor.py`
- Archivos `.interp`, `.tokens`

## MICELIO/nucleo/ — Logica de ejecucion

### eval_visitor.py

Implementa el patron Visitor de ANTLR. Cada nodo del AST tiene un metodo
visitante que define su semantica. Optimizaciones:

- **Tabla de despacho O(1)**: reemplaza `hasattr()` por un `dict[type → method]`
- **Busqueda rapida de variables**: verifica `self.env` primero (~90% de accesos)
- **Asignacion rapida**: mismo principio

### runtime.py

Define:

- `Environment`: entorno con scopes anidados (`parent`)
  - `define(name, value, is_const)`
  - `get(name)`
  - `assign(name, value)`
- `FunctionValue`: funciones definidas por el usuario
- `BoundMethod`: metodos sobre tipos runtime (lista, texto, set, dict)
- `_call_callable`: despacho unificado de llamadas
- Tipos nativos: Numero, Booleano, Texto, Lista, Set, Dict, Nulo
- Representacion: `micelio_repr()` para salida con formato del lenguaje

## MICELIO/stdlib/ — Biblioteca estandar en MICELIO puro

Modulos implementados completamente en `.mice`:

| Modulo | Archivo | Proposito |
|--------|---------|-----------|
| builtins | `builtins.mice` | Auto-cargado: exp, aleatorio, ordenar, map, filter, reduce |
| math | `math.mice` | PI, E, raiz, seno, coseno, tan, log, etc. |
| matriz | `matriz.mice` | Operaciones con matrices |
| grafico | `grafico.mice` | Graficacion 2D (renderiza PPM in-memory) |
| gui | `gui.mice` | Ventanas GTK |
| hifa | `hifa.mice` | Framework web HTTP |
| archivo | `archivo.mice` | IO de archivos |
| lista | `lista.mice` | Utilidades para listas |
| dict | `dict.mice` | Utilidades para diccionarios |
| set | `set.mice` | Utilidades para conjuntos |
| ml | `ml.mice` | ML basico (regresion lineal, KNN, k-medias) |
| dl | `dl.mice` | Deep learning (perceptron, retropropagacion) |

## Pipeline de ejecucion

```
Fuente .mice
    ↓
main.py (preprocesamiento: azucar sintactico)
    ↓
Lexer ANTLR (MicelioLexer) → tokens
    ↓
Parser ANTLR (MicelioParser) → parse tree
    ↓
eval_visitor.py (recorre AST, ejecuta semantica)
    ↓
runtime.py (entorno, tipos, builtins)
    ↓
Resultado (salida por pantalla o archivo)
```

## Extension VS Code

`micelio-vscode/` contiene la extension para VS Code con:

- Resaltado de sintaxis (gramatica TextMate en `micelio.tmLanguage.json`)
- Snippets para construcciones comunes (funcion, si, mientras, para)
- Comando "Micelio: Ejecutar archivo"
- Numeracion de linea y plegado de codigo

Empaquetado:
```bash
bash micelio-vscode/build-vsix.sh
```

Instalacion local:
```bash
bash micelio-vscode/install-local.sh
```

## Graficos (renderizado propio)

El modulo `grafico.mice` implementa renderizado pixel a pixel en memoria
usando el formato PPM (P3). No depende de ninguna libreria grafica externa.

Si se pasa una ruta `.png`, se guarda como `.ppm` equivalente para mantener
la implementacion 100% propia. Si PIL esta instalado, se convierte a PNG real.

Funciones disponibles: `lineas()`, `dispersion()`, `histograma()`,
`titulo()`, `etiquetas()`, `guardar()`, `mostrar()`.

## Sistema de errores pedagogicos

Cada error muestra cuatro partes:

```
Que paso?      → descripcion del error
Donde?         → linea, columna y marca visual
Por que pasa?  → causa tecnica
Como arreglarlo? → sugerencia con ejemplo
```

## Pruebas

El proyecto incluye ejemplos ejecutables en `MICELIO/ejemplos/` que funcionan
como pruebas de regresion. Cada modulo de la biblioteca estandar tiene al menos
un ejemplo asociado.

## Flujo de contribucion

1. Editar sintaxis solo en `MICELIO/gramatica/Micelio.g4`
2. Regenerar ANTLR hacia `MICELIO/generado/`
3. Ajustar semantica en `MICELIO/nucleo/`
4. Ajustar mensajes de error en `MICELIO/errores/`
5. Actualizar docs cuando cambie estructura o comportamiento
