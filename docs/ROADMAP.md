# Hoja de Ruta — MICELIO

> **¿Qué aprender para construir esto?** -> Ver [GUIA_APRENDIZAJE.md](GUIA_APRENDIZAJE.md) — ruta completa desde cero hasta compilador Rust, con semanas, recursos y proyectos por cada bloque.

**Versión:** 0.3.1  
**Estado:** MVP funcional (intérprete Python + ANTLR)  
**Meta:** Lenguaje autónomo de enseñanza de IA en español. Sin dependencias externas de ML/DL. Código MICELIO se compila a binario nativo vía Rust + LLVM. Bucles a velocidad C. Filosofía "Solo MICELIO" intacta — el compilador es invisible, el algoritmo está en `.mice`.

---

## 1. Visión

MICELIO es un lenguaje de programación en español diseñado desde cero para enseñar los fundamentos de inteligencia artificial, machine learning y deep learning. Sus pilares:

- **Cero cajas negras**: cada algoritmo de ML/DL está escrito en MICELIO puro, visible y modificable por el estudiante.
- **Paradigma funcional** como base: funciones como ciudadanos de primera clase, pipe operator, closures.
- **Autocontenido**: el intérprete funciona con una sola dependencia externa (ANTLR runtime). Todo lo demás —matemáticas, matrices, gráficos, ML, DL— es MICELIO.
- **En español**: la sintaxis completa está en español, reduciendo la fricción cognitiva para hablantes nativos.

---

## 2. Estado Actual (v0.3.1)

### Arquitectura

```
.mice → preprocesador → ANTLR lexer/parser → AST → visitor tree-walk → resultado
             ↓
      Python primitivas (__*)
```

### Lo que funciona

| Componente | Estado |
|------------|--------|
| Sintaxis completa (variables, funciones, control de flujo, pipe, kwargs, `*args`) | ✅ Estable |
| Sistema de módulos (`importar`, rutas relativas) | ✅ Estable |
| Biblioteca estándar (12 módulos: math, matriz, ml, dl, grafico, archivo, etc.) | ✅ Completa |
| Gráficos 2D (PIL): líneas, scatter, histograma, mapas de color, estilos visuales | ✅ Completo |
| GUI (GTK): diálogos, calculadora, explorador matemático | ✅ Funcional |
| Web (HTTP server interno): rutas, plantillas, JSON API | ✅ Funcional |
| REPL con historial y comandos `:help`, `:vars` | ✅ Estable |
| VSIX extension: syntax highlighting, hover signatures, autocompletado | ✅ v0.3.0 |
| Errores pedagógicos: mensajes en español con formato visual | ✅ Estable |
| ML: regresión lineal (OLS y GD), logística, K-Means, métricas | ✅ Completo |
| DL: perceptrón multicapa, backpropagation, ReLU, sigmoid, softmax | ✅ Completo |
| Archivos: CSV, JSON, dataset loader, fast CSV con primitiva nativa | ✅ Completo |

### Lo que falta

| Característica | Prioridad | Esfuerzo |
|----------------|-----------|----------|
| Lambdas anónimas compactas (`\|x\| x * 2`) | Alta | 2-3 días |
| KNN (k-nearest neighbors) en `ml.mice` | Alta | 2-3 días |
| Autoencoder como módulo estándar (existe como ejemplo) | Media | 1-2 días |
| Precisión trigonométrica (reducción de cuadrantes en `math.mice`) | Media | 1 día |
| Casteos completos: `aFlotante()`, `aLogico()` | Media | ½ día |
| Benchmarks de rendimiento | Alta | 2 días |
| Suite de tests automatizada | Alta | 3-4 días |
| pipeline CI/CD (GitHub Actions) | Media | 1 día |

### Problemas estructurales detectados

