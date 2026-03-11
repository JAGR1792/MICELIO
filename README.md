# MICELIO

Lenguaje de programacion DLS, con enfoque didactico, funcional y orientado a evolucionar hacia casos de ciencia de datos y ML.

## Vision del proyecto

Micelio busca ser un lenguaje en español que no sea solo "Python traducido", sino una experiencia propia:

- Sintaxis clara para aprender fundamentos de programacion.
- Soporte funcional (map/filter/reduce/ordenar + pipe `|>`).
- Mensajes de error pedagogicos (que paso, por que, como arreglarlo).
- Camino de crecimiento hacia modulos de algebra, estadistica y ML.

## Estado actual (main)

Hoy el proyecto incluye:

- Gramatica ANTLR en `MICELIO/Micelio.g4`.
- Lexer/Parser/Visitor generados en `MICELIO/`.
- Interprete por Visitor en `MICELIO/eval_visitor.py`.
- Runtime en `MICELIO/runtime.py`.
- Entrada/salida, funciones, control de flujo y modulos.
- Modulo estandar inicial: `MICELIO/modulos_std/math.mice`.
- Soporte de desempaquetado:
	- `var a, b = expr`
	- `a, b = expr`
	- `leer a, b` (entrada multiple en una linea)
- Errores pedagogicos en CLI/archivo (`MICELIO/main.py`).

## Estructura del repo

- `MICELIO/`: implementacion principal del lenguaje.
- `MICELIO/modulos_std/`: biblioteca estandar en `.mice`.
- `micelio-vscode/`: extension de sintaxis para VS Code.
- `Pruebas/`: prototipos y experimentos.
- `main.tex`: especificacion extensa de lenguaje y vision tecnica.

## Documentacion completa

La referencia tecnica completa esta en `docs/`:

- `docs/README.md`
- `docs/lenguaje.md`
- `docs/runtime.md`
- `docs/errores-pedagogicos.md`
- `docs/vscode-extension.md`
- `docs/release.md`

## Quickstart (multiplataforma)

### Requisitos previos

