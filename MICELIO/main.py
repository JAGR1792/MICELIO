from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from MicelioLexer import MicelioLexer
from MicelioParser import MicelioParser
from eval_visitor import EvalVisitor
from runtime import MicelioRuntimeError, micelio_repr


@dataclass
class SyntaxIssue:
    line: int
    column: int
    message: str
    offending_text: str


class PedagogicalSyntaxError(Exception):
    def __init__(self, issues: list[SyntaxIssue], source_lines: list[str]):
        super().__init__("Error de sintaxis en Micelio")
        self.issues = issues
        self.source_lines = source_lines


class PedagogicalErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.issues: list[SyntaxIssue] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        text = getattr(offendingSymbol, "text", "") if offendingSymbol else ""
        self.issues.append(SyntaxIssue(line, column, msg, text))


def _line_snippet(source_lines: list[str], line: int, column: int) -> str:
    if line < 1 or line > len(source_lines):
        return ""
    src = source_lines[line - 1]
    caret_col = max(column, 0)
    return f"{line:>3} | {src}\n    | {' ' * caret_col}^"


def _syntax_hint(issue: SyntaxIssue, source_lines: list[str]) -> tuple[str, str]:
    snippet = source_lines[issue.line - 1] if 1 <= issue.line <= len(source_lines) else ""
    msg = issue.message.lower()

    if "mismatched input '\\n' expecting" in msg and "=" in snippet and snippet.strip().endswith("="):
        return (
            "La asignacion quedo incompleta: falta la expresion a la derecha de `=`.",
            "Completa la linea con un valor o expresion. Ejemplos:\n"
            "  a = 10\n"
            "  a = [1, 2, 3]\n"
            "  a = b + 1",
        )

    if "mismatched input 'leer'" in msg and "." in snippet:
        return (
            "`leer` es una sentencia, no una expresion o metodo.",
            "Usa:\n"
            "  var linea\n"
            "  leer linea\n"
            "  var partes = linea.separar()",
        )

    if "extraneous input '.' expecting id" in msg:
        return (
            "Hay un acceso con punto en una posicion donde el parser esperaba otro token.",
            "Verifica que la expresion previa sea valida y que el metodo exista.\n"
            "Ejemplo correcto: `linea.separar()`",
        )

    if "expecting id" in msg and "leer" in snippet:
        return (
            "La instruccion `leer` solo acepta una variable por sentencia en la gramatica actual.",
            "En lugar de `leer a,b`, usa:\n"
            "  leer linea\n"
            "  var a, b = linea.separar()",
        )

    return (
        "Hay una estructura que no coincide con la gramatica de Micelio.",
        "Revisa parentesis, comas y orden de la sentencia cerca del simbolo marcado.",
    )


def format_pedagogical_syntax_error(exc: PedagogicalSyntaxError) -> str:
    first = exc.issues[0]
    why, fix = _syntax_hint(first, exc.source_lines)
    snippet = _line_snippet(exc.source_lines, first.line, first.column)
    return (
        "Error de (sintaxis)\n"
        f"Que paso: {first.message}\n"
        f"Donde: linea {first.line}, columna {first.column}\n"
        f"{snippet}\n"
        f"Por que pasa: {why}\n"
        f"Como arreglarlo: {fix}"
    )


def _runtime_hint(msg: str) -> tuple[str, str]:
    if "no definida" in msg:
        return (
            "Estas usando una variable antes de declararla o fuera de su ambito.",
            "Declara primero con `var nombre = ...` y usa el mismo identificador.",
        )
    if "ya esta definido" in msg:
        return (
            "Estas redeclarando una variable en el mismo ambito.",
            "Usa asignacion (`x = ...`) en lugar de `var x` si ya existe.",
        )
    if "no es invocable" in msg:
        return (
            "Se intento llamar algo que no es funcion/metodo.",
            "Verifica que sea funcion y que uses parentesis correctos: `fn(arg)`.",
        )
    if "desempaquetado" in msg:
        return (
            "El desempaquetado requiere una lista/tupla con el mismo numero de elementos.",
            "Ejemplo: `var a, b = linea.separar()` con una linea que tenga 2 partes.",
        )
    if "leer multiple" in msg or "cantidad de entradas no coincide" in msg:
        return (
            "En `leer a, b, ...` la linea de entrada debe tener exactamente la misma cantidad de valores.",
            "Ejemplo: para `leer a, b` escribe algo como `10 20` en una sola linea.",
        )
    if "asignar_multi" in msg or "cantidad de valores no coincide" in msg:
        return (
            "La asignacion multiple requiere que el lado derecho tenga exactamente la misma cantidad de elementos.",
            "Ejemplo: `a, b = [1, 2]` (2 variables, 2 valores).",
        )
    return (
        "Fallo durante la ejecucion de una sentencia.",
        "Revisa tipos de datos y argumentos de funciones en la linea reportada.",
    )


def format_pedagogical_runtime_error(exc: Exception) -> str:
    raw = str(exc)
    why, fix = _runtime_hint(raw.lower())
    return (
        "Error de (ejecucion)\n"
        f"Que paso: {raw}\n"
        f"Por que pasa: {why}\n"
        f"Como arreglarlo: {fix}"
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
