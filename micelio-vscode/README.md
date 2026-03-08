# Micelio Syntax (Local)

This folder contains a local VS Code language extension for Micelio.

## What it provides

- File extensions: `.mice`, `.micelio`
- Line comments with `#`
- Bracket and quote auto-closing
- Syntax highlighting for:
  - Keywords (`var`, `const`, `funcion`, `si`, `mientras`, etc.)
  - Builtins (`imp`, `leer`, `map`, `filter`, `reduce`, etc.)
  - Booleans and null (`verdadero`, `falso`, `nulo`)
  - Strings, numbers, operators, and function names

## How to use locally

1. Open this folder in VS Code.
2. Press `F5` to launch an Extension Development Host.
3. Open a `.mice` file in the new window.

To package/install permanently, run:

```bash
npm i -g vsce
cd micelio-vscode
vsce package
```

Then install the generated `.vsix` from VS Code: `Extensions -> ... -> Install from VSIX`.
