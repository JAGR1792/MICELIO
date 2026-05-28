@echo off
REM Micelio Setup para Windows

echo === Micelio Setup (Windows) ===
echo.

REM Obtener directorio raiz del proyecto
cd /d "%~dp0\.."

REM Crear venv
if not exist venv (
    echo 1. Creando entorno virtual...
    python -m venv venv
    echo OK: venv creado
) else (
    echo OK: venv ya existe
)

echo.
echo 2. Activando venv e instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo OK: Dependencias instaladas

echo.
echo 3. Verificando instalacion...
python -c "import antlr4; import importlib.metadata; v = importlib.metadata.version('antlr4-python3-runtime'); print(f'OK: antlr4 version: {v}')"
cd MICELIO && python eval_visitor.py && cd ..
echo OK: Micelio setup completado

echo.
echo 4. Instalando extension VS Code...
where code >nul 2>nul
if %errorlevel% equ 0 (
    echo Intentando instalar extension...
    cd micelio-vscode\extension_unpacked
    code --install-extension . 2>nul || (
        echo ADVERTENCIA: No se pudo instalar la extension automaticamente.
    )
    echo INFO: Si tienes problemas, instala manualmente: micelio-vscode\extension_unpacked\
    cd ..\..
) else (
    echo ADVERTENCIA: VS Code no esta instalado o no esta en PATH.
    echo INFO: Descargalo desde https://code.visualstudio.com
    echo INFO: Luego ejecuta: code --install-extension micelio-vscode\extension_unpacked\
)

echo.
echo =========================================
echo OK: Setup completado!
echo =========================================
echo.
echo Para usar Micelio:
echo   1. venv\Scripts\activate.bat  REM activar venv
echo   2. micelio archivo.mice       REM ejecutar archivo
echo   3. micelio                    REM abrir REPL
echo   4. Abre VS Code (recomendado)
echo.
echo Documentacion: docs\README.md
pause
