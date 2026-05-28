#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXT_DIR="$ROOT_DIR/extension_unpacked/extension"

if [[ ! -f "$EXT_DIR/package.json" ]]; then
  echo "No se encontro package.json en $EXT_DIR" >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx no esta disponible. Instala Node.js/NPM primero." >&2
  exit 1
fi

cd "$EXT_DIR"
# Empaqueta la extension en un .vsix portable para instalar en cualquier PC.
npx --yes @vscode/vsce package --allow-missing-repository --skip-license

echo "Listo. Instala el .vsix con: code --install-extension <archivo.vsix>"
