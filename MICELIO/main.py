from __future__ import annotations

import os
import re
import sys

from antlr4 import CommonTokenStream, InputStream

from generado.MicelioLexer import MicelioLexer
from generado.MicelioParser import MicelioParser
from nucleo.eval_visitor import EvalVisitor
from nucleo.runtime import MicelioRuntimeError, micelio_repr
from errores.pedagogicos import (
    PedagogicalErrorListener,
    PedagogicalSyntaxError,
    format_pedagogical_runtime_error,
    format_pedagogical_syntax_error,
)


_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
_LEER_MULTI_RE = re.compile(
    rf"^(?P<indent>\s*)leer\s+(?P<names>{_ID}(?:\s*,\s*{_ID})+)\s*(?P<trail>#.*)?$"
)
_ASSIGN_MULTI_RE = re.compile(
    rf"^(?P<indent>\s*)(?P<names>{_ID}(?:\s*,\s*{_ID})+)\s*=\s*(?P<expr>.+?)\s*(?P<trail>#.*)?$"
)
_COMPOUND_ASSIGN_RE = re.compile(
    rf"^(?P<indent>\s*)(?P<name>{_ID})\s*(?P<op>\*\*=|\+=|-=|\*=|/=|%=)\s*(?P<expr>.+?)\s*(?P<trail>#.*)?$"
)


def preprocess_source(code: str) -> str:
    out_lines: list[str] = []
    for raw_line in code.splitlines():
        line = raw_line
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out_lines.append(line)
            continue

        leer_match = _LEER_MULTI_RE.match(line)
        if leer_match:
            indent = leer_match.group("indent")
            names = ",".join(
                part.strip() for part in leer_match.group("names").split(",")
            )
            trail = f" {leer_match.group('trail')}" if leer_match.group("trail") else ""
            out_lines.append(f'{indent}__leer_multi("{names}"){trail}')
            continue

        assign_match = _ASSIGN_MULTI_RE.match(line)
        if assign_match:
            indent = assign_match.group("indent")
            names = ",".join(
                part.strip() for part in assign_match.group("names").split(",")
            )
            expr = assign_match.group("expr").strip()
            trail = f" {assign_match.group('trail')}" if assign_match.group("trail") else ""
            out_lines.append(f'{indent}__asignar_multi("{names}", {expr}){trail}')
            continue

        compound_match = _COMPOUND_ASSIGN_RE.match(line)
        if compound_match:
            indent = compound_match.group("indent")
            name = compound_match.group("name")
            op = compound_match.group("op")[:-1]
            expr = compound_match.group("expr").strip()
            trail = f" {compound_match.group('trail')}" if compound_match.group("trail") else ""
            out_lines.append(f"{indent}{name} = {name} {op} ({expr}){trail}")
            continue

        out_lines.append(line)

    return "\n".join(out_lines) + ("\n" if code.endswith("\n") else "")


def execute(code: str, visitor: EvalVisitor):
    preprocessed = preprocess_source(code)
    lexer = MicelioLexer(InputStream(preprocessed))
    source_lines = preprocessed.splitlines()
    syntax_listener = PedagogicalErrorListener()

    lexer.removeErrorListeners()
    lexer.addErrorListener(syntax_listener)

    tokens = CommonTokenStream(lexer)
    parser = MicelioParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(syntax_listener)

    tree = parser.program()
    if syntax_listener.issues:
        raise PedagogicalSyntaxError(syntax_listener.issues, source_lines)
    return visitor.visit(tree)


def repl() -> None:
    visitor = EvalVisitor(base_dir=os.getcwd())
    # _ siempre existe en global env para pipe-continuation lines
    visitor.global_env.values["_"] = None
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

        # Una linea comenzando con |> continua el resultado anterior via _
        if line.lstrip().startswith("|>"):
            line = "_ " + line.lstrip()

        try:
            result = execute(line + "\n", visitor)
            if result is not None:
                visitor.global_env.values["_"] = result
                print(micelio_repr(result))
        except PedagogicalSyntaxError as exc:
            print(format_pedagogical_syntax_error(exc))
        except (MicelioRuntimeError, Exception) as exc:
            print(format_pedagogical_runtime_error(exc))


def run_file(path: str) -> int:
    abs_path = os.path.abspath(path)
    visitor = EvalVisitor(base_dir=os.path.dirname(abs_path))
    with open(abs_path, "r", encoding="utf-8") as f:
        code = f.read()
    try:
        execute(code, visitor)
        return 0
    except PedagogicalSyntaxError as exc:
        print(format_pedagogical_syntax_error(exc))
        return 1
    except (MicelioRuntimeError, Exception) as exc:
        print(format_pedagogical_runtime_error(exc))
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(run_file(sys.argv[1]))
    repl()
