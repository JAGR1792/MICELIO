# Instalación de Micelio

Esta carpeta contiene los scripts de instalación para Micelio.

## Instalación rápida

### Linux / macOS
```bash
cd /path/to/MICELIO
bash instalación/setup.sh
```

### Windows
```bash
cd \path\to\MICELIO
instalación\setup.bat
```

## ¿Qué hace el setup?

1. Crea un entorno virtual Python (`venv`)
2. Instala dependencias (ANTLR4, etc.)
3. Verifica la instalación de Micelio
4. Instala la extensión de VS Code
5. Instala el comando `micelio` en tu PATH

## Después de instalar

### Linux / macOS
```bash
source venv/bin/activate
micelio archivo.mice          # ejecutar archivo
micelio                        # abrir REPL
```

### Windows
```bash
venv\Scripts\activate.bat
micelio archivo.mice          # ejecutar archivo
micelio                        # abrir REPL
```

## Scripts disponibles

- **setup.sh** - Instalación para Linux/macOS
- **setup.bat** - Instalación para Windows
- **install-micelio.sh** - Instala solamente el comando `micelio` (llamado automáticamente por setup.sh)

---

Para más información, ver: [docs/README.md](../docs/README.md)
