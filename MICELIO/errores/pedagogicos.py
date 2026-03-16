from __future__ import annotations

from dataclasses import dataclass

from antlr4.error.ErrorListener import ErrorListener


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


def pipeline_assignment_warning(line: int | str) -> str:
    return (
        f"[WARNING pedagogico] linea {line}: "
        "la tuberia `|>` no modifica la variable original por si sola. "
        "Haz asignacion explicita, por ejemplo: "
        "\n`datos = datos"
        "\n   |> map(funcion (x) { x * 2 })`\n"
    )
