from __future__ import annotations

from dataclasses import dataclass
from functools import reduce as py_reduce
from typing import Any, Callable


class MicelioRuntimeError(Exception):
    pass


class ReturnFlow(Exception):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value


class BreakFlow(Exception):
    pass


class ContinueFlow(Exception):
    pass


class Environment:
    def __init__(self, parent: "Environment | None" = None):
        self.parent = parent
        self.values: dict[str, Any] = {}
        self.constants: set[str] = set()

    def define(self, name: str, value: Any, is_const: bool = False) -> None:
        if name in self.values:
            raise MicelioRuntimeError(f"'{name}' ya esta definido en este ambito")
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise MicelioRuntimeError(f"Variable '{name}' no definida")

    def assign(self, name: str, value: Any) -> None:
        if name in self.values:
            if name in self.constants:
                raise MicelioRuntimeError(f"No se puede reasignar la constante '{name}'")
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise MicelioRuntimeError(f"Variable '{name}' no definida")


@dataclass
class FunctionValue:
    name: str | None
    params: list[str]
    body_ctx: Any
    closure: Environment

    def call(self, args: list[Any], call_eval: Callable[[Any, Environment], Any]) -> Any:
        if len(args) != len(self.params):
            fname = self.name or "funcion anonima"
            raise MicelioRuntimeError(
                f"{fname} esperaba {len(self.params)} argumento(s), recibio {len(args)}"
            )
        local_env = Environment(self.closure)
        for p, v in zip(self.params, args):
            local_env.define(p, v)
        try:
            call_eval(self.body_ctx, local_env)
        except ReturnFlow as ret:
            return ret.value
        return None


class BoundMethod:
    def __init__(self, obj: Any, name: str):
        self.obj = obj
        self.name = name

    def __call__(self, *args: Any) -> Any:
        if isinstance(self.obj, list):
            if self.name == "agregar":
                if len(args) != 1:
                    raise MicelioRuntimeError("agregar() requiere 1 argumento")
                self.obj.append(args[0])
                return None
            if self.name == "quitar":
                if len(args) != 1:
                    raise MicelioRuntimeError("quitar() requiere 1 argumento")
                self.obj.remove(args[0])
                return None
            if self.name == "insertar":
                if len(args) != 2:
                    raise MicelioRuntimeError("insertar() requiere 2 argumentos")
                self.obj.insert(int(args[0]), args[1])
                return None
            if self.name == "longitud":
                if args:
                    raise MicelioRuntimeError("longitud() no recibe argumentos")
                return len(self.obj)

        if isinstance(self.obj, set):
            if self.name == "agregar":
                if len(args) != 1:
                    raise MicelioRuntimeError("agregar() requiere 1 argumento")
                self.obj.add(args[0])
                return None
            if self.name == "quitar":
                if len(args) != 1:
                    raise MicelioRuntimeError("quitar() requiere 1 argumento")
                self.obj.discard(args[0])
                return None

        if isinstance(self.obj, dict):
            if self.name == "claves":
                if args:
                    raise MicelioRuntimeError("claves() no recibe argumentos")
                return list(self.obj.keys())
            if self.name == "valores":
                if args:
                    raise MicelioRuntimeError("valores() no recibe argumentos")
                return list(self.obj.values())
            if self.name == "items":
                if args:
                    raise MicelioRuntimeError("items() no recibe argumentos")
                return list(self.obj.items())

        if isinstance(self.obj, str):
            if self.name == "longitud":
                if args:
                    raise MicelioRuntimeError("longitud() no recibe argumentos")
                return len(self.obj)

        raise MicelioRuntimeError(f"Metodo '{self.name}' no soportado para {type(self.obj).__name__}")


def to_number(value: Any, base: int = 10) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        txt = value.strip().lower()
        if txt.startswith("0b"):
            return float(int(txt, 2))
        if txt.startswith("0o"):
            return float(int(txt, 8))
        if txt.startswith("0x"):
            return float(int(txt, 16))
        return float(int(txt, base)) if base != 10 else float(txt)
    raise MicelioRuntimeError(f"No se puede convertir {type(value).__name__} a numero")


def int_to_base(n: int, base: int, uppercase: bool = False) -> str:
    if not (2 <= base <= 36):
        raise MicelioRuntimeError("La base debe estar entre 2 y 36")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if uppercase:
        digits = digits.upper()
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    out = []
    while n > 0:
        out.append(digits[n % base])
        n //= base
    rep = "".join(reversed(out))
    return f"-{rep}" if neg else rep


