from __future__ import annotations

import shutil
import subprocess
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


# ─── Glassmorphic / Catppuccin Frappe UI ─────────────────────────────

CLR_RED = "\033[38;2;231;130;132m"
CLR_PEACH = "\033[38;2;239;159;118m"
CLR_YELLOW = "\033[38;2;229;200;144m"
CLR_GREEN = "\033[38;2;166;209;137m"
CLR_TEAL = "\033[38;2;129;200;190m"
CLR_SKY = "\033[38;2;153;209;219m"
CLR_BLUE = "\033[38;2;140;170;238m"
CLR_LAVENDER = "\033[38;2;186;187;241m"
CLR_TEXT = "\033[38;2;198;208;245m"
CLR_SUBTEXT = "\033[38;2;165;173;206m"
CLR_MANTLE = "\033[38;2;41;44;60m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
RESET = "\033[0m"


def _glass_box(title: str, content: str, color: str = CLR_LAVENDER) -> str:
    lines = content.splitlines()
    max_len = max(len(line) for line in lines) if lines else 0
    title_line = f" {BOLD}{color}{RESET}{CLR_MANTLE}\033[48;2;{_hex_to_rgb_ansi(color)}m {title} {RESET}{color}{RESET}"
    
    out = [f"\n{title_line}"]
    for line in lines:
        out.append(f"  {CLR_SUBTEXT}│{RESET} {line}")
    out.append("")
    return "\n".join(out)


def _hex_to_rgb_ansi(ansi_color: str) -> str:
    # Hack para obtener el color de fondo aproximado
    if CLR_RED in ansi_color: return "231;130;132"
    if CLR_PEACH in ansi_color: return "239;159;118"
    if CLR_LAVENDER in ansi_color: return "186;187;241"
    if CLR_BLUE in ansi_color: return "140;170;238"
    return "186;187;241"


def _send_system_notification(title: str, msg: str, urgency: str = "normal"):
    notify_send = shutil.which("notify-send")
    if notify_send:
        try:
            # Intentamos usar el icono de Micelio o uno del sistema basado
            subprocess.run([
                notify_send,
                "-a", "Micelio",
                "-u", urgency,
                "-i", "dialog-information" if urgency == "normal" else "dialog-error",
                title,
                msg
            ], check=False)
        except Exception:
            pass


def _line_snippet(source_lines: list[str], line: int, column: int) -> str:
    if line < 1 or line > len(source_lines):
        return ""
    src = source_lines[line - 1]
    caret_col = max(column, 0)
    
    line_str = f"{line:>3} │ "
    code_part = f"{CLR_TEXT}{src}{RESET}"
    pointer = f"    │ {CLR_PEACH}{' ' * caret_col}▲{RESET}"
    return f"{DIM}{line_str}{RESET}{code_part}\n{pointer}"


def _syntax_hint(issue: SyntaxIssue, source_lines: list[str]) -> tuple[str, str]:
    snippet = source_lines[issue.line - 1] if 1 <= issue.line <= len(source_lines) else ""
    msg = issue.message.lower()

    if "mismatched input '\\n' expecting" in msg and "=" in snippet and snippet.strip().endswith("="):
        return (
            "La asignación quedó incompleta: falta la expresión a la derecha de `=`. ",
            "Completa la línea con un valor o expresión. Ejemplos:\n"
            f"  {CLR_GREEN}a = 10{RESET}\n"
            f"  {CLR_GREEN}a = [1, 2, 3]{RESET}"
        )

    if "mismatched input 'leer'" in msg and "." in snippet:
        return (
            "`leer` es una sentencia, no una expresión o método.",
            "Usa:\n"
            f"  {CLR_GREEN}var linea; leer linea{RESET}"
        )

    if "extraneous input '.' expecting id" in msg:
        return (
            "Hay un acceso con punto en una posición donde el parser esperaba otro token.",
            "Verifica que la expresión previa sea válida.\n"
            f"Ejemplo: {CLR_GREEN}linea.separar(){RESET}"
        )

    return (
        "Hay una estructura que no coincide con la gramática de Micelio.",
        "Revisa paréntesis, comas y orden de la sentencia."
    )


def format_pedagogical_syntax_error(exc: PedagogicalSyntaxError) -> str:
    first = exc.issues[0]
    why, fix = _syntax_hint(first, exc.source_lines)
    snippet = _line_snippet(exc.source_lines, first.line, first.column)
    
    header = f"{BOLD}{CLR_RED}󰅚 ERROR DE SINTAXIS{RESET}"
    body = (
        f"{CLR_SUBTEXT}Mensaje:{RESET} {first.message}\n"
        f"{CLR_SUBTEXT}Ubicación:{RESET} Línea {first.line}, Columna {first.column}\n\n"
        f"{snippet}\n\n"
        f"{CLR_SUBTEXT}¿Por qué pasa?{RESET}\n{why}\n\n"
        f"{CLR_SUBTEXT}Sugerencia:{RESET}\n{fix}"
    )
    
    _send_system_notification("Error de Sintaxis", f"Línea {first.line}: {first.message}", "critical")
    return _glass_box(header, body, CLR_RED)


def _runtime_hint(msg: str) -> tuple[str, str]:
    if "no definida" in msg:
        return (
            "Estás usando una variable antes de declararla.",
            f"Declara primero con {CLR_GREEN}var nombre = ...{RESET}"
        )
    if "ya esta definido" in msg:
        return (
            "Estás redeclarando una variable en el mismo ámbito.",
            "Usa asignación {CLR_GREEN}x = ...{RESET} en lugar de {CLR_GREEN}var x{RESET}."
        )
    if "no es invocable" in msg:
        return (
            "Se intentó llamar algo que no es función.",
            "Verifica que sea función: {CLR_GREEN}fn(arg){RESET}."
        )
    return (
        "Falló durante la ejecución de una sentencia.",
        "Revisa tipos de datos y argumentos de funciones."
    )


def format_pedagogical_runtime_error(exc: Exception) -> str:
    raw = str(exc)
    why, fix = _runtime_hint(raw.lower())
    
    header = f"{BOLD}{CLR_PEACH}󰓦 ERROR DE EJECUCIÓN{RESET}"
    body = (
        f"{CLR_SUBTEXT}Qué paso:{RESET} {raw}\n\n"
        f"{CLR_SUBTEXT}¿Por qué pasa?{RESET}\n{why}\n\n"
        f"{CLR_SUBTEXT}Sugerencia:{RESET}\n{fix}"
    )
    
    _send_system_notification("Error de Ejecución", raw, "normal")
    return _glass_box(header, body, CLR_PEACH)


def pipeline_assignment_warning(line: int | str) -> str:
    header = f"{BOLD}{CLR_YELLOW} ADVERTENCIA{RESET}"
    body = (
        f"Línea {line}: La tubería {CLR_SKY}|>{RESET} no modifica la variable original.\n"
        "Haz asignación explícita si deseas guardar el resultado."
    )
    return _glass_box(header, body, CLR_YELLOW)
