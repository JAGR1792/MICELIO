# MICELIO

Lenguaje de programación interpretado en español, con paradigma funcional, diseñado para enseñar programación y evolucionar hacia machine learning y deep learning.

## Inicio rápido

```bash
cd MICELIO
pip install antlr4-python3-runtime
python3 main.py ejemplos/01_basico.mice
```

## Documentación

- **[docs/DOCUMENTACION.md](docs/DOCUMENTACION.md)**: documentación completa del lenguaje, biblioteca estándar, ejemplos y arquitectura.
- **`docs/`**: referencias técnicas detalladas (sintaxis, runtime, errores, extensiones).

## Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `MICELIO/main.py` | Entrada CLI y REPL |
| `MICELIO/nucleo/eval_visitor.py` | Evaluación semántica |
| `MICELIO/nucleo/runtime.py` | Entorno de ejecución y builtins |
| `MICELIO/gramatica/Micelio.g4` | Gramática ANTLR4 |
| `MICELIO/modulos_std/` | Biblioteca estándar en Micelio puro |
| `MICELIO/ejemplos/` | 31+ ejemplos ejecutables |

## Dependencias

- `antlr4-python3-runtime` (única obligatoria)
- Opcionales: Pillow, PyGObject (GTK), Flask, ImageMagick, zenity
