# micelio-rs

Implementación en Rust del lenguaje MICELIO (español, funcional, orientado
a la enseñanza de inteligencia artificial). Corresponde a la Fase 2 del
ROADMAP: sustitución del intérprete Python con ANTLR por un compilador
nativo mediante Rust y LLVM, manteniendo la filosofía "Solo MICELIO"
(el código `.mice` permanece visible; el compilador es transparente).

## Estado

- [x] `src/lexer.rs`: analizador léxico manual, sin ANTLR ni dependencias.
- [x] `src/main.rs`: banco de pruebas de la vuelta §4.6 con intervalos perezosos.
- [x] `docs/HISTORICO.md`: comparativa antes/después con metodología reproducible.
- [ ] `src/parser.rs`: descenso recursivo hacia HIR.
- [ ] `src/codegen.rs`: emisión de Rust y compilación con `rustc`.
- [ ] Máquina virtual de bytecode para el modo REPL (Fase 3).

## Requisitos

- Rust estable >= 1.85 (edición 2024). Verificado con `rustc 1.98.1`.

## Uso

```bash
cargo run --release          # Banco de pruebas: sumas de 10k, 1M y 10M.
cargo run --release -- --lexer
cargo test --release
cargo clippy --release
cargo fmt --check
```

## Diseño

- Núcleo sin dependencias externas para facilitar la distribución como
  binario único y eliminar el coste de arranque de ANTLR.
- Perfil `release` con `opt-level=3`, `lto=true`, `codegen-units=1`.
- Extensiones futuras (CSV, JSON, gráficos, HTTP) utilizarán crates
  dedicados según el ROADMAP (`csv`, `serde_json`, `image`, `tiny_http`).

Consulte `docs/HISTORICO.md` para la metodología y los resultados de
rendimiento.
