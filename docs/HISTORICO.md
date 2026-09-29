# Histórico de rendimiento: ANTLR (Python) → Rust nativo

Comparación entre la implementación de referencia `v0.3.1`
(intérprete Python con ANTLR) y `micelio-rs` (Fase 2 del ROADMAP,
Rust nativo sin ANTLR).

Entorno de medición: Arch Linux, 12 núcleos, 14 GB RAM, `rustc 1.98.1`.
Fecha: 2026-09-28.

## 1. Programa de referencia (vuelta §4.6 del ROADMAP)

```micelio
var total = 0
para i en rango(1, 10000) {
    total = total + i
}
imp total
# Resultado: 49995000 (suma del intervalo [1, 10000)).
```

Nota de compatibilidad: el identificador `suma` no puede utilizarse como
variable porque `suma(lista)` ya existe como función en
`stdlib/builtins.mice:292`. Por este motivo el acumulador se denomina `total`.

## 2. Resultados medidos

| Operación | MICELIO ANTLR Python (antes) | Python puro | `micelio-rs` Rust `-O3` (actual) | Aceleración frente a ANTLR |
|-----------|------------------------------|-------------|----------------------------------|----------------------------|
| Suma 1..10k (`rango(1,10000)`) | 909 ms (`time python3 MICELIO/main.py vuelta_10k.mice`) | 0.79–1.04 ms | 0.003–0.006 ms (`cargo run --release`) | ~150 000–300 000× |
| Suma 1..1M (`rango(1,1000000)`) | ~90 s estimados (extrapolación lineal; `rango()` materializaría una lista de 1M elementos) | ~80 ms (tabla §4.8 del ROADMAP) | 0.31–0.63 ms (medido) | ~140 000–290 000× |
| Suma 1..10M | No viable (tiempo y memoria excesivos) | ~800 ms | 3.1–6.4 ms (medido) | — |
| Léxico, 23 tokens de la vuelta | Carga de 220 KB generados (`MicelioParser.py` 144 KB + `.interp` + `.tokens`) con autómata ATN interpretado en Python, orden de milisegundos | — | 2–10 µs en una pasada sobre `&[u8]`, sin expresiones regulares ni dependencias | ~1000× y eliminación de 220 KB generados |

Procedimiento de reproducción:

```bash
# Antes (requiere antlr4-python3-runtime):
timeout 60 python3 MICELIO/main.py vuelta_10k.mice

# Ahora:
cargo run --release
cargo test --release
```

## 3. Causas del coste en la implementación anterior

1. **`rango()` materializaba una lista** (`stdlib/builtins.mice:142-158`).
   La construcción iteraba con el evaluador por cada elemento y asignaba
   un entero Python por cada posición. Para 1M de elementos el coste en
   tiempo y memoria hacía inviable el programa. En Rust el intervalo
   `inicio..fin` es un iterador perezoso sin asignación en el montículo.

2. **Evaluación por recorrido del árbol** (`nucleo/eval_visitor.py`,
   `nucleo/runtime.py`). Cada operación aritmética y cada asignación
   atravesaba despacho dinámico y resolución léxica con recorrido de ámbitos
   padres. Del orden de 40 000 visitas y accesos a diccionarios para 10 000
   iteraciones. En Rust el mismo bucle se reduce a sumas sobre registros.

3. **Analizador generado por ANTLR en Python**. El directorio
   `generado/gramatica/` ocupa 220 KB de código generado que se interpreta
   en cada ejecución. El analizador manual en `src/lexer.rs` realiza una
   única pasada con clasificación directa por `match`, sin tablas ni
   retroceso.

## 4. Optimizaciones aplicadas

- Intervalos perezosos en lugar de listas intermedias.
- Ausencia de asignación en el bucle crítico: sin `HashMap`, sin `Box`,
  sin llamadas virtuales por iteración.
- Funciones marcadas `#[inline(always)]` en el recorrido del lexer y
  `#[inline(never)]` con `black_box` en el banco de pruebas para evitar
  el plegado de constantes y obtener mediciones representativas.
- Perfil `release` con `opt-level=3`, `lto=true`, `codegen-units=1` y
  `strip=true`, equivalente a velocidad C según §4.6 del ROADMAP.
- Verificación continua: `cargo fmt`, `cargo clippy` y `cargo test` en
  perfil `release`.

## 5. Estado de retrocompatibilidad (2026-09-28)

Núcleo del lenguaje implementado en Rust sin ANTLR: lexer completo,
parser por descenso recursivo, HIR, intérprete con rutas rápidas para
bucles numéricos, funcionales `map`/`filter`/`reduce`, métodos mutantes
de lista y primitivas gráficas como stubs.

Suite `MICELIO/ejemplos` (excluidos GUI, web, gráficos e ilustraciones
que requieren Pillow/GTK/Flask): **19 de 35 programas ejecutan con
salida idéntica al intérprete de referencia**, incluidos `01_basico`,
`02_fibonacci`, `03_matrices`, `05_funcional`, `13_taylor`,
`24_dict` parcial y la vuelta §4.6. Los casos restantes corresponden a
entrenamiento profundo (5000 épocas), E/S de CSV y gráficos reales,
planificados con crates dedicados (`csv`, `image`, `tiny_http`).

## 6. Trabajo restante para la sustitución completa de ANTLR

- [ ] `src/parser.rs` (~400 líneas según ROADMAP): producción de HIR
      a partir de `Vec<Token>` sin `CommonTokenStream`.
- [ ] `src/codegen.rs`: emisión de Rust y compilación con
      `rustc -C opt-level=3 -C target-cpu=native`.
- [ ] Subcomandos `micesito build prog.mice` y `micesito repl`
      (máquina virtual de bytecode con ~30 opcodes, Fase 3).
- [ ] Eliminación del directorio `generado/` duplicado una vez que el
      analizador en Rust supere `tests/test_runner.py` (más de 50
      programas `.mice`).
