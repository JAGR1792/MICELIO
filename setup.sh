#!/bin/bash
set -euo pipefail

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
python -c "import antlr4; print(f'✓ antlr4 version: {antlr4.__version__}')"
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
echo "========================================="
echo "✓ Setup completado!"
echo "========================================="
echo
echo "Para usar Micelio:"
echo "  1. Abre VS Code (recomendado)"
echo "  2. source venv/bin/activate  # activar venv"
echo "  3. cd MICELIO && python main.py  # correr REPL"
echo "  4. cd MICELIO && python main.py archivo.mice  # ejecutar archivo"
echo
echo "Documentación: docs/README.md"
