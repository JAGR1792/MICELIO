#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)/extension_unpacked/extension"
PKG_JSON="$SRC_DIR/package.json"

if [[ ! -f "$PKG_JSON" ]]; then
  echo "No se encontro package.json en: $PKG_JSON" >&2
  exit 1
fi

PUBLISHER="$(grep -oP '"publisher"\s*:\s*"\K[^"]+' "$PKG_JSON")"
NAME="$(grep -oP '"name"\s*:\s*"\K[^"]+' "$PKG_JSON")"
VERSION="$(grep -oP '"version"\s*:\s*"\K[^"]+' "$PKG_JSON")"

if [[ -z "${PUBLISHER}" || -z "${NAME}" || -z "${VERSION}" ]]; then
  echo "No se pudo leer publisher/name/version desde package.json" >&2
  exit 1
fi

DST_ROOT="$HOME/.vscode/extensions"
DST_DIR="$DST_ROOT/${PUBLISHER}.${NAME}-${VERSION}"

mkdir -p "$DST_ROOT"
rm -rf "$DST_DIR"
cp -R "$SRC_DIR" "$DST_DIR"

echo "Instalada: ${PUBLISHER}.${NAME} ${VERSION}"
echo "Ruta: $DST_DIR"
echo "Siguiente paso: en VS Code ejecuta 'Developer: Reload Window'"
