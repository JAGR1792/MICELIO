from __future__ import annotations

import os
import sys

from antlr4 import CommonTokenStream, InputStream

from MicelioLexer import MicelioLexer
from MicelioParser import MicelioParser
from eval_visitor import EvalVisitor
from runtime import MicelioRuntimeError, micelio_repr


def execute(code: str, visitor: EvalVisitor):
    lexer = MicelioLexer(InputStream(code))
    tokens = CommonTokenStream(lexer)
    parser = MicelioParser(tokens)
    tree = parser.program()
    return visitor.visit(tree)


def repl() -> None:
    visitor = EvalVisitor(base_dir=os.getcwd())
    print("Micelio REPL (exit para salir)")
    while True:
        try:
            line = input("micelio> ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            break

        if line.strip().lower() in {"exit", "quit", "q"}:
            break
        if not line.strip():
            continue

        try:
            result = execute(line + "\n", visitor)
            if result is not None:
                print(micelio_repr(result))
        except (MicelioRuntimeError, Exception) as exc:
            print(f"Error: {exc}")


def run_file(path: str) -> int:
    abs_path = os.path.abspath(path)
    visitor = EvalVisitor(base_dir=os.path.dirname(abs_path))
    with open(abs_path, "r", encoding="utf-8") as f:
        code = f.read()
    try:
        execute(code, visitor)
        return 0
    except (MicelioRuntimeError, Exception) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(run_file(sys.argv[1]))
    repl()
