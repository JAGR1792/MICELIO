# Extension VS Code de Micelio

## Ubicacion

- `micelio-vscode/extension_unpacked/extension/`

## Que incluye

- Lenguaje `micelio` para archivos `.mice` y `.micelio`
- Resaltado de sintaxis
- Configuracion de comentarios y pares
- Snippets de pipeline
- Continuacion automatica de `|>` con Enter

## Archivos principales

- `package.json`: contributes de lenguaje, comandos y keybindings.
- `language-configuration.json`: reglas de pares y Enter rules.
- `syntaxes/micelio.tmLanguage.json`: gramatica de resaltado.
- `snippets/micelio.code-snippets`: snippets utiles.
- `extension.js`: comportamiento de Enter para auto-pipe.

## Uso en desarrollo

1. Abrir carpeta de extension en VS Code.
2. Ejecutar `F5` (Extension Development Host).
3. Abrir archivo `.mice` en la ventana nueva.

## Instalacion en otra PC

### Opcion A: VSIX (recomendada)

```bash
cd micelio-vscode
./build-vsix.sh
code --install-extension micelio-syntax-0.0.4.vsix
```

### Opcion B: install local rapido

```bash
cd micelio-vscode
./install-local.sh
```

Despues de instalar:

1. `Developer: Reload Window`
2. Confirmar lenguaje `Micelio` en la barra de estado

## Troubleshooting rapido

- Si Enter no auto-inserta `|>`, verifica:
  - que el archivo este en modo `Micelio`
  - que extension version activa sea `0.0.4`
  - recargar ventana de VS Code
