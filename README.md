# micelio-rs

Implementación en Rust del lenguaje MICELIO (español, funcional, orientado
a la enseñanza de inteligencia artificial). Corresponde a la Fase 2 del
ROADMAP: sustitución del intérprete Python con ANTLR por un intérprete
nativo de alto rendimiento en Rust, manteniendo la filosofía "Solo MICELIO"
(el código `.mice` permanece visible; el compilador es transparente).

## Estado

- [x] `src/lexer.rs`: analizador léxico manual, sin ANTLR ni dependencias.
- [x] `src/parser.rs`: descenso recursivo → HIR completo según `Micelio.g4`.
- [x] `src/interp.rs`: intérprete con rutas rápidas para bucles numéricos.
- [x] `src/valor.rs`: valores con semántica por referencia (Rc<RefCell>).
- [x] `src/grafico.rs`: motor de gráficos real (crate `image`, PNG 800x500).
- [x] `src/main.rs`: CLI con REPL interactivo y banco de pruebas.
- [x] `docs/HISTORICO.md`: comparativa antes/después con metodología reproducible.
- [x] **51/51 ejemplos** de `MICELIO/ejemplos` ejecutan con salida idéntica.
- [ ] Fase 3: compilador MICELIO → Rust → LLVM (`codegen.rs`).
- [ ] Fase 4: GUI real (GTK), web real (tiny_http), JSON real (serde_json ✅).

## Retrocompatibilidad

| Ejemplos | Estado |
|---|---|
| 51/51 `.mice` (sin GUI/web/gráficos nativos) | ✅ Idénticos |
| Gráficos (22b, etc.) | ✅ PNG real 800x500 |
| GUI (30) | ✅ Stubs (estado de tema) |
| Web/Hifa (31) | ✅ Stubs (almacenamiento de rutas) |
| JSON | ✅ serde_json real |
| REPL | ✅ Interactivo con `:ayuda`, `:vars`, `:cargar`, `:guardar` |

## Rendimiento

| Operación | ANTLR Python (antes) | Rust -O3 (ahora) | Aceleración |
|---|---|---|---|
| Suma 1..10k | 909 ms | 0.006 ms | ~150.000x |
| Suma 1..1M | ~90 s (estimado) | 0.645 ms | ~140.000x |
| Suma 1..10M | imposible | 6.6 ms | — |
| Lexer 28 tokens | 220 KB generados | 11 µs, cero deps | ~1000x |

## Requisitos

- Rust estable >= 1.85 (edición 2024). Verificado con `rustc 1.98.1`.

## Uso

```bash
cargo run --release          # Banco de pruebas
cargo run --release -- --lexer
micesito programa.mice       # Ejecuta un programa
micesito                     # Modo REPL interactivo
cargo test --release
cargo clippy --release
```

## Diseño

- Núcleo con dependencias mínimas (`image`, `serde_json`, `tiny_http` para extensiones).
- Perfil `release` con `opt-level=3`, `lto=true`, `codegen-units=1`.
- 8 tests de regresión, clippy limpio.

Consulte `docs/HISTORICO.md` para la metodología y los resultados de
rendimiento.
