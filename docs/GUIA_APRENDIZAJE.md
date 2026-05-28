# Guía de Aprendizaje — MICELIO en Rust

**De cero a construir un compilador de lenguaje completo que corre a velocidad C.**

Esta guía asume que partes de **cero absoluto** en Rust y en compiladores. Cada bloque lista qué aprender, cuánto tiempo toma, recursos concretos (gratis), y qué vas a construir al final.

---

## Bloque 0 — Fundamentos (opcional si ya sabes programar)

Si nunca has programado. Si ya sabes Python/C/etc, salta directo a Bloque 1.

| Concepto | Tiempo | Recurso |
|----------|--------|---------|
| Qué es un programa, variable, función | 1 día | [CS50x](https://cs50.harvard.edu/x/) semana 0-2 |
| Algoritmos básicos: loops, condicionales | 3 días | CS50x semana 2-3 |
| Estructuras de datos: listas, diccionarios | 2 días | CS50x semana 4-5 |
| Memoria: stack vs heap, punteros | 2 días | CS50x semana 5 |

**Total:** ~1 semana (puedes hacerlo paralelo al Bloque 1)

---

## Bloque 1 — Rust Básico

**Objetivo:** leer y escribir Rust simple. Entender ownership, borrowing, structs, enums.

| Tema | Tiempo | Recurso | Proyecto |
|------|--------|---------|----------|
| Instalación: `rustup`, `cargo`, `rustc` | 1 hora | [rustup.rs](https://rustup.rs/) | `cargo new hola_mundo` |
| Variables, tipos, funciones | 2 días | [Rust Book cap 1-4](https://doc.rust-lang.org/book/) | Calculadora CLI |
| Ownership, borrowing, lifetimes | 5 días | Rust Book cap 4-5 | Simular un `String` |
| Structs, enums, pattern matching | 3 días | Rust Book cap 6, 10 | `enum Value` + `match` |
| `Option`, `Result`, error handling | 2 días | Rust Book cap 9 | `Result<T, E>` chain |
| Vectores, `HashMap`, colecciones | 2 días | Rust Book cap 8 | Contador de palabras |
| Traits, genéricos | 3 días | Rust Book cap 10 | `trait Display` para tipos |
| Closures, iterators | 2 días | Rust Book cap 13 | Pipeline funcional |
| Módulos, `use`, `pub`, organización | 1 día | Rust Book cap 7 | Proyecto multi-archivo |
| Testing en Rust | 1 día | Rust Book cap 11 | Tests unitarios |

**Proyecto final del bloque:** Calculadora de expresiones aritméticas con memoria:
- `2 + 3 * 4` → 14
- `ans * 2` → 28 (memoria)
- Usa `enum Token { Num(f64), Plus, Minus, Mul, Div }`
- Usa `enum Expr { BinOp(Box<Expr>, Op, Box<Expr>), Num(f64) }`
- Implementa parser recursivo descendente

**Total:** ~3 semanas  
**Recursos extra:** [Rust by Example](https://doc.rust-lang.org/rust-by-example/), [Rustlings](https://github.com/rust-lang/rustlings)

---

## Bloque 2 — Rust Avanzado

**Objetivo:** dominar los patrones que usarás en el compilador.

| Tema | Tiempo | Recurso | Proyecto |
|------|--------|---------|----------|
| `std::cell::RefCell`, `Rc<T>`, `Arc<T>` | 3 días | Rust Book cap 15 | Árbol con referencias compartidas |
| Iterators personalizados | 2 días | Rust Book cap 13 | `struct TokenStream` |
| Macros (declarativas) | 2 días | Rust Book cap 19.5 | `vec![]` personalizado |
| `unsafe` y FFI | 2 días | [Rust FFI guide](https://doc.rust-lang.org/nomicon/ffi.html) | Llamar `sin()` de C |
| CLI apps con `clap` | 1 día | [clap docs](https://docs.rs/clap/) | `micesito --help` |
| `serde` para JSON | 1 día | [serde.rs](https://serde.rs/) | Parsear config.json |
| Manejo de archivos (`std::fs`, `Path`) | 1 día | Rust Book cap 12 | Leer `.mice` de disco |
| `std::process::Command` | 1 día | [docs](https://doc.rust-lang.org/std/process/) | Llamar `rustc` desde tu app |
| Benchmarking (`criterion`) | 1 día | [criterion.rs](https://docs.rs/criterion/) | Medir velocidad del parser |
| Perfilado (`perf`, `flamegraph`) | 2 días | [The Rust Performance Book](https://nnethercote.github.io/perf-book/) | Encontrar bottlenecks |

**Proyecto final del bloque:** Shell CLI que ejecuta comandos externos:
- `run echo "hola"` → ejecuta comando
- `pipe ls \| grep .rs` → pipe entre procesos
- Mide tiempo de ejecución

**Total:** ~2 semanas

---

## Bloque 3 — Teoría de Compiladores (qué necesitas saber)

**Objetivo:** entender cómo funcionan los lenguajes por dentro. No es necesario ser experto — solo lo práctico para MICELIO.

| Tema | Tiempo | Recurso | Proyecto |
|------|--------|---------|----------|
| Qué es un lexer (tokenizer) | 2 días | [Crafting Interpreters cap 4](https://craftinginterpreters.com/scanning.html) | Lexer de JSON |
| Expresiones regulares y DFA | 1 día | [RegexOne](https://regexone.com/) | Reconocer números |
| Qué es un parser | 3 días | [Crafting Interpreters cap 6](https://craftinginterpreters.com/parsing-expressions.html) (Pratt parsing) | Parser de expresión |
| Recursive descent parser | 3 días | [Crafting Interpreters cap 6](https://craftinginterpreters.com/parsing-expressions.html) | Parser de calculadora |
| AST vs HIR vs IR | 1 día | [Crafting Interpreters cap 5](https://craftinginterpreters.com/representing-code.html) | Representar código |
| Análisis semántico (scope, tipos) | 3 días | [Crafting Interpreters cap 7](https://craftinginterpreters.com/evaluating.html) | Resolver variables |
| Bytecode vs árbol | 2 días | [Crafting Interpreters cap 14-15](https://craftinginterpreters.com/chunks-of-bytecode.html) | VM de bytecode |
| Code generation (emitir código) | 3 días | [Crafting Interpreters cap 17](https://craftinginterpreters.com/compiling-expressions.html) | MICELIO → Rust |
| LLVM IR básico (saber qué es) | 1 día | [LLVM Tutorial](https://llvm.org/docs/tutorial/) | Leer IR, no escribir |

**Recurso principal:** [Crafting Interpreters](https://craftinginterpreters.com/) — el mejor libro gratis sobre compiladores. Léelo completo. Aunque el autor usa Java y C, los conceptos son idénticos.

**Proyecto final del bloque:** Escribe un mini-lenguaje "Tiny" en Rust que:
- Lexer: `let x = 5 + 3; print x;`
- Parser: recursive descent a AST
- Codegen: genera código Rust que LLVM compila

**Total:** ~4 semanas (leyendo Crafting Interpreters + implementando en Rust)

---

## Bloque 4 — Construir MICELIO: Lexer + Parser (Semanas 1-2)

**Objetivo:** implementar el frontend completo del compilador MICELIO en Rust.

### Semana 1 — Lexer

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | Definir `enum Token` con todos los tokens de MICELIO | `src/lexer.rs` |
| 2 | Implementar `Lexer::new(input: &str)` | `src/lexer.rs` |
| 3 | `next_token()` — scan de números, strings, identificadores | `src/lexer.rs` |
| 4 | Keywords (`funcion`, `si`, `sino`, `para`, `mientras`, `regresa`, etc.) | `src/lexer.rs` |
| 5 | Operadores (`+`, `-`, `*`, `/`, `**`, `@`, `\|>`, `..`, etc.) | `src/lexer.rs` |
| 6 | Comentarios `#`, saltos de línea, ignorar whitespace | `src/lexer.rs` |
| 7 | Tests del lexer — tokenizar ejemplos reales de MICELIO | `src/lexer.rs` |

**Referencia gramatical:** la gramática ANTLR actual está en `gramatica/Micelio.g4`. Úsala como especificación, pero implementa el lexer a mano (sin ANTLR).

### Semana 2 — Parser

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | Definir `enum HIR` (High IR) — versión ligera del AST | `src/hir.rs` |
| 2 | `Parser::new(tokens)` — recursive descent básico | `src/parser.rs` |
| 3 | Parsear expresiones: literales, binarias, unarias, pipe | `src/parser.rs` |
| 4 | Parsear statements: `var`, `const`, `funcion`, `regresa`, `imp` | `src/parser.rs` |
| 5 | Parsear control de flujo: `si`, `mientras`, `para`, `segun` | `src/parser.rs` |
| 6 | Parsear funciones con `*args`, `**kwargs`, closures anónimas | `src/parser.rs` |
| 7 | Tests del parser — parsear ejemplos reales, verificar HIR | `src/parser.rs` |

**Referencia:** `nucleo/eval_visitor.py` tiene la semántica completa de cada constructo. Úsalo como especificación de comportamiento.

**Nombres clave:**
- Robert Nystrom (autor de Crafting Interpreters)
- Vaughan Pratt (Pratt parsing)
- ANTLR (Terence Parr) — tu grammar actual como referencia

---

## Bloque 5 — Construir MICELIO: Análisis Semántico (Semanas 3-4)

**Objetivo:** resolver variables, tipos, módulos.

### Semana 3 — Scope y resolución de variables

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `struct Scope` con cadena de ámbitos | `src/semantic.rs` |
| 2 | Pase de resolución: `Resolve(HIR) -> ResolvedHIR` | `src/semantic.rs` |
| 3 | Detectar variables no definidas, usos antes de definición | `src/semantic.rs` |
| 4 | Detectar constantes re-asignadas | `src/semantic.rs` |
| 5 | Detectar closures con captura de variables | `src/semantic.rs` |
| 6 | Sistema de módulos: `importar`, resolución de rutas | `src/semantic.rs` |
| 7 | Tests de resolución semántica | `src/semantic.rs` |

### Semana 4 — Tipos (opcional, inferencia básica)

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `enum Type { Num, Str, Bool, List, Matriz, Func, ... }` | `src/types.rs` |
| 2 | Inferencia de tipos en literales | `src/types.rs` |
| 3 | Type-checking en operaciones binarias | `src/types.rs` |
| 4 | Type-checking en llamadas a función | `src/types.rs` |
| 5 | Errores de tipo en español | `src/types.rs` |
| 6-7 | Tests de type-checking | `src/types.rs` |

**Nombres clave:**
- Benjamin C. Pierce (Types and Programming Languages)
- Hindley-Milner type inference (el algoritmo W)

---

## Bloque 6 — Construir MICELIO: Codegen (Semanas 5-7)

**Objetivo:** el corazón del proyecto — generar código Rust desde MICELIO.

### Semana 5 — Codegen básico

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `struct Codegen { buffer: String }` | `src/codegen.rs` |
| 2 | Emitir `fn main()` wrapper | `src/codegen.rs` |
| 3 | Emitir variables: `var x = 5` → `let mut x = 5i64` | `src/codegen.rs` |
| 4 | Emitir expresiones aritméticas | `src/codegen.rs` |
| 5 | Emitir `si`, `mientras`, `para` | `src/codegen.rs` |
| 6 | Emitir funciones | `src/codegen.rs` |
| 7 | Emitir `imp` → `println!` | `src/codegen.rs` |

### Semana 6 — Codegen avanzado

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | Emitir listas, diccionarios, sets | `src/codegen.rs` |
| 2 | Emitir matrices: `a @ b` → `fn mat_mul(a, b)` | `src/codegen.rs` |
| 3 | Emitir closures (captura por entorno) | `src/codegen.rs` |
| 4 | Emitir pipe operator: `x \|> f \|> g` → `g(f(x))` | `src/codegen.rs` |
| 5 | Emitir módulos: `importar math` → `use stdlib::math` | `src/codegen.rs` |
| 6 | Manejo de `*args` y `**kwargs` | `src/codegen.rs` |
| 7 | Tests de codegen — generar Rust, compilar y ejecutar | `src/codegen.rs` |

### Semana 7 — Stdlib nativo en Rust

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `src/stdlib/mod.rs` — registro de funciones nativas | `src/stdlib/mod.rs` |
| 2 | `math` — `f64::sin()`, `cos()`, `exp()`, `ln()`, etc. | `src/stdlib/math.rs` |
| 3 | `matriz` — multiplicación, inversa, determinante, SIMD | `src/stdlib/matriz.rs` |
| 4 | `archivo` — CSV, JSON, lectura/escritura | `src/stdlib/archivo.rs` |
| 5 | `grafico` — PIL-equivalent con `image` crate | `src/stdlib/grafico.rs` |
| 6 | `ml` — regresión lineal, K-Means, métricas | `src/stdlib/ml.rs` |
| 7 | `dl` — perceptrón multicapa, backprop | `src/stdlib/dl.rs` |

**Nombres clave:**
- LLVM (Chris Lattner)
- `cargo expand` (ver macros expandidas)
- `rustc --emit llvm-ir` (ver IR generado)

---

## Bloque 7 — Construir MICELIO: Compilación + CLI (Semanas 8-9)

**Objetivo:** unir todo y crear el binario `micesito`.

### Semana 8 — Pipeline de compilación

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `Compiler::compile(input: &str) -> Result<()>` | `src/compiler.rs` |
| 2 | Escribir archivo `.rs` temporal | `src/compiler.rs` |
| 3 | Llamar `rustc` vía `std::process::Command` | `src/compiler.rs` |
| 4 | Capturar errores de `rustc` y traducirlos a español | `src/compiler.rs` |
| 5 | Ejecutar el binario generado y capturar output | `src/compiler.rs` |
| 6 | Cache: no re-compilar si el .mice no cambió | `src/compiler.rs` |
| 7 | `--tree`, `--tokens`, `--rust`, `--asm` flags | `src/compiler.rs` |

### Semana 9 — CLI con `clap`

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `clap` CLI: `micesito [FLAGS] <archivo>` | `src/main.rs` |
| 2 | `micesito repl` — modo interactivo | `src/repl.rs` |
| 3 | `micesito build archivo.mice` — solo generar binario | `src/main.rs` |
| 4 | `micesito check archivo.mice` — solo chequear sintaxis | `src/main.rs` |
| 5 | `micesito run archivo.mice` — compilar y ejecutar | `src/main.rs` |
| 6 | Colores y formato en la terminal | `src/main.rs` |
| 7 | Testing de integración — ejecutar ejemplos reales | `tests/` |

---

## Bloque 8 — Construir MICELIO: Bytecode VM para REPL (Semanas 10-11)

**Objetivo:** que `micesito repl` funcione sin esperar a `rustc`.

### Semana 10 — Bytecode

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | `enum Opcode` con 30 instrucciones | `src/vm/opcode.rs` |
| 2 | `struct Bytecode { code: Vec<u8>, consts: Vec<Value> }` | `src/vm/bytecode.rs` |
| 3 | Compilar HIR a bytecode | `src/vm/compiler.rs` |
| 4 | `struct VM { stack, ip, globals, frames }` | `src/vm/vm.rs` |
| 5 | Dispatch loop principal | `src/vm/vm.rs` |
| 6 | Valores: `enum Value { Num, Str, List, Matriz, Func, ... }` | `src/vm/value.rs` |
| 7 | Pruebas del VM con programas simples | `tests/vm_test.rs` |

### Semana 11 — REPL completo

| Día | Qué hacer | Archivo |
|-----|-----------|---------|
| 1 | Loop REPL: `read → compile → execute → print` | `src/repl.rs` |
| 2 | Comandos `:help`, `:vars`, `:save`, `:load` | `src/repl.rs` |
| 3 | Comando `:time` — medir tiempo de ejecución | `src/repl.rs` |
| 4 | Comando `:asm` — mostrar bytecode generado | `src/repl.rs` |
| 5 | Modo `:no-opt` — mostrar cada paso | `src/repl.rs` |
| 6 | Historial, tab completion | `src/repl.rs` |
| 7 | Pruebas del REPL | `tests/repl_test.rs` |

---

## Bloque 9 — Optimización y SIMD (Semana 12+)

**Objetivo:** hacer que MICELIO compilado sea competitivo con BLAS en el dominio educativo.

| Tema | Tiempo | Recurso |
|------|--------|---------|
| `perf` profiling en Linux | 2 días | [perf wiki](https://perf.wiki.kernel.org/) |
| `cargo flamegraph` | 1 día | [flamegraph](https://github.com/flamegraph-rs/flamegraph) |
| LLVM optimization passes | 3 días | [LLVM docs](https://llvm.org/docs/Passes.html) |
| Rust `core::simd` (nightly) | 3 días | [Rust SIMD book](https://rust-lang.github.io/packed_simd/) |
| Cache tiling para matmul | 3 días | [What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) |
| Loop unrolling patterns | 1 día | [LLVM loop optimizations](https://llvm.org/docs/LoopTerminology.html) |
| FMA (fused multiply-add) | 1 día | `mul_add` en Rust |
| `black_box()` para benchmarks | 1 día | [criterion.rs](https://docs.rs/criterion/) |

**Proyecto:** benchmark MICELIO compilado vs numpy para cada operación.

---

## Resumen de tiempos

| Bloque | Semanas | Título |
|--------|---------|--------|
| 0 | 1 (opcional) | Fundamentos |
| 1 | 3 | Rust básico |
| 2 | 2 | Rust avanzado |
| 3 | 4 | Teoría de compiladores |
| 4 | 2 | MICELIO: Lexer + Parser |
| 5 | 2 | MICELIO: Semántica |
| 6 | 3 | MICELIO: Codegen + Stdlib |
| 7 | 2 | MICELIO: Compilador + CLI |
| 8 | 2 | MICELIO: Bytecode VM + REPL |
| 9 | 1+ | Optimización SIMD |

**Total estimado:** ~22 semanas (~5 meses) a tiempo completo.  
**Ruta acelerada** (si ya sabes Rust): ~12 semanas (~3 meses).

---

## Recursos clave — guarda estos enlaces

| Recurso | Para qué |
|---------|----------|
| [doc.rust-lang.org/book/](https://doc.rust-lang.org/book/) | Aprender Rust |
| [craftinginterpreters.com](https://craftinginterpreters.com/) | Aprender compiladores |
| [rust-lang.github.io/packed_simd/](https://rust-lang.github.io/packed_simd/) | SIMD en Rust |
| [nnethercote.github.io/perf-book/](https://nnethercote.github.io/perf-book/) | Optimización Rust |
| [rust-lang.org/learn](https://www.rust-lang.org/learn) | Todos los recursos Rust |
| [llvm.org/docs/tutorial/](https://llvm.org/docs/tutorial/) | LLVM kaleidoscope tutorial |
| [serde.rs](https://serde.rs/) | JSON en Rust |
| [docs.rs/clap/](https://docs.rs/clap/) | CLI argument parser |
| [docs.rs/criterion/](https://docs.rs/criterion/) | Benchmarks |
| [regexone.com](https://regexone.com/) | Aprender regex |
| [cs50.harvard.edu/x/](https://cs50.harvard.edu/x/) | Fundamentos CS (gratis, Harvard) |

---

## ¿Qué hacer cada día?

**Rutina diaria recomendada:**

```
1 hora  → teoría (leer Crafting Interpreters, Rust Book, docs)
2 horas → implementar (escribir código del compilador)
1 hora  → refactorizar + tests (que todo lo anterior funcione)
```

**Cada viernes:** corre todos los ejemplos de `ejemplos/` con tu compilador. Si algo falla, lo arreglas antes de avanzar.

**Cada domingo:** lee sobre optimización (SIMD, cache, perfilado) aunque no lo implementes aún. El conocimiento se asienta solo.

---

## Notas finales

1. **No memorices.** Cada concepto lo entiendes cuando lo implementas. Si no sabes Rust ownership, escríbelo mal hasta que el compilador te obligue a corregirlo. Eso es aprender.

2. **Usa el compilador de Rust como maestro.** `rustc` da errores muy precisos. Cada error que te da es una lección.

3. **Prueba todo.** Cada función del compilador debe tener tests. Sin tests, cuando algo se rompa no sabrás qué fue.

4. **Cuando te atores:** busca el error específico en Google/Stack Overflow. Si no encuentras, pregúntale al profe o a la IA. Pero intenta resolverlo solo primero.

5. **Disfruta el proceso.** Vas a construir un lenguaje de programación desde cero que corre a velocidad C. Eso es algo que la mayoría de programadores nunca hace en su vida.