- **Python 3.9+** (descargable desde [python.org](https://www.python.org))
- **Git** (para clonar el repo)
- **Visual Studio Code** (recomendado) — descargable desde [code.visualstudio.com](https://code.visualstudio.com)

### 1. Clonar el repositorio

```bash
git clone https://github.com/JAGR1792/MICELIO.git
cd MICELIO
```

### 2. Ejecutar setup automatizado

Esto instala dependencias, crea el entorno virtual y configura la extensión VS Code.

**Linux / Mac:**

```bash
bash setup.sh
source venv/bin/activate
```

**Windows:**

```cmd
setup.bat
REM ya se activa automáticamente
```

### 3. Trabajar con Micelio

#### Opción A: VS Code (recomendado)

La extensión Micelio se instala automáticamente durante setup. Ofrece:

- Resaltado de sintaxis
- Snippets de código
- Autocompletado
- Integración con terminal

1. Abre VS Code
2. Abre la carpeta `MICELIO` como workspace
3. Crea archivos `.mice` o usa el terminal integrado

**Terminal integrado (en VS Code):**

```bash
# Activar venv si aún no está activo
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate.bat  # Windows

# Abrir REPL
python main.py

# O ejecutar archivo
python main.py tu_programa.mice
```

#### Opción B: Línea de comandos

```bash
cd MICELIO
python main.py                  # Abre REPL
python main.py tu_programa.mice # Ejecuta archivo
```

### Desactivar entorno virtual

Cuando termines de trabajar:

```bash
deactivate  # Linux/Mac o Windows
```

---

## Portabilidad multiplataforma

**¿Por qué estos scripts?**

- ✅ **Aislamiento**: El `venv` local no contamina el Python del sistema.
- ✅ **Reproducibilidad**: Cualquiera que clone el repo obtiene exactamente las mismas versiones (`requirements.txt`).
- ✅ **Multiplataforma**: Scripts separados para Linux/Mac (`.sh`) y Windows (`.bat`) detectan la plataforma automáticamente.
- ✅ **Sin instalaciones extras**: Solo requiere Python 3.9+ (nada más).

**Para colaboradores:**

Si colaborás en el proyecto:

1. Clona el repo
2. Ejecuta `bash setup.sh` (Linux/Mac) o `setup.bat` (Windows)
3. Comienza a desarrollar
4. El `venv/` se ignora en Git (ver `.gitignore`)

### Instalación manual de extensión VS Code

Si `setup.sh`/`setup.bat` tiene problemas instalando la extensión:

```bash
code --install-extension micelio-vscode/extension_unpacked/
```

O abre VS Code y ve a:

1. **Extensions** (Ctrl+Shift+X o Cmd+Shift+X)
2. **Install from VSIX...**
3. Busca `micelio-vscode/extension_unpacked/`

## Como esta hecho Micelio (arquitectura pedagogica)

Micelio esta construido como un interprete clasico por etapas. Esta separacion no es solo tecnica: esta pensada para aprender compiladores e interpretes de forma didactica.

1. Lexing y parsing con ANTLR.
2. Arbol de sintaxis (parse tree) generado desde la gramatica.
3. Evaluacion por Visitor (interpretacion semantica).
4. Runtime con entorno, builtins y utilidades de tipos.

Archivos clave:

- `MICELIO/Micelio.g4`: define la sintaxis del lenguaje.
- `MICELIO/MicelioLexer.py` y `MICELIO/MicelioParser.py`: generados por ANTLR.
- `MICELIO/eval_visitor.py`: interpreta nodos del arbol.
- `MICELIO/runtime.py`: entorno de ejecucion, builtins y representacion de valores.
- `MICELIO/main.py`: entrada CLI/REPL, manejo de errores y preprocesado de azucar sintactico.

## Flujo de ejecucion (de archivo `.mice` a resultado)

Cuando ejecutas `python3 main.py programa.mice`, ocurre esto:

1. Se lee el codigo fuente.
2. Se aplica preprocesado para azucar sintactico compatible (ejemplo: `leer a, b` y `a, b = expr`).
3. ANTLR tokeniza y parsea.
4. Si hay errores de sintaxis, se muestran mensajes pedagogicos.
5. El Visitor evalua sentencias/expresiones.
6. Runtime resuelve variables, funciones, tipos y metodos.
7. Se imprime salida con formato de Micelio.

## Comportamiento actual del lenguaje (resumen util)

- Tipado dinamico fuerte con conversiones explicitas.
- Variables y constantes: `var`, `const`.
- Control de flujo: `si`, `sino`, `mientras`, `para`, `segun`.
- Funciones de primera clase y funciones anonimas.
- Colecciones: lista, set, dict.
- Programacion funcional:
	- `map`, `filter`, `reduce`
	- operador pipe `|>`
- Entrada/salida:
	- `leer variable`
	- `leer a, b, c` (multiple en una linea)
	- `imp expresion`
- Desempaquetado:
	- `var a, b = expr`
	- `a, b = expr`

Nota importante:

- El desempaquetado requiere misma cantidad de variables y valores.
- Algunos identificadores no pueden usarse como variables si son palabras reservadas (`y`, `o`, `si`, etc.).

## Requisitos

- Python 3.10+
- `antlr4-python3-runtime`

Instalacion minima:

```bash
pip install antlr4-python3-runtime
```

## Ejecutar Micelio

Desde `MICELIO/`:

```bash
python3 main.py archivo.mice
```

Ejemplo:

```bash
cd MICELIO
python3 main.py A.mice
```

## Ejemplos rapidos

### 1) Pipe funcional

```mice
var datos = [1, 2, 3, 4, 5]

var total = datos
	|> map(funcion (x) { regresa x * 2 })
	|> filter(funcion (x) { regresa x > 5 })
	|> reduce(funcion (acc, x) { regresa acc + x }, 0)

imp total
```

### 2) Entrada multiple y desempaquetado

```mice
var a, b
leer a, b

var x, y = [10, 20]
a, b = [x, y]

imp a + b
```

### 3) Leer una linea y partir texto

```mice
var linea
leer linea

var p1, p2 = linea.separar()
imp p1 + " " + p2
```

## Biblioteca estandar actual

### Modulo `math.mice`

Ubicacion: `MICELIO/modulos_std/math.mice`

Incluye (resumen):

- Constantes: `PI`, `E`
- Trigonometria: `seno`, `coseno`, `tangente`
- Inversas: `arcoseno`, `arcocoseno`, `arcotangente`
- Otras: `raiz`, `log`, `log10`, `exp`, `potencia`
- Utilitarias: `abs`, `piso`, `techo`, `redondear`

Importacion:

```mice
importar "math.mice" como math
imp math.seno(math.PI / 2)
```

## Errores pedagogicos

`main.py` muestra errores en formato guiado:

- `Que paso`
- `Donde` (linea/columna + marca)
- `Por que pasa`
- `Como arreglarlo`

Esto aplica tanto para errores de sintaxis como de ejecucion.

Ejemplo de valor pedagogico:

- Si escribes `leer.separar()`, Micelio no solo marca error; tambien explica que `leer` es sentencia, no metodo, y sugiere una forma correcta.

## Extension de sintaxis de VS Code (Micelio Syntax)

Ubicacion: `micelio-vscode/extension_unpacked/extension/`

Incluye:

- Resaltado de sintaxis para `.mice` y `.micelio`.
- Configuracion de comentarios/pares.
- Snippets de pipeline.
- Continuacion automatica de `|>` con Enter.

### Instalar en otra PC

Opcion recomendada (`.vsix`):

```bash
cd micelio-vscode
./build-vsix.sh
code --install-extension micelio-syntax-0.0.4.vsix
```

Opcion local rapida:

```bash
cd micelio-vscode
./install-local.sh
```

Despues: `Developer: Reload Window` en VS Code.

## Instalador experimental (prueba ligera)

Para un prototipo ligero de instalacion sin depender de Python del usuario final, ver:

- `Pruebas/Arimetica_estable/installer/build-linux.sh`

Este flujo genera un binario standalone y un paquete instalable Linux para la prueba aritmetica.

## Estado vs especificacion (`main.tex`)

`main.tex` describe la direccion completa del lenguaje. El codigo de `main` implementa una parte funcional y creciente de esa especificacion.

Interpretacion recomendada:

- `main.tex`: contrato de vision y alcance tecnico a largo plazo.
- `README.md`: estado implementado y utilizable hoy.
- Codigo en `MICELIO/`: fuente de verdad de comportamiento actual.

## Ramas del proyecto

- `main`: nucleo del lenguaje Micelio.
- `tooling/vscode-syntax`: enfoque en extension/editor tooling.
- `experiments/pruebas-legacy`: pruebas y acercamientos experimentales.

## Limitaciones actuales

- La especificacion extensa (`main.tex`) va por delante de algunas implementaciones.
- No todo lo descrito en la vision de ML esta cerrado en runtime aun.
- Hay funcionalidades aun en estado experimental (por ejemplo instaladores por plataforma).

## Hoja de ruta sugerida (alineada con `main.tex`)

Prioridad recomendada:

1. `matriz.mice` (transpuesta, determinante, inversa, producto).
2. `estadistica.mice` (media, varianza, normalizacion).
3. `aleatorio.mice` (semilla, rand, muestreo reproducible).
4. `ml_basico.mice` (activaciones, perdida, entrenamiento minimo).

## Contribuir

1. Crea una rama desde la rama objetivo.
2. Implementa cambios pequenos y comprobables.
3. Incluye ejemplo `.mice` reproducible cuando apliquen cambios de lenguaje.
4. Si tocas extension VS Code, prueba tambien en `tooling/vscode-syntax`.

## Guia rapida de aprendizaje (pedagogica)

Ruta sugerida para nuevos usuarios:

1. Ejecuta expresiones simples y `imp`.
2. Aprende variables/constantes y control de flujo.
3. Practica funciones anonimas + `map/filter/reduce`.
4. Usa `|>` para leer pipelines de izquierda a derecha.
5. Prueba `leer` simple y multiple.
6. Usa desempaquetado para codigo mas claro.
7. Importa `math.mice` y arma mini programas modulares.

---

## Siguiente paso natural: `docs/`

Si el proyecto sigue creciendo, conviene separar esta documentacion en:

- `README.md` corto para onboarding rapido.
- `docs/lenguaje.md` (sintaxis y semantica).
- `docs/runtime.md` (entorno, tipos, builtins).
- `docs/errores-pedagogicos.md` (catalogo de errores y sugerencias).
- `docs/vscode-extension.md` (instalacion y desarrollo de sintaxis).
- `docs/release.md` (versionado, empaquetado, instaladores).

Esa estructura mantiene la entrada amigable y la referencia tecnica completa.
