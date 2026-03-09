#!/usr/bin/env bash
set -euo pipefail

# Instala el comando `micelio` en:
# - ~/.local/bin (por defecto, sin sudo)
# - /usr/local/bin (si se pasa --system, requiere sudo)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN_PY="$SCRIPT_DIR/main.py"

if [[ ! -f "$MAIN_PY" ]]; then
  echo "No se encontro main.py en: $MAIN_PY" >&2
  exit 1
fi

TARGET_DIR="$HOME/.local/bin"
MODE="user"

if [[ "${1:-}" == "--system" ]]; then
  TARGET_DIR="/usr/local/bin"
  MODE="system"
fi

mkdir -p "$TARGET_DIR"
WRAPPER_PATH="$TARGET_DIR/micelio"

WRAPPER_CONTENT=$(cat <<EOF
#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="\${PYTHON_BIN:-python3}"
MAIN_PY="$MAIN_PY"

if [[ "\${1:-}" == "--help" || "\${1:-}" == "-h" ]]; then
  echo "Uso: micelio <archivo.mice>"
  echo "     micelio                # abre REPL"
  exit 0
fi

exec "\$PYTHON_BIN" "\$MAIN_PY" "\$@"
EOF
)

if [[ "$MODE" == "system" ]]; then
  echo "$WRAPPER_CONTENT" | sudo tee "$WRAPPER_PATH" >/dev/null
  sudo chmod +x "$WRAPPER_PATH"
else
  echo "$WRAPPER_CONTENT" > "$WRAPPER_PATH"
  chmod +x "$WRAPPER_PATH"
fi

echo "Instalado: $WRAPPER_PATH"

if [[ "$MODE" == "user" ]]; then
  case ":$PATH:" in
    *":$HOME/.local/bin:"*)
      echo "PATH OK: ~/.local/bin ya esta en PATH"
      ;;
    *)
      echo "IMPORTANTE: agrega ~/.local/bin a tu PATH"
      echo "Para bash, agrega esto a ~/.bashrc:"
      echo '  export PATH="$HOME/.local/bin:$PATH"'
      ;;
  esac
fi

echo "Prueba: micelio --help"