| Problema | Impacto |
|----------|---------|
| Código ANTLR generado duplicado (`generado/` y `generado/gramatica/`) | Confusión, 236 KB basura |
| Scratch files en raíz del intérprete (`A.mice`, `B.mice`) | Contamina el árbol |
| Datos (`data.csv`, `seno.csv`) mezclados con código fuente | Desorden |
| `DOCUMENTACION_GENERAL.md` dentro de `MICELIO/` en vez de `docs/` | Inconsistente |
| `index.html` (126 KB) en raíz del proyecto | Desorden |
| Imágenes duplicadas en 4 directorios distintos (~250 KB) | Basura en VCS |
| `instalacion/` con tilde — problemas cross-platform | Riesgo |
| `stdlib/` nombre inconsistente con el resto | Estética |
| 4 pares de ejemplos con el mismo número (#18, #19, #22, #23) | Ambigüedad |
| `ejemplos/README.md` desactualizado (menciona 10 de 46+) | Engañoso |
| Sin `tests/` ni `pyproject.toml` | No instalable ni testeable |

---

## 3. Fase 1 — Consolidación y Limpieza (1-2 semanas)

### 3.1 Reestructuración de directorios

```
ANTES                                        DESPUÉS
─────                                        ───────
MICELIO/                                     (se convierte en la raíz del proyecto)
├── .gitignore                               ├── .gitignore
├── .nojekyll                                ├── .nojekyll
├── README.md                                ├── README.md
├── requirements.txt                         ├── pyproject.toml
├── index.html                               ├── Cargo.toml               (Fase 3)
├── .vscode/                                 ├── .vscode/
├── MICELIO/                                 │
│   ├── main.py                              ├── src/
│   ├── A.mice (scratch)                     │   ├── main.py
│   ├── B.mice (scratch)                     │   ├── nucleo/
│   ├── seno.csv                             │   │   ├── eval_visitor.py
│   ├── DOCUMENTACION_GENERAL.md             │   │   └── runtime.py
│   ├── gramatica/Micelio.g4                 │   └── errores/
│   ├── generado/ (DUPLICADO)                │       └── pedagogicos.py
│   ├── generado/gramatica/                  │
│   ├── nucleo/                              ├── gramatica/
│   ├── errores/                             │   └── Micelio.g4
│   ├── stdlib/                         │
│   ├── ejemplos/                            ├── generado/
│   ├── graficos/                            │   └── gramatica/          (única copia)
│   └── README.md                            │
├── docs/                                    ├── stdlib/                 (renombrado)
│   ├── DOCUMENTACION.md                     │   ├── builtins.mice
│   ├── DOCUMENTACION.html                   │   ├── math.mice
│   └── ...                                  │   └── ...
├── graficos/                                │
├── instalacion/                             ├── ejemplos/
│   ├── install-micelio.sh                   │   ├── README.md
│   ├── setup.sh                             │   ├── 01_basicos/
│   └── setup.bat                            │   ├── 02_funcional/
├── micelio-vscode/                          │   ├── 03_matematicas/
│   ├── build-vsix.sh                        │   ├── 04_ml/
│   ├── install-local.sh                     │   ├── 05_dl/
│   └── extension_unpacked/                  │   ├── 06_graficos/
├── graficos/                                │   ├── 07_gui/
│   └── (PNGs generados)                     │   ├── 08_web/
│                                             │   └── scratch/            (A.mice, B.mice, etc.)
│                                             ├── data/
│                                             │   ├── data.csv
│                                             │   └── seno.csv
│                                             ├── tests/
│                                             │   └── test_runner.py
│                                             ├── scripts/               (renombrado, sin tilde)
│                                             │   ├── install.sh
│                                             │   ├── install.bat
│                                             │   ├── build-vsix.sh
│                                             │   └── install-local.sh
│                                             ├── vscode-extension/      (renombrado)
│                                             ├── assets/                (imágenes no generadas)
│                                             ├── output/                (PNGs, .gitignored)
│                                             └── docs/
│                                                 ├── ROADMAP.md
│                                                 ├── DOCUMENTACION.md
│                                                 └── ...
```

### 3.2 Operaciones específicas

| # | Acción | Detalle |
|---|--------|---------|
| 1 | Eliminar copia stale de ANTLR | Borrar `generado/Micelio*.*` (todo fuera de `generado/gramatica/`) |
| 2 | Mover scratch files | `A.mice`, `B.mice` → `ejemplos/scratch/` |
| 3 | Mover datos | `seno.csv` → `data/` |
| 4 | Mover documentación | `DOCUMENTACION_GENERAL.md` → `docs/` |
| 5 | Mover `index.html` | → `docs/` |
| 6 | Unificar imágenes | Mover todos los PNGs a `output/`, deduplicar, añadir `output/` a `.gitignore` |
| 7 | Renombrar `instalacion/` | → `scripts/` |
| 8 | Renombrar `stdlib/` | → `stdlib/` |
| 9 | Renombrar `micelio-vscode/` | → `vscode-extension/` |
| 10 | Resolver números duplicados | #18 → #18a/18b, #19 → #19a/19b, etc. O renumerar |
| 11 | Actualizar `ejemplos/README.md` | Listar los 46+ ejemplos con descripciones |
| 12 | Crear `pyproject.toml` | `pip install -e .` instalable |
| 13 | Actualizar imports Python | `from stdlib import` → `from micelio.stdlib import` si se hace paquete |
| 14 | Crear `tests/test_runner.py` | Script que ejecuta todos los `.mice` y verifica exit code 0 |
| 15 | `.gitignore` actualizado | `output/`, `__pycache__/`, `*.pyc`, `.venv/`, `*.vsix` |

### 3.3 Nuevas funcionalidades para paridad

| Funcionalidad | Dónde | Descripción |
|---------------|-------|-------------|
| `aFlotante(x)`, `aLogico(x)` | `builtins.mice` | Casteos completos |
| `map` compacto | `builtins.mice` | Ya existe, documentar mejor |
| `KNN` (clasificación) | `ml.mice` | K-nearest neighbors con distancia euclidiana |
| `autoencoder` como módulo | `dl.mice` | Sacar de `10_autoencoder.mice` y estandarizar |
| Precisión trigonométrica | `math.mice` | Reducción de cuadrantes para seno/coseno |
| Benchmarks | `tests/benchmarks/` | Scripts que miden tiempos de ejemplos clave |

---

## 4. Fase 2 — Compilador MICELIO → Rust → LLVM (6-10 semanas)

### 4.1 Filosofía

MICELIO deja de ser "intérprete con AST" y se convierte en **lenguaje compilado con modo REPL para debug**.

```
$ micesito prog.mice         → compila a Rust + llama a rustc → ejecuta binario
$ micesito build prog.mice   → genera binario standalone
$ micesito repl              → bytecode VM liviano para probar código al vuelo
```

El usuario escribe **exclusivamente en MICELIO**. El compilador es invisible. La filosofía "Solo MICELIO" se mantiene intacta — todo algoritmo sigue visible en `.mice`, el estudiante abre `dl.mice` y ve el backprop completo.

La diferencia es que cuando el usuario corre `micesito 01_basico.mice`, el código se compila a nativo y los bucles corren a **velocidad C**.

### 4.2 Arquitectura general

```
┌─────────────────────────────────────────────────────┐
│                   micesito (binario)                 │
├─────────────────────────────────────────────────────┤
│                                                      │
│  $ micesito prog.mice       → compila + ejecuta    │
│  $ micesito build prog.mice → genera prog.exe       │
│  $ micesito repl            → REPL interactivo      │
│  $ micesito check prog.mice → solo sintaxis         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 4.3 Pipeline de compilación

```
prog.mice
    │
    ├── 1. Lexer (Rust, ~200 líneas)
    │       String → tokens: Num, Str, Ident, Keyword, ...
    │
    ├── 2. Parser recursivo (Rust, ~400 líneas)
    │       Tokens → HIR (High IR, árbol ligero)
    │       Función por cada regla gramatical
    │       Sin ANTLR, sin AST pesado
    │
    ├── 3. Análisis semántico (Rust, ~300 líneas)
    │       Resuelve variables, tipos, módulos
    │       Scope resolution, closure detection
    │
    ├── 4. Codegen (Rust, ~600 líneas)
    │       HIR → código Rust en StringBuilder
    │       → genera main.rs con stdlib inlineado
    │
    ├── 5. rustc -C opt-level=3 -C target-cpu=native
    │       → binario nativo con SIMD, loop unrolling, FMA
    │
    └── 6. Ejecución del binario
            → captura stdout/stderr, muestra resultado
```

### 4.4 Mapeo MICELIO → Rust generado

| MICELIO | Rust generado |
|---------|---------------|
| `var x = 5` | `let mut x = 5i64;` |
| `var x = 3.14` | `let mut x = 3.14f64;` |
| `const E = 2.718` | `const E: f64 = 2.718;` |
| `funcion suma(a, b) { regresa a + b }` | `fn suma(a: f64, b: f64) -> f64 { a + b }` |
| `si (x > 0) { imp x }` | `if x > 0.0 { println!("{}", x); }` |
| `mientras (x < 10) { x = x + 1 }` | `while x < 10.0 { x += 1.0; }` |
| `para i en rango(0, 10) { ... }` | `for i in 0..10 { ... }` |
| `matriz A = [[1,2],[3,4]]` | `let a = vec![vec![1.0,2.0],vec![3.0,4.0]];` |
| `a @ b` | `matriz::multiplicar(&a, &b)` |
| `x \|> f \|> g` | `g(f(x))` |
| `importar math` | `use stdlib::math;` |
| `funcion f(...args)` | `fn f(args: &[Value]) -> Value { ... }` |

### 4.5 Modo dual: compilado + bytecode VM

| Modo | Cómo | Velocidad de bucles | Para qué |
|------|------|---------------------|----------|
| **REPL** | Bytecode VM liviano (stack machine) | ~5x más lento que C | Probar ideas, aprender, debuggear |
| **Compilado** | MICELIO → Rust → LLVM -O3 | **1x C** (idéntico) | Producción, datos grandes, benchmarks |

El REPL usa un VM mínimo con ~30 opcodes. No hay AST, el parser emite bytecode directo. Comparte lexer y parser con el compilador.

```
Compartido:    lexer.rs + parser.rs → HIR
                            ↓
Modo REPL:     HIR → bytecode → stack VM
Modo compile:  HIR → codegen Rust → rustc
```

### 4.6 ¿Qué pasa con el bucle `para i en rango(1, 1000000)`?

```micelio
var suma = 0
para i en rango(1, 1000000) {
    suma = suma + i
}
imp suma
```

Se compila a:

```rust
fn main() {
    let mut suma = 0i64;
    for i in 1..1_000_000 {
        suma += i;
    }
    println!("{}", suma);
}
```

LLVM -O3 convierte eso en el mismo assembly que GCC generaría para C:

```asm
.L3:
    add     rbx, rax        # suma += i
    add     rax, 1          # i++
    cmp     rax, 1000000
    jne     .L3
```

**Cero diferencia con C.** El mismo número de instrucciones, los mismos registros, la misma velocidad.

### 4.7 Stdlib: dual nativo + `.mice` visible

El estándar library existe en dos formas:

| Módulo | En compilado | En REPL | Visible en `.mice` |
|--------|-------------|---------|-------------------|
| `math.mice` | Rust nativo (`f64::sin()`) | Rust nativo | ✅ se genera un `.mice` equivalente |
| `matriz.mice` | Rust nativo (SIMD) | Rust nativo | ✅ |
| `ml.mice` | Rust nativo | Bytecode VM | ✅ |
| `dl.mice` | Rust nativo | Bytecode VM | ✅ |
| `archivo.mice` | Rust nativo (csv, json) | Rust nativo | ✅ |
| `builtins.mice` | Rust nativo | Rust nativo | ✅ |
| `grafico.mice` | Rust nativo (image crate) | Rust nativo | ✅ |

El usuario siempre puede abrir `stdlib/ml.mice` y ver el algoritmo completo. En modo compilado, ese `.mice` no se interpreta — el compilador reconoce los patrones y usa la versión nativa. En modo `--no-opt`, el compilador genera Rust a partir del `.mice` línea por línea para que el usuario vea cómo se traduce.

### 4.8 Rendimiento esperado (compilado)

| Operación | Python puro | Python+numpy | MICELIO compilado | vs C |
|-----------|------------|-------------|-------------------|------|
| Bucle 1M sumas | 80ms | — | **~3ms** | 1x |
| Fibonacci(40) recursivo | 30s | — | **~0.5s** | 1x |
| MatMul 4×4 | 50µs | 2µs (BLAS) | **0.01µs** (desenrollado) | 1x |
| MatMul 50×50 | 5ms | 1µs (BLAS) | **2µs** (auto-vectorizado) | 1x |
| MatMul 500×500 | — | 50µs (BLAS) | **500µs** (cache tiling SIMD) | 0.1x |
| seno(1.0) Taylor 30 términos | 5µs | 0.2µs (C) | **0.05µs** (FMA nativa) | 1x |
| XOR 500 epochs (stdlib nativo) | — | — | **~5ms** | 1x |
| CSV 10K filas | 5ms | — | **~0.5ms** | 1x |

**En matrices pequeñas (< 100×100), MICELIO compilado es más rápido que numpy+BLAS** porque no tiene overhead de llamada a función externa. En matrices grandes, BLAS gana por cache tiling especializado, pero MICELIO sigue siendo competitivo (0.1-1x).

### 4.9 Dependencias del compilador

| Componente | Crate/Herramienta | Propósito |
|-----------|-------------------|-----------|
| Lexer/Parser | Rust std | Hecho a mano |
| CLI | `clap` | Argumentos de línea de comandos |
| Compilador externo | `rustc` (asume instalado) | Generar binario nativo |
| Codegen | Rust `std::fmt` | Emitir código Rust como string |
| REPL VM | Hecho a mano | Stack VM para modo interactivo |
| Stdlib math | Rust `std::f64` | `sin()`, `cos()`, `exp()`, `ln()` |
| Stdlib CSV | `csv` crate | Lectura/escritura CSV |
| Stdlib JSON | `serde_json` | Lectura/escritura JSON |
| Stdlib gráficos | `image` crate | PNG, BMP, gráficos 2D |
| Stdlib HTTP | `tiny_http` | Servidor web (hifa) |

**Nota**: el usuario debe tener `rustc` instalado para el modo compilado. El REPL no necesita `rustc`. En el futuro se puede distribuir un binario que empaquete `rustc` vía `rustup` o usar Cranelift para JIT sin `rustc`.

---

## 5. Fase 3 — Bytecode VM para REPL (4-6 semanas)

El compilador de la Fase 2 es para producción (bucles a velocidad C). Pero para el REPL y modo "probar ideas rápido" necesitamos un entorno interactivo que no espere a `rustc`.

### 5.1 Arquitectura

```
.mice → Lexer → Parser Recursivo → HIR
                                        ↓
                              ┌──────────────────┐
                              │  Modo REPL:       │
                              │  HIR → Bytecode   │
                              │        ↓          │
                              │  Stack VM         │
                              └──────────────────┘
```

El lexer y parser se comparten con el compilador. Ambos producen el mismo HIR. La diferencia está después:

| Componente | Código | Propósito |
|-----------|--------|-----------|
| `lexer.rs` | ~200 líneas | Tokenize |
| `parser.rs` | ~400 líneas | HIR |
| `compiler.rs` | ~600 líneas | HIR → código Rust |
| `vm.rs` | ~500 líneas | HIR → bytecode → ejecución |
| `repl.rs` | ~150 líneas | Loop interactivo |

### 5.2 Diseño de Bytecode (para REPL)

30 opcodes, stack-based:

```
LOAD_NIL, LOAD_BOOL, LOAD_NUM, LOAD_STR
LOAD_VAR g, STORE_VAR g
LOAD_LOCAL l, STORE_LOCAL l
ADD, SUB, MUL, DIV, POW, NEG, NOT
EQ, NE, LT, GT, LE, GE
JMP offset, JIF offset
CALL nargs, RETURN, MAKECLOSURE
NEW_LIST n, NEW_MATRIX, NEW_DICT n
GET_ITEM, SET_ITEM
FOR_INIT, FOR_NEXT
IMPORT
```

### 5.3 Stack VM

```rust
pub fn run(&mut self, bc: &Bytecode) -> Result<Value> {
    loop {
        let op = bc.code[self.ip];
        self.ip += 1;
        match op {
            LOAD_NUM => {
                let n = f64::from_le_bytes(
                    bc.code[self.ip..self.ip+8].try_into().unwrap()
                );
                self.ip += 8;
                self.push(Value::Num(n));
            }
            ADD => {
                let b = self.pop();
                let a = self.pop();
                self.push(a + b?);  // tipo-check en runtime
            }
            CALL => {
                let nargs = bc.code[self.ip] as usize;
                self.ip += 1;
                let args: Vec<Value> = self.stack.drain(
                    self.stack.len() - nargs..
                ).collect();
                let func = self.pop();
                self.call_function(func, args)?;
            }
            // ... resto de opcodes
        }
    }
}
```

### 5.4 REPL completo

```bash
$ micesito
micelio> var x = 5
=> 5
micelio> x * 10
=> 50
micelio> :vars
x = 5
=> nil
micelio> funcion cuadrado(n) { regresa n * n }
=> <funcion>
micelio> cuadrado(7)
=> 49
micelio> :help
micelio> :save prueba.mice
micelio> :exit
```

Comandos del REPL:
- `:help` — ayuda
- `:vars` — lista variables
- `:save archivo.mice` — guarda historial
- `:load archivo.mice` — carga archivo
- `:type expresion` — muestra tipo inferido
- `:time expresion` — ejecuta y muestra tiempo
- `:asm expresion` — muestra bytecode generado
- `:no-opt` — cambia a modo sin optimizaciones

### 5.5 Modo `:no-opt` (didáctico)

El usuario puede cambiar al modo "lento pero transparente":

```
micelio> :no-opt
Modo educativo activado. Todo el código se interpreta bytecode a bytecode.

micelio> var suma = 0
=> Opcodes: LOAD_NUM(0) STORE_VAR("suma")

micelio> para i en rango(1, 10) { suma = suma + i }
=> Opcodes: LOAD_NUM(1) LOAD_NUM(10) FOR_INIT ...
   (muestra el bytecode generado para cada instrucción)
```

Esto permite al estudiante **ver exactamente qué hace el VM** con su código.

---

## 6. Fase 4 — Ecosistema (paralelo a Fase 2-3)

### 6.1 LSP Server (Language Server Protocol)

- Servidor en Rust que usa el mismo lexer/parser
- Hover, go-to-definition, autocompletado, diagnósticos en tiempo real
- Reemplaza el actual `extension.js` de la VSIX

### 6.2 WASM (WebAssembly)

- Compilar el intérprete a WASM para ejecutar MICELIO en el navegador
- Demostraciones interactivas en la documentación web
- Playground online: editar y ejecutar MICELIO sin instalar nada

### 6.3 Documentación mejorada

- Sitio web generado con ejemplos interactivos (WASM)
- Tutoriales paso a paso con verificación automática
- Video-demostraciones de cada algoritmo

### 6.4 CI/CD

- GitHub Actions: test, lint, build en cada PR
- Publicación automática de VSIX en releases
- Benchmarks contra regresión

---

## 7. Metas de Rendimiento

### 7.1 Modo compilado (Fase 2)

| Operación | Python puro | Python+numpy | MICELIO compilado | vs C |
|-----------|------------|-------------|-------------------|------|
| Bucle suma 1M iter | 80ms | — | **~3ms** | 1x |
| Fibonacci(40) recursivo | 30s | — | **~0.5s** | 1x |
| MatMul 4×4 | 50µs | 2µs | **0.01µs** | 1x |
| MatMul 100×100 | — | 5µs (BLAS) | **10µs** | 1x |
| seno(1.0) Taylor | 5µs | 0.2µs | **0.05µs** | 1x |
| XOR 500 epochs (stdlib nativo) | — | — | **~5ms** | 1x |
| CSV 10K filas | 5ms | — | **~0.5ms** | 1x |
| Regresión lineal (100 datos) | 50µs | 10µs | **~1µs** | 1x |

**MICELIO compilado = velocidad C.** LLVM genera el mismo código que GCC.

### 7.2 Modo REPL (Fase 3)

| Operación | REPL (bytecode VM) | vs C | Caso de uso |
|-----------|-------------------|------|-------------|
| Bucle suma 1M iter | ~15ms | 5x más lento | Aceptable para debug |
| Llamada a función | ~50ns | 10x más lento | Rápido |
| Acceso a variable | ~10ns | 2x más lento | Muy rápido |

El REPL es lo suficientemente rápido para aprender y prototipar. Cuando se necesita velocidad, se usa el modo compilado.

### 7.3 Tabla resumen

| Fase | Velocidad vs Python puro | Velocidad vs C |
|------|--------------------------|----------------|
| Hoy (Python + AST walk) | 0.1x | 0.001x |
| Fase 2 (compilado) | **10-100x** | **1x** |
| Fase 3 (REPL VM) | 2-5x | 0.2x |

**Meta cumplida:** el bucle `para` que mencionaste corre a velocidad C en modo compilado. Para el REPL es 5x más lento que C, pero sigue siendo más rápido que Python.

---

## 8. Lo Que Hace Único a MICELIO (para portafolio)

1. **Lenguaje completo desde cero**: lexer, parser, intérprete, VM, stdlib — todo diseñado y construido por una persona.
2. **Cero dependencias de ML/DL**: cada regresión, cada backpropagation, cada métrica está escrita en el propio lenguaje.
3. **Arquitectura evolutiva**: comenzó como un DSL académico con ANTLR, está migrando a transpilador, y terminará como una VM en Rust bytecode. Cada fase está documentada y justificada.
4. **En español**: único en su clase. No hay otro lenguaje de programación en español con gráficos, ML, DL y web server incorporados.
5. **Ecosistema completo**: intérprete, REPL, stdlib (12 módulos), gráficos, GUI, web framework, VSIX extension, documentación responsive.
6. **Propósito pedagógico**: no es "otro lenguaje más". Está diseñado para que un estudiante entienda IA desde los fundamentos, sin cajas negras.

---

## Apéndice A: Benchmark Suite (propuesta)

```bash
$ micelio benchmark                      # ejecuta todo
$ micelio benchmark --matrix             # solo operaciones matriciales
$ micelio benchmark --dl                 # solo deep learning
$ micelio benchmark --json > report.json # salida para CI
```

Benchmarks planificados:

| Benchmark | Descripción | Métrica |
|-----------|-------------|---------|
| `mat_mul_4x4` | Multiplicación 4×4 | tiempo |
| `mat_mul_100x100` | Multiplicación 100×100 | tiempo |
| `mat_inv_10x10` | Inversa 10×10 | tiempo + precisión |
| `xor_train` | XOR 500 epochs | tiempo + error final |
| `kmeans_100pts` | K-Means 100 ptos, 3 clusters | tiempo + convergencia |
| `trig_precision` | seno(π/2) vs 1.0 | error absoluto |
| `csv_read_10k` | Leer 10,000 filas CSV | tiempo |
| `json_parse` | Parsear JSON 1000 entradas | tiempo |
| `fib_30` | Fibonacci recursivo n=30 | tiempo |

---

## Apéndice B: Registro de Decisiones Técnicas

| Decisión | Fecha | Contexto | Consecuencia |
|----------|-------|----------|--------------|
| ANTLR grammar + Python visitor | Inicio | Rápido prototipado | Fácil de empezar, lento en ejecución |
| Funciones matemáticas puras en MICELIO | v0.2 | Filosofía "sin cajas negras" | 10x más lento que Python math |
| Keyword arguments en grammar | v0.2.5 | Necesidad de kwargs en gráficos | Grammar más compleja pero API más natural |
| Primitiva `__leer_csv_rapido` | v0.3.1 | 10K filas CSV era inviable en MICELIO puro | Única concesión a I/O nativa |
| Bytecode VM en Rust | Planeado | Rendimiento y portabilidad | Requiere reescritura completa del runtime |
| Compilador MICELIO → Rust → LLVM | Planeado v2 | Bucles a velocidad C, filosofía "Solo MICELIO" intacta | Requiere `rustc` instalado en el sistema |
| Modo dual (REPL + compilado) | Planeado | REPL rápido para aprender, compilado para producción | Mantener dos backends |
| Stdlib dual (Rust nativo + .mice visible) | Planeado | Velocidad nativa + transparencia didáctica | El .mice es representación, no ejecución |
| Rechazar ensamblador | Planeado | Velocidad no justifica esfuerzo 100x mayor | Rust + LLVM da el mismo resultado con 1% del trabajo |
