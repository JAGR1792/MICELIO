# Micelio Syntax (Local)

This folder contains a local VS Code language extension for Micelio.

## What it provides

- File extensions: `.mice`, `.micelio`
- Line comments with `#`
- Bracket and quote auto-closing
- Syntax highlighting for:
  - Keywords (`var`, `const`, `funcion`, `si`, `mientras`, etc.)
  - Builtins (`imp`, `leer`, `map`, `filter`, `reduce`, conversiones y bases)
  - Booleans and null (`verdadero`, `falso`, `nulo`)
  - Strings, numbers, operators, and function names
- Snippets for pipe composition (`|>`):
  - `pipe`
  - `pipe_map`
  - `pipe_filter`
  - `pipe_reduce`
  - `pipe_chain`
- Auto pipe continuation on `Enter`:
  - If a line starts with `|>` (with optional indentation), pressing `Enter` inserts a new line with `|> ` preserving indentation.

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

## Use on another PC

Option A (recommended, portable `.vsix`):

```bash
cd micelio-vscode
./build-vsix.sh
code --install-extension micelio-syntax-0.0.5.vsix
```

Option B (quick local install from folder):

```bash
cd micelio-vscode
./install-local.sh
```

After either option, run `Developer: Reload Window` in VS Code.

## Enter auto-pipe example

Input:

```mice
datos
  |> map(funcion (x) { regresa x * 2 })
```

Cursor at end of second line + `Enter` produces:

```mice
datos
  |> map(funcion (x) { regresa x * 2 })
  |> 
```
