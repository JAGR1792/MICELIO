# Release, Empaquetado e Instaladores

## Objetivo

Permitir uso de Micelio sin friccion en otras maquinas.

## Estrategia actual

### Lenguaje principal

- Ejecucion actual: `python main.py archivo.mice`
- Proxima meta: binario standalone por plataforma

### Extension VS Code

- Version actual: `0.0.4`
- Tag recomendado: `v0.0.4-vsix`
- Release esperado en GitHub: `Micelio VSIX 0.0.4`

## Flujo recomendado para release de extension

1. Actualizar version en `package.json`.
2. Generar VSIX con `./build-vsix.sh`.
3. Probar instalacion local.
4. Crear tag y release en GitHub.
5. Publicar notas de cambios.

## Instalador experimental (prueba ligera)

Disponible en:

- `Pruebas/Arimetica_estable/installer/build-linux.sh`

Genera:

- binario `calc-lite`
- paquete `calc-lite-linux.tar.gz`
- script `install.sh` para instalacion en `~/.local/bin`

## Como llevar esto a Micelio completo

1. Empaquetar `MICELIO/main.py` con PyInstaller/Nuitka.
2. Incluir recursos requeridos (`modulos_std`, etc.).
3. Generar artefactos por plataforma:
   - Linux
   - Windows
   - macOS
4. Distribuir por GitHub Releases.

## Convencion de versiones sugerida

- Lenguaje: `vX.Y.Z`
- Extension VSCode: `vX.Y.Z-vsix`
- Mensajes de commit estilo:
  - `feat(...)`
  - `fix(...)`
  - `release(...)`

## Checklist de release

- tests manuales minimos ejecutados
- README/docs actualizados
- version y changelog consistentes
- tag creado
- release publicado
