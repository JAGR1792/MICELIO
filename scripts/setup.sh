#!/bin/bash
set -euo pipefail

# Obtener directorio raíz del proyecto
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "=== Micelio Setup (Linux/Mac) ==="
echo

# Crear venv
if [ ! -d "venv" ]; then
    echo "1. Creando entorno virtual..."
    python3 -m venv venv
    echo "✓ venv creado"
else
    echo "✓ venv ya existe"
fi

echo
echo "2. Activando venv e instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencias instaladas"

echo
echo "3. Verificando instalacion..."
python -c "import antlr4; import importlib.metadata; v = importlib.metadata.version('antlr4-python3-runtime'); print(f'✓ antlr4 version: {v}')"
cd MICELIO && python eval_visitor.py && cd ..
echo "✓ Micelio setup completado"

echo
echo "4. Instalando extension VS Code..."
if command -v code &> /dev/null; then
    cd micelio-vscode/extension_unpacked
    code --install-extension . 2>/dev/null || echo "⚠ No se pudo instalar la extension automáticamente."
    echo "ℹ Si tienes problemas, instala manualmente: micelio-vscode/extension_unpacked/"
    cd ../..
else
    echo "⚠ VS Code no está instalado o no está en PATH."
    echo "ℹ Instálalo desde https://code.visualstudio.com"
    echo "ℹ Luego ejecuta: code --install-extension micelio-vscode/extension_unpacked/"
fi

echo
echo "5. Instalando comando 'micelio'..."
bash "$SCRIPT_DIR/install-micelio.sh"
echo

echo "========================================="
echo "✓ Setup completado!"
echo "========================================="
echo
echo "Para usar Micelio:"
echo "  1. source venv/bin/activate  # activar venv"
echo "  2. micelio archivo.mice      # ejecutar archivo"
echo "  3. micelio                   # abrir REPL"
echo "  4. Abre VS Code (recomendado)"
echo
echo "Documentación: docs/README.md"
