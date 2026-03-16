# Estructura del proyecto

Esta guia explica la nueva organizacion del repo y que se maneja en cada carpeta.

## Vista rapida

- `MICELIO/`: implementacion del lenguaje.
- `docs/`: documentacion tecnica y guias.
- `micelio-vscode/`: extension de VS Code.
- `Pruebas/`: prototipos y experimentos historicos.

## Carpeta `MICELIO/`

- `MICELIO/main.py`
  - Punto de entrada CLI/REPL.
  - Preprocesa azucar sintactico (`leer a,b`, asignaciones multiples, compuestos).
  - Arma lexer/parser y delega ejecucion al visitor.

- `MICELIO/gramatica/`
  - Fuente de verdad de sintaxis ANTLR.
  - Archivo principal: `MICELIO/gramatica/Micelio.g4`.

- `MICELIO/generado/`
  - Codigo generado por ANTLR desde la gramatica.
  - Incluye lexer/parser/listener/visitor y archivos `.tokens`/`.interp`.
  - No se edita a mano; se regenera desde `MICELIO/gramatica/Micelio.g4`.

- `MICELIO/nucleo/`
  - Logica de ejecucion del lenguaje.
  - `eval_visitor.py`: semantica de sentencias/expresiones.
  - `runtime.py`: entorno, builtins, tipos y utilidades.

- `MICELIO/errores/`
  - Manejo de errores pedagogicos.
  - `pedagogicos.py`: listeners, formato y sugerencias de correccion.

- `MICELIO/modulos_std/`
  - Biblioteca estandar escrita en `.mice`.
  - Modulos como `math.mice`, `gui.mice`, `hifa.mice`, etc.

- `MICELIO/hifa_demo_test/`
  - Demo web de ejemplo para framework Hifa.

## Carpeta `docs/`

- `docs/README.md`: indice general.
- `docs/lenguaje.md`: sintaxis, semantica y ejemplos.
- `docs/runtime.md`: detalles del runtime y arquitectura de ejecucion.
- `docs/errores-pedagogicos.md`: formato de errores y catalogo.
- `docs/vscode-extension.md`: extension y flujo de desarrollo.
- `docs/release.md`: versionado, empaquetado e instalacion.
- `docs/estructura-proyecto.md`: este documento.

## Carpeta `micelio-vscode/`

- `micelio-vscode/extension_unpacked/extension/`
  - Codigo fuente de la extension (gramatica TextMate, snippets, comandos).
- `micelio-vscode/build-vsix.sh`
  - Genera paquete `.vsix`.
- `micelio-vscode/install-local.sh`
  - Instalacion local rapida de extension.

## Regla de mantenimiento recomendada

1. Editar sintaxis solo en `MICELIO/gramatica/Micelio.g4`.
2. Regenerar ANTLR hacia `MICELIO/generado/`.
3. Ajustar semantica en `MICELIO/nucleo/`.
4. Ajustar mensajes de error en `MICELIO/errores/`.
5. Actualizar docs (`docs/`) cuando cambie estructura o comportamiento.