def to_text(value: Any, base: int = 10, mayusculas: bool = False) -> str:
    if isinstance(value, bool):
        return "verdadero" if value else "falso"
    if value is None:
        return "nulo"
    if isinstance(value, (int, float)) and base != 10:
        return int_to_base(int(value), int(base), uppercase=bool(mayusculas))
    return str(value)


def to_bool(value: Any) -> bool:
    return bool(value)


def matrix_mul(a: list[list[Any]], b: list[list[Any]]) -> list[list[float]]:
    if not a or not b:
        return []
    a_cols = len(a[0])
    b_rows = len(b)
    if a_cols != b_rows:
        raise MicelioRuntimeError("Dimensiones invalidas para multiplicacion matricial")
    b_cols = len(b[0])
    out = []
    for i in range(len(a)):
        row = []
        for j in range(b_cols):
            total = 0.0
            for k in range(a_cols):
                total += float(a[i][k]) * float(b[k][j])
            row.append(total)
        out.append(row)
    return out


def elementwise_mul(left: Any, right: Any) -> Any:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left * right
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            raise MicelioRuntimeError("Producto elemento a elemento requiere mismo tamano")
        return [elementwise_mul(l, r) for l, r in zip(left, right)]
    raise MicelioRuntimeError("Operacion .*, tipos no compatibles")


def make_builtins() -> dict[str, Any]:
    def _map(fn: Callable[..., Any], iterable: list[Any]) -> list[Any]:
        return [fn(x) for x in iterable]

    def _filter(fn: Callable[..., Any], iterable: list[Any]) -> list[Any]:
        return [x for x in iterable if fn(x)]

    def _reduce(fn: Callable[..., Any], iterable: list[Any], initial: Any) -> Any:
        return py_reduce(fn, iterable, initial)

    def _a_binario(n: Any) -> str:
        return int_to_base(int(to_number(n)), 2)

    def _a_octal(n: Any) -> str:
        return int_to_base(int(to_number(n)), 8)

    def _a_hexadecimal(n: Any) -> str:
        return int_to_base(int(to_number(n)), 16)

    def _a_base(n: Any, base: Any) -> str:
        return int_to_base(int(to_number(n)), int(to_number(base)))

    def _desde_base(texto: Any, base: Any) -> float:
        return float(int(str(texto), int(to_number(base))))

    return {
        "map": _map,
        "filter": _filter,
        "reduce": _reduce,
        "longitud": lambda x: len(x),
        "aNumero": to_number,
        "aTexto": to_text,
        "aBooleano": to_bool,
        "aBinario": _a_binario,
        "aOctal": _a_octal,
        "aHexadecimal": _a_hexadecimal,
        "aBase": _a_base,
        "desdeBinario": lambda txt: _desde_base(txt, 2),
        "desdeOctal": lambda txt: _desde_base(txt, 8),
        "desdeHexadecimal": lambda txt: _desde_base(txt, 16),
        "desdeBase": _desde_base,
    }


def module_table() -> dict[str, dict[str, Any]]:
    builtins = make_builtins()
    return {
        "convert": {
            "aNumero": builtins["aNumero"],
            "aTexto": builtins["aTexto"],
            "aBooleano": builtins["aBooleano"],
            "aBinario": builtins["aBinario"],
            "aOctal": builtins["aOctal"],
            "aHexadecimal": builtins["aHexadecimal"],
            "aBase": builtins["aBase"],
            "desdeBinario": builtins["desdeBinario"],
            "desdeOctal": builtins["desdeOctal"],
            "desdeHexadecimal": builtins["desdeHexadecimal"],
            "desdeBase": builtins["desdeBase"],
        },
        "lista": {
            "map": builtins["map"],
            "filter": builtins["filter"],
            "reduce": builtins["reduce"],
        },
    }


def micelio_repr(value: Any) -> str:
    if value is True:
        return "verdadero"
    if value is False:
        return "falso"
    if value is None:
        return "nulo"
    if isinstance(value, list):
        return "[" + ", ".join(micelio_repr(v) for v in value) + "]"
    if isinstance(value, set):
        return "{" + ", ".join(sorted(micelio_repr(v) for v in value)) + "}"
    if isinstance(value, dict):
        items = [f"{micelio_repr(k)}: {micelio_repr(v)}" for k, v in value.items()]
        return "{" + ", ".join(items) + "}"
    return str(value)
