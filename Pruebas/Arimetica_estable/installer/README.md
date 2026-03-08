# Calc Lite Installer (Linux)

This builds an installable package for the lightweight arithmetic demo.

## Build

```bash
cd Pruebas/Arimetica_estable/installer
./build-linux.sh
```

Output:

- `Pruebas/Arimetica_estable/release/calc-lite-linux.tar.gz`

## Install on a target Linux machine

```bash
tar -xzf calc-lite-linux.tar.gz
cd calc-lite-linux
./install.sh
```

By default it installs to `~/.local/bin/calc-lite`.

## Run

```bash
calc-lite
```

Then type an expression, e.g.:

- `2+3*4`
- `(10-2)/2`
