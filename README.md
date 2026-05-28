# MICELIO

Lenguaje de programación en español, con paradigma funcional, diseñado para enseñar fundamentos de IA desde cero. Sin dependencias externas de ML/DL.

## Inicio rápido

```bash
pip install antlr4-python3-runtime
python3 MICELIO/main.py MICELIO/ejemplos/01_basico.mice
```

## Documentación

- **[docs/DOCUMENTACION.md](docs/DOCUMENTACION.md)** — documentación completa del lenguaje
- **[docs/ROADMAP.md](docs/ROADMAP.md)** — plan de futuro (compilador Rust, bytecode VM)
- **[docs/GUIA_APRENDIZAJE.md](docs/GUIA_APRENDIZAJE.md)** — ruta de aprendizaje desde cero

## Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `MICELIO/main.py` | Entrada CLI y REPL |
| `MICELIO/nucleo/eval_visitor.py` | Evaluación semántica |
| `MICELIO/nucleo/runtime.py` | Entorno de ejecución y builtins |
| `MICELIO/gramatica/Micelio.g4` | Gramática ANTLR4 |
| `MICELIO/stdlib/` | Biblioteca estándar (12 módulos en MICELIO puro) |
| `MICELIO/ejemplos/` | 50+ ejemplos ejecutables |
| `data/` | Datos de ejemplo (CSV) |
| `tests/test_runner.py` | Ejecuta todos los ejemplos y verifica |

## Dependencias

- `antlr4-python3-runtime` (única obligatoria)
- Opcionales: Pillow (gráficos), PyGObject (GUI), Flask (web)
