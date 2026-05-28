#!/usr/bin/env python3
"""Test runner: ejecuta todos los .mice de ejemplos y verifica que terminen sin error."""

import os
import sys
import subprocess
import time

MICELIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAIN_PY = os.path.join(MICELIO_DIR, "MICELIO", "main.py")
EJEMPLOS_DIR = os.path.join(MICELIO_DIR, "MICELIO", "ejemplos")
SCRATCH_DIR = os.path.join(EJEMPLOS_DIR, "scratch")
SKIP = {
    "04_errores.mice",  # espera errores
    "06_caperucita.mice",  # requiere entrada interactiva
    "30_gui_didactico.mice",  # requiere GTK
    "31_hifa_didactico.mice",  # requiere Flask
}


def discover_examples():
    examples = []
    for root, dirs, files in os.walk(EJEMPLOS_DIR):
        for f in files:
            if f.endswith(".mice") and f not in SKIP:
                examples.append(os.path.join(root, f))
    return sorted(examples)


def run_test(path):
    rel = os.path.relpath(path, MICELIO_DIR)
    start = time.time()
    result = subprocess.run(
        [sys.executable, MAIN_PY, path],
        capture_output=True, text=True, timeout=120
    )
    elapsed = time.time() - start
    ok = result.returncode == 0
    return ok, elapsed, rel, result.stdout, result.stderr


def main():
    examples = discover_examples()
    passed = 0
    failed = 0
    total = len(examples)

    print(f"MICELIO Test Runner — {total} ejemplos encontrados\n")
    print(f"{'':-^60}", "   Tiempo")
    print(f"{'Archivo':<50} {'Estado':<8} {'(s)'}")

    for path in examples:
        ok, elapsed, rel, stdout, stderr = run_test(path)
        status = "✅ OK" if ok else "❌ FAIL"
        elapsed_s = f"{elapsed:.2f}"
        print(f"{rel:<50} {status:<8} {elapsed_s}s")
        if not ok:
            failed += 1
            print(f"  STDERR: {stderr[:500]}")
        else:
            passed += 1

    print(f"\n{'='*60}")
    print(f"Total: {total} | Pasaron: {passed} | Fallaron: {failed}")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
