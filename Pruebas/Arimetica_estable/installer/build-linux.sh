#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$ROOT_DIR"

echo "[1/4] Installing build dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip pyinstaller antlr4-python3-runtime

echo "[2/4] Building single-file binary..."
rm -rf build dist release
"$PYTHON_BIN" -m PyInstaller --onefile --name calc-lite --clean main.py

echo "[3/4] Creating installer payload..."
mkdir -p release/calc-lite-linux
cp dist/calc-lite release/calc-lite-linux/calc-lite
cat > release/calc-lite-linux/install.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX="${PREFIX:-$HOME/.local}"
TARGET_DIR="$PREFIX/bin"

mkdir -p "$TARGET_DIR"
install -m 755 "$SCRIPT_DIR/calc-lite" "$TARGET_DIR/calc-lite"

echo "Installed calc-lite to: $TARGET_DIR/calc-lite"
echo "If needed, add this to PATH: export PATH=\"$TARGET_DIR:\$PATH\""
echo "Run with: calc-lite"
EOF
chmod +x release/calc-lite-linux/install.sh

echo "[4/4] Packaging installer tarball..."
tar -C release -czf release/calc-lite-linux.tar.gz calc-lite-linux

echo "Done. Installer package: $ROOT_DIR/release/calc-lite-linux.tar.gz"
echo "Install on target machine:"
echo "  tar -xzf calc-lite-linux.tar.gz"
echo "  cd calc-lite-linux && ./install.sh"
